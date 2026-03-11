import matplotlib.pyplot as plt

from network_state_simulator import NetworkStateSimulator
from sender import Sender


class NetworkSimulator:

    def __init__(self):

        # initialize network
        self.network = NetworkStateSimulator()

        # initialize sender
        self.sender = Sender(self.network)

        # simulation parameters
        self.time_step = 0.1
        self.simulation_duration = 40

        # logging storage
        self.metrics = {
            "time": [],
            "cwnd": [],
            "RTT": [],
            "queue_load": [],
            "throughput": [],
            "sender_rate": [],
            "congestion_probability": [],
            "score": []
        }


    def log_metrics(self, current_time, data):

        self.metrics["time"].append(current_time)
        self.metrics["cwnd"].append(data["cwnd"])
        self.metrics["RTT"].append(data["RTT"])
        self.metrics["queue_load"].append(data["queue_load"])
        self.metrics["throughput"].append(data["throughput"])
        self.metrics["sender_rate"].append(data["sender_rate"])
        self.metrics["congestion_probability"].append(data["congestion_probability"])
        self.metrics["score"].append(data["congestion_score"])


    def print_live_status(self, current_time, data):

        print(
            f"{current_time:5.1f} | "
            f"cwnd={data['cwnd']:.2f} | "
            f"rate={data['sender_rate']:.2f} | "
            f"RTT={data['RTT']:.2f} | "
            f"queue={data['queue_load']:.2f} | "
            f"P={data['congestion_probability']:.2f} | "
            f"score={data['congestion_score']:.2f}"
        )


    def generate_graphs(self):

        time_axis = self.metrics["time"]

        fig, axes = plt.subplots(4, 2, figsize=(14, 12))

        # 1️⃣ Congestion Window
        axes[0,0].plot(time_axis, self.metrics["cwnd"])
        axes[0,0].set_title("Congestion Window vs Time")
        axes[0,0].set_xlabel("Time")
        axes[0,0].set_ylabel("cwnd")

        # 2️⃣ RTT
        axes[0,1].plot(time_axis, self.metrics["RTT"])
        axes[0,1].set_title("RTT vs Time")
        axes[0,1].set_xlabel("Time")
        axes[0,1].set_ylabel("RTT")

        # 3️⃣ Queue Load
        axes[1,0].plot(time_axis, self.metrics["queue_load"])
        axes[1,0].set_title("Queue Load vs Time")
        axes[1,0].set_xlabel("Time")
        axes[1,0].set_ylabel("Queue Load")

        # 4️⃣ Sender Rate
        axes[1,1].plot(time_axis, self.metrics["sender_rate"])
        axes[1,1].set_title("Sender Rate vs Time")
        axes[1,1].set_xlabel("Time")
        axes[1,1].set_ylabel("Rate")

        # 5️⃣ ML Probability
        axes[2,0].plot(time_axis, self.metrics["congestion_probability"])
        axes[2,0].set_title("ML Congestion Probability vs Time")
        axes[2,0].set_xlabel("Time")
        axes[2,0].set_ylabel("Probability")

        # 6️⃣ Controller Score
        axes[2,1].plot(time_axis, self.metrics["score"])
        axes[2,1].set_title("Congestion Score vs Time")
        axes[2,1].set_xlabel("Time")
        axes[2,1].set_ylabel("Score")

        # 7️⃣ Throughput
        axes[3,0].plot(time_axis, self.metrics["throughput"])
        axes[3,0].set_title("Throughput vs Time")
        axes[3,0].set_xlabel("Time")
        axes[3,0].set_ylabel("Throughput")

        # 8️⃣ Phase Diagram (Queue vs cwnd)
        axes[3,1].plot(self.metrics["queue_load"], self.metrics["cwnd"], alpha=0.7)

        # mark starting point
        axes[3,1].scatter(
            self.metrics["queue_load"][0],
            self.metrics["cwnd"][0],
            color="green",
            label="Start"
        )

        # mark final point
        axes[3,1].scatter(
            self.metrics["queue_load"][-1],
            self.metrics["cwnd"][-1],
            color="red",
            label="End"
        )

        axes[3,1].set_title("Phase Diagram: cwnd vs Queue Load")
        axes[3,1].set_xlabel("Queue Load")
        axes[3,1].set_ylabel("cwnd")
        axes[3,1].legend()

        plt.tight_layout()
        plt.show()


    def run(self):

        current_time = 0

        print("\nStarting Network Simulation\n")

        while current_time < self.simulation_duration:

            # run sender iteration
            data = self.sender.run_iteration()

            # log metrics
            self.log_metrics(current_time, data)

            # live output
            self.print_live_status(current_time, data)

            # advance time
            current_time = round(current_time + self.time_step, 2)

        print("\nSimulation Finished\n")

        # generate graphs
        self.generate_graphs()


if __name__ == "__main__":

    simulator = NetworkSimulator()
    simulator.run()