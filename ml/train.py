import os
import sys

# Ensure backend and ml folders are in python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.app.database import SessionLocal
from backend.app.models import FactoryData
from ml.models.profit_predictor import ProfitPredictor
from ml.models.health_scorer import HealthScorer

def train_models():
    """
    Connects to the SQLite database, pulls all historical factory records,
    and retrains both the Profit Predictor (Linear Regressor) and Business Health Scorer (Decision Tree).
    """
    print("Starting MSME Decision Support System ML model training...")
    
    db = SessionLocal()
    try:
        # Fetch all records
        records = db.query(FactoryData).all()
        record_count = len(records)
        print(f"Retrieved {record_count} historical records from the database.")
        
        if record_count < 5:
            print("Insufficient data for training models. At least 5 records are required.")
            print("Please enter more factory data or upload a CSV file via the dashboard to enable ML training.")
            return False
            
        # Retrain Profit Predictor
        predictor = ProfitPredictor()
        predictor_success = predictor.train(records)
        if predictor_success:
            print("Profit Regressor (Linear Regression) trained and saved successfully.")
        else:
            print("Failed to train Profit Regressor.")

        # Retrain Health Scorer
        scorer = HealthScorer()
        scorer_success = scorer.train(records)
        if scorer_success:
            print("Health Classifier (Decision Tree) trained and saved successfully.")
        else:
            print("Failed to train Health Classifier.")
            
        return predictor_success and scorer_success
        
    except Exception as e:
        print(f"Training error occurred: {str(e)}")
        return False
    finally:
        db.close()

if __name__ == "__main__":
    train_models()
