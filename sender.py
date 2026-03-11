from ml_decision_engine import MLDecisionEngine
from congestion_controller import CongestionController
from iot_monitor import IoTMonitor


class Sender:

    def __init__(self, network):

        self.network = network

        self.iot_monitor = IoTMonitor(network)

        self.ml_engine = MLDecisionEngine()

        self.controller = CongestionController()

        self.cwnd = 10

        self.rate_scale = 1.0


    def build_feature_vector(self, sender_metrics, telemetry):

        RTT, RTT_trend, packet_loss, throughput = sender_metrics

        queue_load = telemetry["queue_load"]
        queue_growth_rate = telemetry["queue_growth_rate"]
        link_utilization = telemetry["link_utilization"]

        # Normalize queue load to match dataset range (0–100)
        buffer_size = self.network.buffer_size
        queue_percent = (queue_load / buffer_size) * 100

        features = [
            RTT,
            RTT_trend,
            packet_loss,
            throughput,
            queue_percent,
            queue_growth_rate,
            link_utilization
        ]

        return features

    def cwnd_to_rate(self):

        return self.cwnd * self.rate_scale


    def run_iteration(self):

        self.network.update_network_state()

        sender_metrics = self.network.get_sender_metrics()

        telemetry = self.iot_monitor.get_telemetry()

        features = self.build_feature_vector(sender_metrics, telemetry)

        P, T = self.ml_engine.predict(features)

        new_cwnd, score = self.controller.update_cwnd(self.cwnd, P, T)

        self.cwnd = new_cwnd

        sender_rate = self.cwnd_to_rate()

        self.network.set_sender_rate(sender_rate)

        RTT, _, packet_loss, throughput = sender_metrics

        return {
            "cwnd": self.cwnd,
            "sender_rate": sender_rate,
            "RTT": RTT,
            "packet_loss": packet_loss,
            "throughput": throughput,
            "queue_load": telemetry["queue_load"],
            "congestion_probability": P,
            "time_to_congestion": T,
            "congestion_score": score
        }