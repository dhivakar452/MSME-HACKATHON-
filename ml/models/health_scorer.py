import os
import pickle
import numpy as np
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from typing import List, Tuple, Any

class HealthScorer:
    """
    Evaluates the business health of an MSME factory.
    Starts as a rule-based engine and transitions to a Decision Tree Classifier
    once retrained with sufficient historical records.
    """
    def __init__(self, model_dir: str = None):
        if model_dir is None:
            base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
            self.model_dir = os.path.join(base_dir, "saved_models")
        else:
            self.model_dir = model_dir
            
        os.makedirs(self.model_dir, exist_ok=True)
        self.model_path = os.path.join(self.model_dir, "health_classifier.pkl")
        self.classifier = None
        self.is_trained = False
        
        # Mapping of numeric classes back to categorical tags
        self.categories_map = {0: "Risk", 1: "Average", 2: "Good", 3: "Excellent"}
        self.reverse_map = {v: k for k, v in self.categories_map.items()}
        
        # Load pre-trained decision tree from disk if it exists
        self.load()

    def _rule_based_evaluate(self, profit: float, sales: float, production: float, electricity: float, inventory: float, machine_downtime: float) -> Tuple[float, str]:
        """
        Heuristic / Rule-based scoring engine.
        Calculates a composite health score out of 100 based on factory ratios.
        """
        score = 50.0  # Baseline score

        # 1. Profit Margin Impact (Up to 30 points)
        if sales > 0:
            margin = profit / sales
            if margin >= 0.25:
                score += 30.0
            elif margin >= 0.15:
                score += 20.0
            elif margin >= 0.05:
                score += 10.0
            elif margin < 0.0:
                score -= 15.0  # Penalize for operating at a loss
        else:
            score -= 20.0

        # 2. Machine Downtime Impact (Up to 15 points)
        # Downtime ratio relative to a standard 24 hour cycle
        downtime_ratio = machine_downtime / 24.0 if machine_downtime <= 24.0 else 1.0
        if downtime_ratio <= 0.05:     # Less than 1.2 hours
            score += 15.0
        elif downtime_ratio <= 0.15:   # Less than 3.6 hours
            score += 5.0
        elif downtime_ratio > 0.30:    # High downtime (over 7.2 hours)
            score -= 15.0

        # 3. Inventory to Sales ratio (Up to 15 points)
        if sales > 0:
            inv_ratio = inventory / sales
            if 0.1 <= inv_ratio <= 0.4:
                score += 15.0  # Healthy inventory turnover
            elif inv_ratio > 1.0:
                score -= 10.0  # Over-stocked inventory, tied up capital
            elif inv_ratio < 0.05:
                score -= 5.0   # Under-stocked, stockout risk
        else:
            score -= 10.0

        # 4. Production to Sales alignment (Up to 10 points)
        if production > 0 and sales > 0:
            prod_sales_ratio = production / sales
            # If production volume roughly matches sales levels, efficiency is high
            if 0.8 <= prod_sales_ratio <= 1.2:
                score += 10.0
            elif prod_sales_ratio > 2.0:
                score -= 5.0  # Over-producing relative to sales demand
        
        # Ensure score bounds [0.0, 100.0]
        score = max(0.0, min(100.0, score))

        # Categorize health based on composite score
        if score >= 80.0:
            category = "Excellent"
        elif score >= 60.0:
            category = "Good"
        elif score >= 40.0:
            category = "Average"
        else:
            category = "Risk"
            
        return score, category

    def train(self, records: List[Any]) -> bool:
        """
        Trains a Decision Tree Classifier on the historical data.
        Labels the historical data using the rule-based scorer first, then trains the tree.
        """
        if len(records) < 5:
            return False
            
        try:
            data_list = []
            for r in records:
                if hasattr(r, "__dict__"):
                    d = {col.name: getattr(r, col.name) for col in r.__table__.columns}
                else:
                    d = dict(r)
                data_list.append(d)
                
            df = pd.DataFrame(data_list)
            
            # Programmatically label training rows using the rule engine
            categories = []
            for _, row in df.iterrows():
                _, cat = self._rule_based_evaluate(
                    profit=row['profit'],
                    sales=row['sales'],
                    production=row['production'],
                    electricity=row['electricity_bill'],
                    inventory=row['inventory'],
                    machine_downtime=row['machine_downtime']
                )
                categories.append(self.reverse_map[cat])
                
            df['category_label'] = categories
            
            # Required Inputs for model 2
            X = df[['profit', 'sales', 'production', 'electricity_bill', 'inventory', 'machine_downtime']]
            y = df['category_label']
            
            # Train the Decision Tree
            clf = DecisionTreeClassifier(max_depth=4, random_state=42)
            clf.fit(X, y)
            
            self.classifier = clf
            self.is_trained = True
            
            # Save classifier to disk
            with open(self.model_path, "wb") as f:
                pickle.dump(self.classifier, f)
            return True
            
        except Exception as e:
            print(f"Error training DecisionTree HealthScorer: {str(e)}")
            return False

    def score(self, profit: float, sales: float, production: float, electricity: float, inventory: float, machine_downtime: float) -> Tuple[float, str]:
        """
        Evaluates and outputs the health score and health category.
        Uses Decision Tree if trained, else defaults to rule-based engine.
        """
        # Always compute rule-based score to give a fine-grained float score [0-100]
        calculated_score, rule_category = self._rule_based_evaluate(profit, sales, production, electricity, inventory, machine_downtime)
        
        # Use Decision Tree Classifier for category prediction if trained
        if self.is_trained and self.classifier is not None:
            try:
                features = np.array([[profit, sales, production, electricity, inventory, machine_downtime]])
                pred_class = self.classifier.predict(features)[0]
                category = self.categories_map.get(pred_class, rule_category)
                return calculated_score, category
            except Exception as e:
                print(f"Decision Tree scoring failed, falling back to rule-based: {str(e)}")
                
        return calculated_score, rule_category

    def load(self) -> bool:
        """Loads a pre-trained Decision Tree model from disk if it exists."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.classifier = pickle.load(f)
                self.is_trained = True
                return True
            except Exception as e:
                print(f"Error loading health classifier model: {str(e)}")
        return False
