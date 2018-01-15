import numpy as np

SELL = "S"
BUY = "B"
NEUTRAL = "N"

def label_matrix(attribute_matrix):
    for i in range(len(attribute_matrix)):
        label = label_row(attribute_matrix[i])
        attribute_matrix[i].append(label)

def label_row(row):
    buy_signal = 0
    sell_signal = 0
    if row[0] == 1:
        sell_signal += 1
    if row[1] == 1:
        buy_signal += 1
    if row[4] == 1:
        sell_signal += 1
    if row[5] == 1:
        buy_signal += 1
    if row[6] == 1 and row[7] == 0:
        sell_signal += 1
    if row[6] == 0 and row[7] == 1:
        buy_signal += 1

    if sell_signal == buy_signal:
        return NEUTRAL
    elif sell_signal > buy_signal:
        return SELL
    else:
        return BUY

def get_code(tree, feature_names, target_names,
             spacer_base="    "):
    """Produce psuedo-code for decision tree.

    Args
    ----
    tree -- scikit-leant DescisionTree.
    feature_names -- list of feature names.
    target_names -- list of target (class) names.
    spacer_base -- used for spacing code (default: "    ").

    Notes
    -----
    based on http://stackoverflow.com/a/30104792.
    """
    left      = tree.tree_.children_left
    right     = tree.tree_.children_right
    threshold = tree.tree_.threshold
    features  = [feature_names[i] for i in tree.tree_.feature]
    value = tree.tree_.value

    def recurse(left, right, threshold, features, node, depth):
        spacer = spacer_base * depth
        if (threshold[node] != -2):
            print(spacer + "if ( " + features[node] + " <= " + \
                  str(threshold[node]) + " ) {")
            if left[node] != -1:
                    recurse(left, right, threshold, features,
                            left[node], depth+1)
            print(spacer + "}\n" + spacer +"else {")
            if right[node] != -1:
                    recurse(left, right, threshold, features,
                            right[node], depth+1)
            print(spacer + "}")
        else:
            target = value[node]
            for i, v in zip(np.nonzero(target)[1],
                            target[np.nonzero(target)]):
                target_name = target_names[i]
                target_count = int(v)
                print(spacer + "return " + str(target_name) + \
                      " ( " + str(target_count) + " examples )")

    recurse(left, right, threshold, features, 0, 0)
