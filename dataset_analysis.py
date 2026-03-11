import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# -----------------------------
# Load Dataset
# -----------------------------

data = pd.read_csv("network_dataset.csv")

print("\n==============================")
print("DATASET OVERVIEW")
print("==============================")

print("\nDataset Shape (Rows, Columns):")
print(data.shape)

print("\nFirst 5 Rows:")
print(data.head())

print("\nDataset Statistics:")
print(data.describe())


# -----------------------------
# Congestion Label Distribution
# -----------------------------

print("\n==============================")
print("CONGESTION CLASS DISTRIBUTION")
print("==============================")

print(data["congestion_label"].value_counts())

sns.countplot(x="congestion_label", data=data)

plt.title("Congestion Label Distribution")
plt.xlabel("Congestion Label (0 = No Congestion, 1 = Congestion)")
plt.ylabel("Count")

plt.show()


# -----------------------------
# Feature Distribution Analysis
# -----------------------------

print("\n==============================")
print("FEATURE DISTRIBUTIONS")
print("==============================")

features = [
    "RTT",
    "RTT_trend",
    "packet_loss_rate",
    "throughput",
    "queue_load",
    "queue_growth_rate",
    "link_utilization"
]

for feature in features:

    plt.figure(figsize=(7,4))

    sns.histplot(data[feature], bins=40, kde=True)

    plt.title(feature + " Distribution")

    plt.xlabel(feature)

    plt.ylabel("Frequency")

    plt.show()


# -----------------------------
# Correlation Matrix
# -----------------------------

print("\n==============================")
print("FEATURE CORRELATION MATRIX")
print("==============================")

plt.figure(figsize=(10,8))

sns.heatmap(
    data.corr(),
    annot=True,
    cmap="coolwarm",
    fmt=".2f"
)

plt.title("Feature Correlation Heatmap")

plt.show()


print("\nAnalysis Complete!")