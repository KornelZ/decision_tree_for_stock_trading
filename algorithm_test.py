from main import main, get_frame
import os
import pandas as pd
from timeit import default_timer as timer

COLUMNS = ["TRAINING SET", "TRAINING SET SIZE", "TESTING SET", "TESTING SET SIZE",
           "RESULT", "COMPUTATION TIME"]

def dataset_test():
    directory_path = "datasets"
    paths = os.listdir(directory_path)
    result_list = []
    for train_dataset in paths:
        for test_dataset in paths:
            train_frame = get_frame(directory_path + "\\" + train_dataset)
            test_frame = get_frame(directory_path + "\\" + test_dataset)
            start = timer()
            train_length = train_frame.shape[0]
            test_length = test_frame.shape[0]
            labels, result = main(train_frame, int(0.2 * train_length), test_frame, int(0.8 * test_length), False)
            end = timer()

            result_row = [train_dataset, str(int(train_length * 0.2)),
                          test_dataset, str(int(test_length * 0.8)),
                          str(result), str(end - start)]
            result_list.append(result_row)
    result_frame = pd.DataFrame(result_list, columns=COLUMNS)
    result_frame.to_csv("Tests_results.csv")


dataset_test()