class IoTMonitor:

    def __init__(self, network):

        self.network = network


    def get_telemetry(self):

        queue_load, queue_growth_rate, link_utilization = self.network.get_iot_metrics()

        telemetry = {
            "queue_load": queue_load,
            "queue_growth_rate": queue_growth_rate,
            "link_utilization": link_utilization
        }

        return telemetry