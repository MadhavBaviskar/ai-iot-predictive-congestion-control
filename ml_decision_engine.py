import joblib
import numpy as np
import pandas as pd


class MLDecisionEngine:

    def __init__(self):

        # load trained models
        self.classifier = joblib.load("congestion_classifier.pkl")
        self.regressor = joblib.load("time_regressor.pkl")

        self.feature_names = [
            "RTT",
            "RTT_trend",
            "packet_loss_rate",
            "throughput",
            "queue_load",
            "queue_growth_rate",
            "link_utilization"
        ]

    def predict(self, feature_vector):

        if len(feature_vector) != 7:
            raise ValueError("Feature vector must contain 7 elements")

        # convert to DataFrame with feature names
        features = pd.DataFrame([feature_vector], columns=self.feature_names)

        # classifier prediction
        probabilities = self.classifier.predict_proba(features)

        congestion_probability = probabilities[0][1]

        # regression prediction
        time_to_congestion = self.regressor.predict(features)[0]

        # stability safeguards
        congestion_probability = np.clip(congestion_probability, 0.001, 0.999)
        time_to_congestion = max(0.1, time_to_congestion)

        return congestion_probability, time_to_congestion