class HitPredictor:
    def __init__(self):
        self.model = RandomForestClassifier()
        self.scaler = StandardScaler()
        self.is_trained = False

    def train_model(self, X, y):
        """Train the prediction model"""
        X_scaled = self.scaler.fit_transform(X)
        self.model.fit(X_scaled, y)
        self.is_trained = True

    def predict(self, features):
        """Predict hit potential for new song"""
        if not self.is_trained:
            raise ValueError("Model must be trained before prediction")
            
        scaled_features = self.scaler.transform([features])
        proba = self.model.predict_proba(scaled_features)[0]
        return {
            'probability_top_chart': proba[1],
            'confidence': max(proba)
        }