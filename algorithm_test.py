from main import main, get_frame
import os
from timeit import default_timer as timer

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
            labels, result= main(train_frame, int(0.2 * train_length), test_frame, int(0.8 * test_length), False)
            end = timer()
            result_list.append("TRAIN: " + train_dataset + " el. count = " + str(int(train_length * 0.2)) + \
                                " TEST: " + test_dataset + " el. count = " + str(int(test_length * 0.8)) + \
                                " RESULT: " + str(result) + " time of computation: " + str(end - start))
    with open ("Tests_results.txt", "w") as result_file:
        for results in result_list:
            result_file.write(results + "\n")



dataset_test()