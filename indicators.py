import numpy as np


def get_SMA(data, start, end):
    return sum(data[start:end]) / (end - start)


def get_EMA(data, start, end):

    n = end - start
    alpha = 2 / (n + 1)
    weighted_sum = data[start]
    divisor = 1;
    weight = 1 - alpha
    for i in range(start + 1, end):
        weighted_sum += data[i] * weight
        divisor += weight
        weight *= weight

    return weighted_sum / divisor


def get_MACD(data, start, end):
    """start end should be no longer than max length of data"""
    short_term_EMA = []
    long_term_EMA = []
    signal_line = []
    macd = []

    short_term_length = 12
    long_term_length = 26
    signal_line_length = 9

    for i in range(start, end):
        if i + long_term_length < end:
            short_term_EMA.append(get_EMA(data, i, i + short_term_length))
            long_term_EMA.append(get_EMA(data, i, i + long_term_length))
            macd.append(long_term_EMA[i] - short_term_EMA[i])

    for i in range(0, len(macd)):
        if i + signal_line_length < len(macd):
            signal_line.append(get_EMA(macd, i, i + signal_line_length))

    return short_term_EMA, long_term_EMA, signal_line, macd


def get_low(lower, start, end):
    return min(lower[start:end])


def get_high(higher, start, end):
    return max(higher[start:end])


def get_K_stochastic(lower, higher, closing, length, end):
    """length should be 5 or 20"""
    minLower = get_low(lower, end - length, end)
    maxHigher = get_high(higher, end - length, end)
    stochastic = []
    for i in range(end - length, end):
        k = 100 * (closing[i] - minLower) / ((maxHigher - minLower) + 1)
        stochastic.append(k)

    return stochastic


def get_D_of_K_stochastic(k_stochastic, end, length):
    return get_EMA(k_stochastic, end - length, end)


def std_dev(data, start, end):
    return np.std(data[start:end])


def get_bollinger_bands(data, length, end, q):
    """length is typically 20 and q 2
    https://en.wikipedia.org/wiki/Bollinger_Bands
    """
    deviation = std_dev(data, end - length, end)
    ema = get_EMA(data, end - length, end)
    upper_band = ema + q * deviation
    lower_band = ema - q * deviation

    return lower_band, ema, upper_band


def get_keltner_channel(lower, upper, close, length, end):
    """length is typically 10
    https://en.wikipedia.org/wiki/Keltner_channel
    """
    concatenated_list = [lower[end - length:end], upper[end - length:end], close[end - length:end]]
    keltner_channel_list = [(x + y + z) / 3 for x, y, z in zip(*concatenated_list)]
    keltner_channel = get_SMA(keltner_channel_list, end - length, end)

    concatenated_list = [lower[end - length:end], upper[end - length:end]]
    distance_list = [abs(x - y) for x, y in zip(*concatenated_list)]
    distance = get_SMA(distance_list, end - length, end)

    return keltner_channel, distance








