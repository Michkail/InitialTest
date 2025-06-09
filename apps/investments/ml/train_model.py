import pickle
from sklearn.ensemble import RandomForestClassifier
import numpy as np


# training data: [amount, is_crypto, tx_type]
X = np.array([[1000, 1, 0],
              [50000, 0, 1],
              [250000, 1, 1],
              [200, 0, 0]])
y = [0, 0, 1, 0]  # 1 = fraud

model = RandomForestClassifier()
model.fit(X, y)

with open("./fraud_model.pkl", "wb") as f:
    pickle.dump(model, f)
