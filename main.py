from data_processing import preprocess_data
from data_labeling import label_matrix, get_code
from pandas import DataFrame
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = r"apple_stock.csv"
COLUMNS = ["MACD_SELL", "MACD_BUY", "EMA(C)", "EMA(V)",
          "K_SELL", "K_BUY", "BB_BUY", "BB_SELL", "ACTION"]
TARGETS = ["BUY", "SELL", "NEUTRAL"]
def main():
    matrix = preprocess_data(DATA_PATH)
    label_matrix(matrix)
    data_frame = DataFrame(matrix, columns=COLUMNS)
    features = list(data_frame.columns[:7])
    y = data_frame["ACTION"]
    x = data_frame[features]

    dt = DecisionTreeClassifier(min_samples_split=4, random_state=99)
    dt.fit(x, y)
    get_code(dt, features, TARGETS)

if __name__ == "__main__":
    main()


