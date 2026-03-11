import random


class NetworkStateSimulator:

    def __init__(self):

        # LINK PARAMETERS
        self.link_capacity = 45      # reduced so congestion can occur
        self.buffer_size = 200

        # NETWORK STATE
        self.queue_load = 10
        self.sender_rate = 10
        self.incoming_rate = 0

        # PREVIOUS METRICS (for smoothing)
        self.prev_RTT = 40
        self.prev_throughput = 8


    def update_network_state(self):

        time_step = 0.1

        # background traffic (IoT / other flows)
        cross_traffic = random.uniform(5, 25)

        # total incoming traffic
        self.incoming_rate = self.sender_rate + cross_traffic

        # packets entering router
        incoming_packets = self.incoming_rate * time_step

        # packets router can send
        service_packets = self.link_capacity * time_step

        # queue update
        self.queue_load += (incoming_packets - service_packets) * 1.0     

        # queue cannot go negative
        if self.queue_load < 0:
            self.queue_load = 0

        # buffer overflow → drop packets
        if self.queue_load > self.buffer_size:
            overflow = self.queue_load - self.buffer_size
            self.queue_load = self.buffer_size


    def set_sender_rate(self, rate):

        self.sender_rate = rate


    def get_sender_metrics(self):

        base_rtt = 40

        # ---------- RTT MODEL ----------
        queue_delay = (self.queue_load / self.buffer_size) * 120
        RTT = base_rtt + queue_delay

        # smooth RTT
        RTT = 0.7 * RTT + 0.3 * self.prev_RTT

        RTT_trend = RTT - self.prev_RTT

        self.prev_RTT = RTT


        # ---------- PACKET LOSS MODEL ----------
        if self.queue_load >= self.buffer_size:
            packet_loss = random.uniform(0.08, 0.2)

        elif self.queue_load > 0.75 * self.buffer_size:
            packet_loss = random.uniform(0.02, 0.08)

        elif self.queue_load > 0.5 * self.buffer_size:
            packet_loss = random.uniform(0.005, 0.02)

        else:
            packet_loss = random.uniform(0, 0.005)


        # ---------- THROUGHPUT MODEL ----------
        successful_rate = self.sender_rate * (1 - packet_loss)

        throughput = min(successful_rate, self.link_capacity)

        # smooth throughput
        throughput = 0.6 * throughput + 0.4 * self.prev_throughput

        self.prev_throughput = throughput


        return RTT, RTT_trend, packet_loss, throughput


    def get_iot_metrics(self):

        # queue load returned raw (sender normalizes it)
        queue_load = self.queue_load

        # queue growth estimation
        queue_growth_rate = (self.incoming_rate - self.link_capacity) * 0.2
        queue_growth_rate = max(-5, min(queue_growth_rate, 20))

        # link utilization
        link_utilization = min(
            1.0,
            self.incoming_rate / self.link_capacity
        )

        return queue_load, queue_growth_rate, link_utilization