import pickle
import os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import pandas as pd
import numpy as np

class HitPredictor:
    def __init__(self, model_path='data/models/hit_predictor.pkl'):
        self.model = None
        self.scaler = StandardScaler()
        self.model_path = model_path
        self.feature_importance = None
        
        # Try to load pre-trained model
        if os.path.exists(model_path):
            self.load_model()
    
    def train_model(self, X, y, test_size=0.2, random_state=42):
        """Train and evaluate the prediction model"""
        # Convert to numpy if needed
        if isinstance(X, pd.DataFrame):
            X = X.values
        if isinstance(y, pd.Series):
            y = y.values
        
        # Train-test split
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        # Feature scaling
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Initialize and train model
        self.model = RandomForestClassifier(
            n_estimators=100,
            max_depth=10,
            random_state=random_state,
            class_weight='balanced'
        )
        self.model.fit(X_train_scaled, y_train)
        
        # Evaluate
        y_pred = self.model.predict(X_test_scaled)
        print("\nModel Evaluation:")
        print(classification_report(y_test, y_pred))
        
        # Store feature importance
        self.feature_importance = dict(zip(
            range(X.shape[1]), 
            self.model.feature_importances_
        ))
        
        # Save model
        self.save_model()
    
    def predict(self, features):
        """Make prediction for new song features"""
        if not self.model:
            raise ValueError("Model not trained or loaded")
        
        # Ensure features are in correct format
        if isinstance(features, (list, pd.Series)):
            features = np.array(features).reshape(1, -1)
        elif isinstance(features, pd.DataFrame):
            features = features.values
        
        # Scale features
        scaled_features = self.scaler.transform(features)
        
        # Make prediction
        proba = self.model.predict_proba(scaled_features)[0]
        prediction = self.model.predict(scaled_features)[0]
        
        return {
            'prediction': prediction,
            'probability_top_chart': proba[1],
            'confidence': max(proba),
            'feature_importance': self._get_important_features(features)
        }
    
    def save_model(self):
        """Save model and scaler to disk"""
        with open(self.model_path, 'wb') as f:
            pickle.dump({
                'model': self.model,
                'scaler': self.scaler,
                'feature_importance': self.feature_importance
            }, f)
    
    def load_model(self):
        """Load model and scaler from disk"""
        with open(self.model_path, 'rb') as f:
            data = pickle.load(f)
            self.model = data['model']
            self.scaler = data['scaler']
            self.feature_importance = data.get('feature_importance')
    
    def _get_important_features(self, features):
        """Get most influential features for a prediction"""
        if not self.feature_importance:
            return None
        
        # Get indices of top 3 most important features
        top_indices = sorted(
            self.feature_importance.items(),
            key=lambda x: x[1],
            reverse=True
        )[:3]
        
        return [
            (idx, self.feature_importance[idx], features[0][idx])
            for idx, _ in top_indices
        ]