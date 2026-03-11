from ml_decision_engine import MLDecisionEngine

engine = MLDecisionEngine()

print("\nML Sanity Test\n")

test_cases = [

    # Low congestion
    [40, -2, 0.0, 8, 20, -1, 0.2],

    # Medium congestion
    [70, 6, 0.02, 4, 65, 7, 0.75],

    # High congestion
    [90, 10, 0.05, 2, 90, 12, 0.95]

]

labels = [
    "LOW CONGESTION CASE",
    "MEDIUM CONGESTION CASE",
    "HIGH CONGESTION CASE"
]

for label, features in zip(labels, test_cases):

    P, T = engine.predict(features)

    print(label)
    print("features:", features)
    print("Predicted congestion probability:", round(P,3))
    print("Predicted time to congestion:", round(T,3))
    print("-"*40)