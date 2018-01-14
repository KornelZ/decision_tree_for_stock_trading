

class Binarizer:

    def __init__(self):
        self.bollinger_lower_range = 0.95
        self.bollinger_upper_range = 1.05
        self.price_range = 0.01

    def bin_macd(self, macd, signal_line):
        if macd < signal_line:
            return 1, 0
        elif macd > signal_line:
            return 0, 1
        else:
            return 0, 0

    def bin_ema(self, short_term, long_term):
        if short_term > long_term:
            return 1
        return 0

    def bin_k_stochastic(self, k_stochastic, d_of_k, prev_d):
        #rising
        if d_of_k > prev_d and k_stochastic > d_of_k:
            return 0, 1
        elif d_of_k < prev_d and k_stochastic > d_of_k:
            return 1, 0
        else:
            return 0, 0

    def bin_bollinger(self, lower_band, upper_band, price):
        asset_ranking = 0
        if lower_band > self.bollinger_lower_range * price \
           and upper_band < self.bollinger_upper_range * price:
            asset_ranking = 1

        time_to_buy = 0
        if lower_band > (1.0 - self.price_range) * price:
            time_to_buy = 1

        return asset_ranking, time_to_buy
