from ml_decision_engine import MLDecisionEngine

# initialize ML engine
engine = MLDecisionEngine()

# example network state
feature_vector = [
    60,     # RTT
    5,      # RTT trend
    0.01,   # packet loss
    4,    # throughput
    60,     # queue load
    6,     # queue growth
    0.7    # link utilization
]

# run prediction
probability, time_to_congestion = engine.predict(feature_vector)

print("Predicted congestion probability:", probability)
print("Predicted time to congestion:", time_to_congestion)