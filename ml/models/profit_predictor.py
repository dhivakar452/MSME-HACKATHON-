import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LinearRegression
from typing import List, Any

class ProfitPredictor:
    """
    Linear Regression model wrapper to predict future profit of an MSME factory
    based on sales, production, electricity cost, inventory, salary, and machine running hours.
    """
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            # Set default directory to store serialized models
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.model_dir = os.path.join(base_dir, "saved_models")
        else:
            self.model_dir = model_dir
            
        os.makedirs(self.model_dir, exist_ok=True)
        self.model_path = os.path.join(self.model_dir, "profit_regressor.pkl")
        self.model = None
        self.is_trained = False
        
        # Load model from disk if it already exists
        self.load()

    def train(self, records: List[Any]) -> bool:
        """
        Trains the Linear Regression model on lists of FactoryData SQLAlchemy or Dict models.
        """
        if len(records) < 5:
            # We need at least 5 records to fit a meaningful multi-variable linear model
            return False
            
        try:
            # Convert SQLAlchemy models/objects to dictionaries
            data_list = []
            for r in records:
                if hasattr(r, "__dict__"):
                    # SQLAlchemy objects
                    d = {col.name: getattr(r, col.name) for col in r.__table__.columns}
                else:
                    d = dict(r)
                data_list.append(d)
                
            df = pd.DataFrame(data_list)
            
            # Map database schema columns to predictor features
            # Required Features: Sales, Production, Electricity, Inventory, Salary, Machine Running Hours
            X = df[['sales', 'production', 'electricity_bill', 'inventory', 'salary', 'machine_running_hours']]
            y = df['profit']
            
            # Fit model
            reg = LinearRegression()
            reg.fit(X, y)
            
            self.model = reg
            self.is_trained = True
            
            # Save the trained model to disk
            with open(self.model_path, "wb") as f:
                pickle.dump(self.model, f)
            return True
            
        except Exception as e:
            print(f"Error during ProfitPredictor training: {str(e)}")
            return False

    def predict(self, sales: float, production: float, electricity: float, inventory: float, salary: float, machine_running_hours: float) -> float:
        """
        Predicts profit based on input features. Falls back to a heuristic if model is not trained.
        """
        if self.is_trained and self.model is not None:
            try:
                features = np.array([[sales, production, electricity, inventory, salary, machine_running_hours]])
                prediction = self.model.predict(features)[0]
                return float(prediction)
            except Exception as e:
                print(f"Error during ProfitPredictor prediction: {str(e)}")
                # Fail-safe fallback if prediction crashes
        
        # Heuristic Fallback: A rough estimation representing base profit margin (e.g., 15% of Sales minus fixed/variable approximations)
        # In a real factory: Profit = Sales - Costs
        # We model this roughly as: sales * 0.20 - electricity * 0.5 - salary * 0.1
        approx_profit = (sales * 0.25) - (electricity * 0.1) - (salary * 0.05)
        return float(approx_profit)

    def load(self) -> bool:
        """Loads a pre-trained model from disk if it exists."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                self.is_trained = True
                return True
            except Exception as e:
                print(f"Error loading profit regressor model: {str(e)}")
        return False
