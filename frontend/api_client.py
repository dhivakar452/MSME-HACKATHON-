"""
API Client for the MSME Decision Support System Frontend.
Wraps all HTTP calls to the FastAPI backend running on localhost:8000.
"""

import requests
from typing import Optional, Dict, Any, List

BASE_URL = "http://127.0.0.1:8000"


class APIClient:
    def __init__(self, token: Optional[str] = None):
        self.token = token
        self.session = requests.Session()
        if token:
            self.session.headers.update({"Authorization": f"Bearer {token}"})

    def set_token(self, token: str):
        self.token = token
        self.session.headers.update({"Authorization": f"Bearer {token}"})

    # ------------------------------------------------------------------
    # Authentication
    # ------------------------------------------------------------------
    def register(self, username: str, password: str, email: str = "") -> Dict[str, Any]:
        payload = {"username": username, "password": password, "email": email}
        r = self.session.post(f"{BASE_URL}/register", json=payload)
        return {"status": r.status_code, "data": r.json()}

    def login(self, username: str, password: str) -> Dict[str, Any]:
        r = self.session.post(
            f"{BASE_URL}/login",
            data={"username": username, "password": password},
        )
        if r.status_code == 200:
            data = r.json()
            self.set_token(data.get("access_token", ""))
        return {"status": r.status_code, "data": r.json()}

    # ------------------------------------------------------------------
    # Factory Data
    # ------------------------------------------------------------------
    def add_factory_data(self, payload: Dict[str, Any]) -> Dict[str, Any]:
        r = self.session.post(f"{BASE_URL}/factory-data", json=payload)
        return {"status": r.status_code, "data": r.json() if r.content else {}}

    def get_factory_data(self, skip: int = 0, limit: int = 500) -> List[Dict]:
        r = self.session.get(f"{BASE_URL}/factory-data", params={"skip": skip, "limit": limit})
        if r.status_code == 200:
            return r.json()
        return []

    def health_check(self) -> bool:
        try:
            r = requests.get(f"{BASE_URL}/docs", timeout=3)
            return r.status_code == 200
        except Exception:
            return False
