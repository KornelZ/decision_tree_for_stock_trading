import pandas as pd
from indicators_test import load_data, DATA_STOCK
from indicators import get_MACD, get_K_stochastic, get_D_of_K_stochastic, get_bollinger_bands
from attribute_binarization import Binarizer

K_STOCHASTIC_INTERVAL = 20
BOLLINGER_Q = 2

data = load_data(DATA_STOCK)
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
    d_of_k_list.append(get_D_of_K_stochastic(k_stochastic_list[j], K_STOCHASTIC_INTERVAL, K_STOCHASTIC_INTERVAL))
    bollinger_band_list.append(get_bollinger_bands(data["close"].tolist(), K_STOCHASTIC_INTERVAL, \
                                               i + K_STOCHASTIC_INTERVAL, BOLLINGER_Q))
    i = i + K_STOCHASTIC_INTERVAL
    j += 1

print("MACD " + str(macd_list))
print("VOLUME EMA " + str(volume_ema_list))
print("K_STOCHASTIC " + str(k_stochastic_list))
print("D OF K_STOCHASTIC " + str(d_of_k_list))
print("BOLLINGER " + str(bollinger_band_list))

binarizer = Binarizer()
bin_macd = []
for i in range(len(macd_list[2])):
    bin_macd.append(binarizer.bin_macd(macd_list[3][i], macd_list[2][i]))
print(bin_macd)
bin_close_ema = []
for i in range(len(macd_list[0])):
    bin_close_ema.append(binarizer.bin_ema(macd_list[0][i], macd_list[1][i]))
bin_volume_ema = []
for i in range(len(volume_ema_list[0])):
    bin_volume_ema.append(binarizer.bin_ema(volume_ema_list[0][i], volume_ema_list[1][i]))
