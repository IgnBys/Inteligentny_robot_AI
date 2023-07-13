import csv
import os
import random
import pandas as pd #for manipulating the csv data
import numpy as np #for mathematical calculation
import json


def make_variable_tree():
    current_directory = os.getcwd()
    tree_file_path = os.path.join(current_directory, "tree.txt")
    with open(tree_file_path, "r", encoding="utf-8") as f:
        tree_str = f.read()  # Чтение содержимого файла в виде строки
        tree = json.loads(tree_str)
    return tree

def calc_total_entropy(train_data, label, class_list):
    total_row = train_data.shape[0]  # the total size of the dataset
    total_entr = 0

    for c in class_list:  # for each class in the label
        total_class_count = train_data[train_data[label] == c].shape[0]  # number of the class
        if total_class_count != 0:
            total_class_entr = - (total_class_count / total_row) * np.log2(total_class_count / total_row)
        else:
            total_class_entr = 0
        total_entr += total_class_entr  # adding the class entropy to the total entropy of the dataset

    return total_entr


def calc_entropy(feature_value_data, label, class_list):
    class_count = feature_value_data.shape[0]
    entropy = 0

    for c in class_list:
        label_class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # row count of class c
        entropy_class = 0
        if label_class_count != 0:
            probability_class = label_class_count / class_count  # probability of the class
            entropy_class = - probability_class * np.log2(probability_class)  # entropy
        entropy += entropy_class
    return entropy


def calc_info_gain(feature_name, train_data, label, class_list):
    feature_value_list = train_data[feature_name].unique()  # unqiue values of the feature
    total_row = train_data.shape[0]
    feature_info = 0.0

    for feature_value in feature_value_list:
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # filtering rows with that feature_value
        feature_value_count = feature_value_data.shape[0]
        feature_value_entropy = calc_entropy(feature_value_data, label,
                                             class_list)  # calculcating entropy for the feature value
        feature_value_probability = feature_value_count / total_row
        feature_info += feature_value_probability * feature_value_entropy  # calculating information of the feature value

    return calc_total_entropy(train_data, label,
                              class_list) - feature_info  # calculating information gain by subtracting


def find_most_informative_feature(train_data, label, class_list):
    feature_list = train_data.columns.drop(label)  # finding the feature names in the dataset
    # N.B. label is not a feature, so dropping it
    max_info_gain = -1
    max_info_feature = None

    for feature in feature_list:  # for each feature in the dataset
        feature_info_gain = calc_info_gain(feature, train_data, label, class_list)
        if max_info_gain < feature_info_gain:  # selecting feature name with highest information gain
            max_info_gain = feature_info_gain
            max_info_feature = feature

    return max_info_feature


def generate_sub_tree(feature_name, train_data, label, class_list):
    feature_value_count_dict = train_data[feature_name].value_counts(
        sort=False)  # dictionary of the count of unqiue feature value
    tree = {}  # sub tree or node

    for feature_value, count in feature_value_count_dict.items():
        feature_value_data = train_data[
            train_data[feature_name] == feature_value]  # dataset with only feature_name = feature_value

        assigned_to_node = False  # flag for tracking feature_value is pure class or not
        for c in class_list:  # for each class
            class_count = feature_value_data[feature_value_data[label] == c].shape[0]  # count of class c

            if class_count == count:  # count of (feature_value = count) of class (pure class)
                tree[feature_value] = c  # adding node to the tree
                train_data = train_data[train_data[feature_name] != feature_value]  # removing rows with feature_value
                assigned_to_node = True
        if not assigned_to_node:  # not pure class
            tree[feature_value] = "?"  # as feature_value is not a pure class, it should be expanded further,
            # so the branch is marking with ?

    return tree, train_data


def make_tree(root, prev_feature_value, train_data, label, class_list):
    if train_data.shape[0] != 0:  # if dataset becomes enpty after updating
        max_info_feature = find_most_informative_feature(train_data, label, class_list)  # most informative feature
        tree, train_data = generate_sub_tree(max_info_feature, train_data, label,
                                             class_list)  # getting tree node and updated dataset
        next_root = None

        if prev_feature_value != None:  # add to intermediate node of the tree
            root[prev_feature_value] = dict()
            root[prev_feature_value][max_info_feature] = tree
            next_root = root[prev_feature_value][max_info_feature]
        else:  # add to root of the tree
            root[max_info_feature] = tree
            next_root = root[max_info_feature]

        for node, branch in list(next_root.items()):  # iterating the tree node
            if branch == "?":  # if it is expandable
                feature_value_data = train_data[train_data[max_info_feature] == node]  # using the updated dataset
                make_tree(next_root, node, feature_value_data, label, class_list)  # recursive call with updated dataset



def id3(train_data_m, label):
    current_directory = os.getcwd()
    train_data = train_data_m.copy() #getting a copy of the dataset
    tree = {} #tree which will be updated
    class_list = train_data[label].unique() #getting unqiue classes of the label
    make_tree(tree, None, train_data, label, class_list) #start calling recursion
    print(tree)
    tree_file_path = os.path.join(current_directory, "tree.txt")
    with open(tree_file_path, "a", encoding="utf-8") as f:
        f.write(json.dumps(tree))
    return tree


def build_tree_string_reverse(node, level=0):
    indent = " " * level
    tree_string = ""
    for key, value in reversed(list(node.items())):
        if isinstance(value, dict):
            tree_string += f"{indent}{key}:\n"
            tree_string += build_tree_string_reverse(value, level + 2)
        else:
            tree_string += f"{indent}{key}: {value}\n"
    return tree_string


def predict(tree, instance):
    if not isinstance(tree, dict): #if it is leaf node
        return tree #return the value
    else:
        root_node = next(iter(tree)) #getting first key/feature name of the dictionary
        feature_value = instance[root_node] #value of the feature
        if feature_value in tree[root_node]: #checking the feature value in current tree node
            return predict(tree[root_node][feature_value], instance) #goto next feature
        else:
            return None

def evaluate(tree, test_data_m, label):
    correct_preditct = 0
    wrong_preditct = 0
    for index, row in test_data_m.iterrows(): #for each row in the dataset
        result = predict(tree, test_data_m.iloc[index]) #predict the row
        if result == test_data_m[label].iloc[index]: #predicted value and expected value is same or not
            correct_preditct += 1 #increase correct count
        else:
            wrong_preditct += 1 #increase incorrect count
    accuracy = correct_preditct / (correct_preditct + wrong_preditct) #calculating accuracy
    return accuracy

def write_predict_tree(tree, file_path, level=0, indent_size=4):
    with open(file_path, "w", encoding="utf-8") as f:
        write_node(tree, f, level, indent_size)

def write_node(node, file, level, indent_size):
    indent = " " * (level * indent_size)
    for key, value in node.items():
        if isinstance(value, dict):
            file.write(f"{indent}If {key}:\n")
            write_node(value, file, level + 1, indent_size)
        else:
            file.write(f"{indent}Decision: {value}\n")


def answer(levels: list,tree):
    options = ["client", "generator", "charger"]
    letters = ['b', 'g', 'c']
    max_accuracy=0
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "output2.csv")
    print(file_path)
    # if os.path.exists("tree_last.txt"):
    #     os.remove("tree_last.txt")
    train_data_m = pd.read_csv(file_path)
    # tree = id3(train_data_m, 'ocena')
    # print(tree)
    # tree_string = build_tree_string_reverse(tree)



    # tree_file_path = os.path.join(current_directory, "tree.txt")
    # tree_last_file_path = os.path.join(current_directory, "tree_last.txt")
    # with open(tree_file_path, "r", encoding="utf-8") as f:
    #     tree_str = f.read()  # Чтение содержимого файла в виде строки
    #     tree = json.loads(tree_str)
    # print(tree)


    # Read the content of "tree.txt"
    # with open(tree_file_path, "r", encoding="utf-8") as f:
    #     existing_content = f.read()
    #
    # # Append the new data to "tree.txt"
    # with open(tree_file_path, "a", encoding="utf-8") as f:
    #     f.write(tree_string)
    #
    # # Overwrite the content of "tree_last.txt" with the last data
    # with open(tree_for_human_file_path, "w", encoding="utf-8") as f:
    #     f.write(tree_string)

    letters = ['b', 'g', 'c']
    test_data_file = "test.csv"
    with open(test_data_file, "r", newline="") as file:
        reader = csv.reader(file)
        test_data = list(reader)
    for i in range (0,8):
        test_data[1][i]=levels[i]
    # Перебор букв и оценка дерева для каждой буквы
    max_accuracy = 0
    best_letter = ""
    for letter in letters:
        # Вставка буквы в пустую ячейку
        test_data[1][8] = letter

        # Запись измененных данных обратно в файл
        with open(test_data_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(test_data)

        # Оценка дерева с использованием измененных тестовых данных
        test_data_m = pd.read_csv(test_data_file)
        accuracy = evaluate(tree, test_data_m, 'ocena')

        # Проверка, является ли точность выше текущего максимума
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            best_letter = letter

    # Обновление тестовых данных с лучшей буквой
    test_data[1][8] = best_letter

    # Запись окончательно измененных данных обратно в файл
    with open(test_data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(test_data)
    predict_tree_file_path = os.path.join(current_directory, "predict_tree.txt")

    # Запись дерева с пояснениями в файл "predict_tree.txt"
    write_predict_tree(tree, predict_tree_file_path)
    print("Best letter:", best_letter)
    print("Accuracy:", max_accuracy)
    wynik=''
    match best_letter:
        case 'b':
           wynik='charger'
        case 'g':
            wynik = 'generator'
        case 'c':
            wynik = 'client'
    return wynik

if __name__ == "__main__":
    current_directory = os.getcwd()
    file_path = os.path.join(current_directory, "output2.csv")
    print(file_path)
    # if os.path.exists("tree_last.txt"):
    #     os.remove("tree_last.txt")
    # train_data_m = pd.read_csv(file_path)
    # tree = id3(train_data_m, 'ocena')
    # print(tree)

    # print(tree_string)
    tree_file_path = os.path.join(current_directory, "tree.txt")
    tree_last_file_path = os.path.join(current_directory, "tree_last.txt")
    with open(tree_file_path, "r", encoding="utf-8") as f:
        tree_str = f.read()  # Чтение содержимого файла в виде строки
        tree = json.loads(tree_str)
    print(tree)
    tree_string = build_tree_string_reverse(tree)
    # Read the content of "tree.txt"
    # with open(tree_file_path, "r", encoding="utf-8") as f:
    #     tree = f.read()
    # tree_string = build_tree_string_reverse(tree)
    # print(tree)

    # Append the new data to "tree.txt"
    # with open(tree_file_path, "a", encoding="utf-8") as f:
    #     f.write(tree_string)

    # Overwrite the content of "tree_last.txt" with the last data
    with open(tree_last_file_path, "w", encoding="utf-8") as f:
        f.write(tree_string)

    letters = ['b', 'g', 'c']
    test_data_file = "test.csv"
    with open(test_data_file, "r", newline="") as file:
        reader = csv.reader(file)
        test_data = list(reader)

    # Перебор букв и оценка дерева для каждой буквы
    max_accuracy = 0
    best_letter = ""
    for letter in letters:
        # Вставка буквы в пустую ячейку
        test_data[1][8] = letter

        # Запись измененных данных обратно в файл
        with open(test_data_file, "w", newline="") as file:
            writer = csv.writer(file)
            writer.writerows(test_data)

        # Оценка дерева с использованием измененных тестовых данных
        test_data_m = pd.read_csv(test_data_file)
        accuracy = evaluate(tree, test_data_m, 'ocena')

        # Проверка, является ли точность выше текущего максимума
        if accuracy > max_accuracy:
            max_accuracy = accuracy
            best_letter = letter

    # Обновление тестовых данных с лучшей буквой
    test_data[1][8] = best_letter

    # Запись окончательно измененных данных обратно в файл
    with open(test_data_file, "w", newline="") as file:
        writer = csv.writer(file)
        writer.writerows(test_data)
    predict_tree_file_path = os.path.join(current_directory, "predict_tree.txt")

    # Запись дерева с пояснениями в файл "predict_tree.txt"
    write_predict_tree(tree, predict_tree_file_path)
    print("Best letter:", best_letter)
    print("Accuracy:", max_accuracy)