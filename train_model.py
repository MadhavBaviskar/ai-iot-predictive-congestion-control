import pandas as pd
import matplotlib.pyplot as plt
import joblib

from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier, RandomForestRegressor
from sklearn.metrics import accuracy_score, classification_report, mean_absolute_error


# -----------------------------------
# 1 Load Dataset
# -----------------------------------

data = pd.read_csv("network_dataset.csv")

print("\nDataset Loaded")
print("Shape:", data.shape)


# -----------------------------------
# 2 Define Features and Targets
# -----------------------------------

features = [
    "RTT",
    "RTT_trend",
    "packet_loss_rate",
    "throughput",
    "queue_load",
    "queue_growth_rate",
    "link_utilization"
]

X = data[features]

y_class = data["congestion_label"]

y_reg = data["time_to_congestion"]


# -----------------------------------
# 3 Train-Test Split
# -----------------------------------

X_train, X_test, y_class_train, y_class_test = train_test_split(
    X, y_class, test_size=0.2, random_state=42
)

_, _, y_reg_train, y_reg_test = train_test_split(
    X, y_reg, test_size=0.2, random_state=42
)

print("\nTraining samples:", len(X_train))
print("Testing samples:", len(X_test))


# -----------------------------------
# 4 Train Congestion Classifier
# -----------------------------------

classifier = RandomForestClassifier(
    n_estimators=150,
    max_depth=12,
    random_state=42
)

classifier.fit(X_train, y_class_train)

print("\nCongestion Classifier Trained")


# -----------------------------------
# 5 Evaluate Classifier
# -----------------------------------

y_pred = classifier.predict(X_test)

accuracy = accuracy_score(y_class_test, y_pred)

print("\nClassifier Accuracy:", accuracy)

print("\nClassification Report:")

print(classification_report(y_class_test, y_pred))


# -----------------------------------
# 6 Train Time-to-Congestion Regressor
# -----------------------------------

regressor = RandomForestRegressor(
    n_estimators=150,
    max_depth=12,
    random_state=42
)

regressor.fit(X_train, y_reg_train)

print("\nTime-to-Congestion Regressor Trained")


# -----------------------------------
# 7 Evaluate Regressor
# -----------------------------------

y_pred_reg = regressor.predict(X_test)

mae = mean_absolute_error(y_reg_test, y_pred_reg)

print("\nRegression Mean Absolute Error:", mae)


# -----------------------------------
# 8 Save Models
# -----------------------------------

joblib.dump(classifier, "congestion_classifier.pkl")

joblib.dump(regressor, "time_regressor.pkl")

print("\nModels saved successfully")


# -----------------------------------
# 9 Feature Importance (VERY IMPORTANT)
# -----------------------------------

importances = classifier.feature_importances_

feature_importance_df = pd.DataFrame({
    "feature": features,
    "importance": importances
})

feature_importance_df = feature_importance_df.sort_values(
    by="importance",
    ascending=False
)

print("\nFeature Importance Ranking:\n")

print(feature_importance_df)


# -----------------------------------
# 10 Plot Feature Importance
# -----------------------------------

plt.figure(figsize=(8,5))

plt.barh(
    feature_importance_df["feature"],
    feature_importance_df["importance"]
)

plt.gca().invert_yaxis()

plt.title("Feature Importance for Congestion Prediction")

plt.xlabel("Importance Score")

plt.tight_layout()

plt.show()


print("\nTraining Pipeline Completed Successfully")