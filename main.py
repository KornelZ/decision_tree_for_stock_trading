from data_processing import preprocess_data
from data_labeling import label_matrix, get_code
import pandas as pd
from sklearn.tree import DecisionTreeClassifier
from sklearn.metrics import accuracy_score

DATA_PATH = r"./datasets/Apple10years.csv"
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


def classify(test_frame, features, dt):
    y_test = test_frame["ACTION"]
    x_test = test_frame[features]
    prediction = dt.predict(x_test)
    return prediction, accuracy_score(y_test,prediction)


def main(train_frame, train_size, test_frame, test_size, display_tree=True):
    df_train = train_frame.tail(train_size)
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
            train_path = raw_input('please type in the training dataset path:')
            train_size = int(raw_input('please type in the training dataset size (last n rows)'))
            test_path = raw_input('please type in the test dataset path:')
            test_size = int(raw_input('please type in the test dataset size (first n rows)'))
            train_frame = get_frame(train_path)
            test_frame = get_frame(test_path)
            decision_tree = raw_input('if you want to see the decision tree press "d"')
            if decision_tree == "d":
                display_tree = True
            else:
                display_tree = False
            labels, result = main(train_frame, train_size, test_frame, test_size, display_tree)

        except:
            print("Invalid input")
            continue
        show_results(labels, test_frame)
        print("Accuracy " + str(result))
        finish = raw_input('if you want to quit press "q"')
        if finish == "q":
            end = True;

def show_results(labels, data_frame):
    show_daily_result = raw_input('if you want to save the results press "s"')
    if show_daily_result == "s":
        result_frame = pd.DataFrame(data_frame)
        result_frame["PREDICTED ACTION"] = pd.Series(labels)
        result_frame.to_csv("results.csv")
        #with open("results.txt", "w") as result_file:
         #   for i in range(data_frame.shape[0]):
          #      if (i < len(labels)):
           #         result_file.write(str(data_frame.iloc[[i]]) + " PREDICTED ACTION: " + str(labels[i]) + "\n")

if __name__ == "__main__":
    main_loop()


