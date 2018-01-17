from data_processing import preprocess_data
from data_labeling import label_matrix, get_code
import pandas as pd
from sklearn.tree import DecisionTreeClassifier

DATA_PATH = r"apple7years.csv"
COLUMNS = ["MACD_SELL", "MACD_BUY", "EMA(C)", "EMA(V)",
           "K_SELL", "K_BUY", "BB_BUY", "BB_SELL", "ACTION"]
TARGETS = ["BUY", "SELL", "NEUTRAL"]


def get_frame(path):
    matrix = preprocess_data(path)
    label_matrix(matrix)
    return pd.DataFrame(matrix, columns=COLUMNS)


def train(train_frame, features):
    y = train_frame["ACTION"]
    x = train_frame[features]
    dt = DecisionTreeClassifier(min_samples_split=100, random_state=99, criterion="entropy")
    dt.fit(x, y)
    return dt


def classify(test_frame, features, dt: DecisionTreeClassifier):
    y_test = test_frame["ACTION"]
    x_test = test_frame[features]
    return dt.score(x_test, y_test)


def main(train_path, train_size, test_path, test_size, display_tree=True):
    train_frame = get_frame(train_path)
    df_train = train_frame.tail(train_size)
    test_frame = get_frame(test_path)
    df_test = test_frame.head(test_size)
    features = list(df_train.columns[:7])

    dt = train(df_train, features)

    if display_tree:
        get_code(dt, features, TARGETS)

    return classify(df_test, features, dt)


def main_loop():
    end = False
    while not end:
        try:
            train_path = input('please type in the training dataset path:')
            train_size = int(input('please type in the training dataset size (last n rows)'))
            test_path = input('please type in the test dataset path:')
            test_size = int(input('please type in the test dataset size (first n rows)'))
            result = main(train_path, train_size, test_path, test_size)
        except:
            print("Invalid input")
            continue

        print(result)
        finish = input('if you want to quit press "q"')
        if finish == "q":
            end = True;


if __name__ == "__main__":
    main_loop()


