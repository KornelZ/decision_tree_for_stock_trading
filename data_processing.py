from indicators_test import load_data
from indicators import get_MACD, get_K_stochastic, get_D_of_K_stochastic, get_bollinger_bands
from attribute_binarization import Binarizer



K_STOCHASTIC_INTERVAL = 20
BOLLINGER_Q = 2

def preprocess_data(path : str):

    data = load_data(path)
    macd_list = get_MACD(data["close"].tolist(),0,data["close"].shape[0])
    volume_ema_list = get_MACD(data["volume"].tolist(), 0, data["volume"].shape[0])

    i = 0
    k_stochastic_list = []
    d_of_k_list = []
    bollinger_band_list = []
    j = 0
    while i + K_STOCHASTIC_INTERVAL < data["low"].shape[0]:
        k_stochastic_list.append(get_K_stochastic(data["low"].tolist(), data["high"].tolist(), \
                                                  data["close"].tolist(), K_STOCHASTIC_INTERVAL, i + K_STOCHASTIC_INTERVAL))
        bollinger_band_list.append(get_bollinger_bands(data["close"].tolist(), K_STOCHASTIC_INTERVAL, \
                                                   i + K_STOCHASTIC_INTERVAL, BOLLINGER_Q))
        i = i + K_STOCHASTIC_INTERVAL
        j += 1

    i = 0
    while i + K_STOCHASTIC_INTERVAL < data["low"].shape[0]:
        bollinger_band_list.append(get_bollinger_bands(data["close"].tolist(), K_STOCHASTIC_INTERVAL, \
                                                       i + K_STOCHASTIC_INTERVAL, BOLLINGER_Q))
        i += 1

    combined_k_stochastic = []
    for i in range(len(k_stochastic_list)):
        for j in range(len(k_stochastic_list[i])):
            combined_k_stochastic.append(k_stochastic_list[i][j])

    for i in range(len(combined_k_stochastic) - K_STOCHASTIC_INTERVAL):
        d_of_k_list.append(get_D_of_K_stochastic(combined_k_stochastic, i + K_STOCHASTIC_INTERVAL, K_STOCHASTIC_INTERVAL))

    binarizer = Binarizer()
    bin_macd = []
    for i in range(len(macd_list[2])):
        bin_macd.append(binarizer.bin_macd(macd_list[3][i], macd_list[2][i]))

    bin_close_ema = []
    for i in range(len(macd_list[0])):
        bin_close_ema.append(binarizer.bin_ema(macd_list[0][i], macd_list[1][i]))

    bin_volume_ema = []
    for i in range(len(volume_ema_list[0])):
        bin_volume_ema.append(binarizer.bin_ema(volume_ema_list[0][i], volume_ema_list[1][i]))

    bin_stochastic = []
    for i in range(len(d_of_k_list) - 1):
        bin_stochastic.append(binarizer.bin_k_stochastic(combined_k_stochastic[i], d_of_k_list[i], d_of_k_list[i + 1]))

    bin_bollinger = []
    for i in range(len(bollinger_band_list)):
        bin_bollinger.append(binarizer.bin_bollinger(bollinger_band_list[i][0], bollinger_band_list[i][2], \
                                                     data["close"][i]))
    attribute_matrix = []
    macd_attr = list(map(list, zip(*bin_macd)))
    attribute_matrix.append(macd_attr[0])
    attribute_matrix.append(macd_attr[1])
    attribute_matrix.append(bin_close_ema)
    attribute_matrix.append(bin_volume_ema)
    stochastic_attr = list(map(list, zip(*bin_stochastic)))
    attribute_matrix.append(stochastic_attr[0])
    attribute_matrix.append(stochastic_attr[1])
    bollinger_attr = list(map(list, zip(*bin_bollinger)))
    attribute_matrix.append(bollinger_attr[0])
    attribute_matrix.append(bollinger_attr[1])
    min_length = min(map(len, attribute_matrix))
    for i in range(len(attribute_matrix)):
        print(len(attribute_matrix[i]))

    result_matrix = []
    for i in range(min_length):
        tmp = []
        for j in range(len(attribute_matrix)):
            tmp.append(attribute_matrix[j][i])
        result_matrix.append(tmp)

    return result_matrix

