import numpy as np
import pandas as pd
import os
from indicators import get_SMA,get_EMA,get_MACD,get_K_stochastic,get_D_of_K_stochastic, std_dev, get_bollinger_bands, get_keltner_channel

DATA_STOCK = r"C:\Users\aleks\Desktop\doto_munink\apple_stock.csv"

def load_data(path : str):
    data = pd.read_csv(path, index_col=0)
    return data

def SMA_test ():
    data = load_data(DATA_STOCK)
    SMA = get_SMA(data["close"].tolist(),0,data["close"].shape[0])
    print(SMA)

SMA_test()

def EMA_test():
    data = load_data(DATA_STOCK)
    EMA = get_EMA(data["close"].tolist(),0,data["close"].shape[0])
    print(EMA)

EMA_test()

def MACD_test():
    data = load_data(DATA_STOCK)
    MACD = get_MACD(data["close"].tolist(),0,data["close"].shape[0])
    print(MACD[0])
    print(MACD[1])
    print(MACD[2])

MACD_test()

def K_stochastic_test():
    data = load_data(DATA_STOCK)
    K = get_K_stochastic(data["low"],data["high"],data["close"],20,20)
    D_of_K = get_D_of_K_stochastic(K,len(K),len(K))
    print(K)
    print(D_of_K)

K_stochastic_test()

def std_dev_test():
    data = load_data(DATA_STOCK)
    std = std_dev(data["close"],0,data["close"].shape[0])
    print(std)

std_dev_test()

def bollinger_bands_test():
    data = load_data(DATA_STOCK)
    bollinger_band = get_bollinger_bands(data["close"], 20, 20, 2)
    print(bollinger_band)

bollinger_bands_test()

def keltner_channel_test():
    data = load_data(DATA_STOCK)
    keltner_channel = get_keltner_channel(data["low"], data["high"], data["close"], 10, 10)
    print(keltner_channel[0])
    print(keltner_channel[1])

keltner_channel_test()