import os
import sys
import unittest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Ensure the root folder is in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.main import app
from backend.app.database import Base, get_db
from backend.app.auth import SECRET_KEY, ALGORITHM

# Setup separate isolated Test database
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_database.db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False})
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def override_get_db():
    try:
        db = TestingSessionLocal()
        yield db
    finally:
        db.close()

# Apply dependency override to FastAPI app
app.dependency_overrides[get_db] = override_get_db

class TestMSMEAppAPI(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        # Create tables in test DB
        Base.metadata.create_all(bind=engine)
        cls.client = TestClient(app)

    @classmethod
    def tearDownClass(cls):
        # Drop test tables and clean up the database file
        Base.metadata.drop_all(bind=engine)
        if os.path.exists("./test_database.db"):
            try:
                os.remove("./test_database.db")
            except PermissionError:
                pass

    def test_01_user_registration(self):
        """Test user registration endpoint."""
        response = self.client.post(
            "/register",
            json={"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.json()["username"], "testuser")
        self.assertIn("id", response.json())

    def test_02_user_login(self):
        """Test JWT token retrieval endpoint."""
        response = self.client.post(
            "/token",
            data={"username": "testuser", "password": "testpassword123"}
        )
        self.assertEqual(response.status_code, 200)
        token_data = response.json()
        self.assertIn("access_token", token_data)
        self.assertEqual(token_data["token_type"], "bearer")
        # Store token for subsequent tests
        self.__class__.token = token_data["access_token"]

    def test_03_add_factory_data(self):
        """Test daily factory metrics submission endpoint."""
        headers = {"Authorization": f"Bearer {self.token}"}
        record_data = {
            "date": "2026-07-01",
            "sales": 10000.0,
            "production": 500.0,
            "electricity_bill": 800.0,
            "raw_material_cost": 3000.0,
            "salary": 2000.0,
            "inventory": 1500.0,
            "machine_running_hours": 8.0,
            "machine_downtime": 1.5,
            "profit": 4200.0
        }
        response = self.client.post("/factory-data", json=record_data, headers=headers)
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()["date"], "2026-07-01")
        self.assertEqual(response.json()["profit"], 4200.0)

    def test_04_get_dashboard_metrics(self):
        """Test dashboard summary endpoint."""
        headers = {"Authorization": f"Bearer {self.token}"}
        response = self.client.get("/dashboard-metrics", headers=headers)
        self.assertEqual(response.status_code, 200)
        metrics = response.json()
        self.assertEqual(metrics["today_sales"], 10000.0)
        self.assertEqual(metrics["today_profit"], 4200.0)
        # Verify AI recommendation engine populated recommendations
        self.assertTrue(len(metrics["recommendations"]) > 0)

    def test_05_csv_upload_validation(self):
        """Test uploading non-csv file returns error."""
        headers = {"Authorization": f"Bearer {self.token}"}
        files = {"file": ("test.txt", b"plain text data", "text/plain")}
        response = self.client.post("/factory-data/upload", files=files, headers=headers)
        self.assertEqual(response.status_code, 400)
        self.assertIn("Only CSV files are supported", response.json()["detail"])

if __name__ == "__main__":
    unittest.main()
