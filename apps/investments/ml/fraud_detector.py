import pickle
import numpy as np
import os


class FraudDetector:
    def __init__(self):
        model_path = os.path.join(os.path.dirname(__file__), "./fraud_model.pkl")

        with open(model_path, "rb") as f:
            self.model = pickle.load(f)

    def predict(self, amount, currency, tx_type):
        is_crypto = int(currency.code in ["BTC", "ETH", "USDT"])
        tx_type_map = {"purchase": 0, "withdrawal": 1}
        input_vec = np.array([[float(amount), is_crypto, tx_type_map.get(tx_type, 0)]])
        prediction = self.model.predict(input_vec)

        return prediction[0] == 1
