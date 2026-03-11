class CongestionController:

    def update_cwnd(self, cwnd, P, T):

        # congestion score
        score = (0.6 * P) + (0.4 * (1 / (T + 1)))

        # severe congestion
        if score > 0.12:
            cwnd = max(5, cwnd * 0.7)

        # moderate congestion → gradual decrease
        elif score > 0.09:
            cwnd = max(5, cwnd - 1.0)

        # safe region → increase
        else:
            cwnd = cwnd + 0.6

        # upper bound
        cwnd = min(cwnd, 40)

        return cwnd, score