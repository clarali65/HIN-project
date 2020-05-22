import os
import numpy as np
from sklearn import svm

def my_svm(x, y, k=5, split_list=[0.2, 0.4, 0.6, 0.8], time=10, show_train=True, shuffle=True):
    x = np.array(x)
    x = np.squeeze(x)
    y = np.array(y)
    if len(y.shape) > 1:
        y = np.argmax(y, axis=1)
    for split in split_list:
        ss = split
        split = int(x.shape[0] * split)
        micro_list = []
        macro_list = []
        acc = []
        if time:
            for i in range(time):
                if shuffle:
                    permutation = np.random.permutation(x.shape[0])
                    x = x[permutation, :]
                    y = y[permutation]

                train_x = x[:split, :]
                test_x = x[split:, :]

                train_y = y[:split]
                test_y = y[split:]

                estimator = svm.SVC(gamma='scale', decision_function_shape='ovo')
                estimator.fit(train_x, train_y)
                y_pred = estimator.predict(test_x)
                acc_s = accuracy_score(test_y,y_pred)
                f1_macro = f1_score(test_y, y_pred, average='macro')
                f1_micro = f1_score(test_y, y_pred, average='micro')
                macro_list.append(f1_macro)
                micro_list.append(f1_micro)
                acc.append(acc_s)
            print('SVM({}avg, split:{}, k={}) f1_macro: {:.4f}, f1_micro: {:.4f}, acc: {:.4f}'.format(
                time, ss, k, sum(macro_list) / len(macro_list), sum(micro_list) / len(micro_list), sum(acc)/ len(acc)))
