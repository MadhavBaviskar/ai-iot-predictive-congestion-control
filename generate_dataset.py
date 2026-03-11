import csv
import random
import os

NUM_SAMPLES = 5000
TARGET_PER_CLASS = NUM_SAMPLES // 2

data = []

count_congestion = 0
count_no_congestion = 0


while len(data) < NUM_SAMPLES:

    # ---- Network Telemetry (IoT Node) ----

    queue_load = random.uniform(0, 100)

    queue_growth_rate = random.uniform(-5, 20)

    link_utilization = random.uniform(0.1, 1.0)



    # ---- Sender Metrics ----

    base_rtt = random.uniform(30, 50)

    rtt_variation = queue_load * random.uniform(0.2, 0.6)

    RTT = base_rtt + rtt_variation


    RTT_trend = queue_growth_rate * random.uniform(0.5, 1.5)


    packet_loss_rate = max(
        0,
        (queue_load - 80) / 100 + random.uniform(0, 0.02)
    )


    throughput = max(
        0.5,
        (1 - link_utilization + random.uniform(-0.1, 0.1)) * 10
    )



    # ---- Determine Congestion Score ----

    congestion_score = (
        0.25 * (queue_load / 100) +
        0.25 * max(queue_growth_rate, 0) / 20 +
        0.25 * link_utilization +
        0.15 * max(RTT_trend, 0) / 20 +
        0.10 * packet_loss_rate
    )



    # ---- Assign Label ----

    congestion_label = 1 if congestion_score > 0.55 else 0



    # ---- Balance Dataset ----

    if congestion_label == 1 and count_congestion < TARGET_PER_CLASS:

        time_to_congestion = random.uniform(0, 3)

        count_congestion += 1

    elif congestion_label == 0 and count_no_congestion < TARGET_PER_CLASS:

        time_to_congestion = random.uniform(4, 15)

        count_no_congestion += 1

    else:
        continue



    data.append([
        RTT,
        RTT_trend,
        packet_loss_rate,
        throughput,
        queue_load,
        queue_growth_rate,
        link_utilization,
        congestion_label,
        time_to_congestion
    ])



# ---- Save Dataset ----

file_path = os.path.abspath("network_dataset.csv")

with open(file_path, "w", newline="") as f:

    writer = csv.writer(f)

    writer.writerow([
        "RTT",
        "RTT_trend",
        "packet_loss_rate",
        "throughput",
        "queue_load",
        "queue_growth_rate",
        "link_utilization",
        "congestion_label",
        "time_to_congestion"
    ])

    writer.writerows(data)


print("Dataset generated successfully!")
print("Total Samples:", len(data))
print("Congestion:", count_congestion)
print("No Congestion:", count_no_congestion)
print("Saved at:", file_path)