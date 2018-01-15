from data_processing import preprocess_data
from data_labeling import label_matrix, get_code
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = r"apple7years.csv"
COLUMNS = ["MACD_SELL", "MACD_BUY", "EMA(C)", "EMA(V)",
           "K_SELL", "K_BUY", "BB_BUY", "BB_SELL", "ACTION"]
TARGETS = ["BUY", "SELL", "NEUTRAL"]


def main(data_path, test_size):
    matrix = preprocess_data(data_path)
    label_matrix(matrix)
    data_frame = pd.DataFrame(matrix, columns=COLUMNS)
    df_train = data_frame.iloc[test_size:, :]
    df_test = data_frame.iloc[:test_size, :]
    features = list(df_train.columns[:7])
    y = df_train["ACTION"]
    x = df_train[features]
    dt = DecisionTreeClassifier(min_samples_split=25, random_state=99, criterion="entropy")
    dt.fit(x, y)
    get_code(dt, features, TARGETS)
    y_test = df_test["ACTION"]
    x_test = df_test[features]
    return dt.score(x_test, y_test)

def main_loop():
    end = False
    while end == False:
        path = input('please type in the dataset path:')
        test_size = int(input('please type in the test dataset size'))
        result = main(path,test_size)
        print(result)
        finish = input('if you want to quit press "q"')
        if finish == "q":
            end = True;

if __name__ == "__main__":
    main_loop()


