import os
import numpy as np
import sklearn
from sklearn import svm
import warnings
warnings.filterwarnings("ignore")

def my_svm(x, y, k = 5, split_list = [0.2,0.4,0.6,0.8], time = 10, show_train = True, shuffle = True):
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
                    permutation = np.random.permutation(x.shape[0])  # np.random.permutation:打乱顺序后并返回
                    x = x[permutation, :]
                    y = y[permutation]

                train_x = x[:split, :]
                test_x = x[split:, :]

                train_y = y[:split]
                test_y = y[split:]

                estimator = svm.SVC(gamma='scale', decision_function_shape='ovo')
                estimator.fit(train_x, train_y)
                y_pred = estimator.predict(test_x)
                acc_s = sklearn.metrics.accuracy_score(test_y, y_pred)
                f1_macro = sklearn.metrics.f1_score(test_y, y_pred, average='macro')
                f1_micro = sklearn.metrics.f1_score(test_y, y_pred, average='micro')
                macro_list.append(f1_macro)
                micro_list.append(f1_micro)
                acc.append(acc_s)
            print('SVM({}avg, split:{}, k={}) f1_macro: {:.4f}, f1_micro: {:.4f}, acc: {:.4f}'.format(
                time, ss, k, sum(macro_list) / len(macro_list), sum(micro_list) / len(micro_list), sum(acc) / len(acc)))

label_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/emb_project/cora_data/cora_paper_label.txt'
concate_emb_file_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/emb_project/cora_data/node_emb/concate/'
emb_file_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/emb_project/cora_data/node_emb/aspect/'
new_label_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/emb_project/cora_data/'
new_label = 'new_cora_paper_label.txt'

emb_dict = {} #key:node index,value:node_embedding
label_dict = {} #key:node_index,value:node_label
emb_list = []
label_list = []
concatenate = False

if concatenate is not True:
    # preprocessing for embedding
    dirs = os.listdir(emb_file_path)
    for path in dirs:
        if os.path.splitext(path)[1] == '.emb':
            path = os.path.join(emb_file_path, path)
        else:
            continue
        with open(path, 'r') as f_in_emb:
            for line_emb in f_in_emb:
                idx = line_emb.rstrip().split()[0]
                emb = [float(ele) for ele in line_emb.rstrip().split()[1:]]
                if idx[0] == "p":
                    emb_dict[idx] = emb

    # preprocessing of label
    with open(label_path, 'r') as f_in_label:
        f_new_label_name = os.path.join(new_label_path, new_label)
        with open(f_new_label_name, 'w') as f_out_label:
            for line_in in f_in_label:
                index, label = line_in.strip().split()
                node_name = "p:" + str(index)
                if node_name in emb_dict:
                    label_dict[node_name] = label
                    label_list.append(label)
                    emb_list.append(emb_dict[node_name])
                    f_out_label.write(node_name + ' ')
                    f_out_label.write(label + '\n')

    my_svm(emb_list, label_list)
    print(path[-6:-4], "has been processed.")

else:
    emb_dict = dict()
    emb_list = []
    dirs = os.listdir(concate_emb_file_path)

    for path in dirs:
        if os.path.splitext(path)[1] == '.emb':
            path = os.path.join(concate_emb_file_path, path)
        else:
            continue
        with open(path, 'r') as f_in_emb:
            for line in f_in_emb:
                idx = line.rstrip().split()[0]
                emb = [float(ele) for ele in line.rstrip().split()[1:]]
                if idx[0] == "p":
                    if idx not in emb_dict:
                        emb_dict[idx] = emb
                    else:
                        emb_dict[idx] = np.concatenate([emb_dict[idx], emb], axis=0)
                        #concate_emb_dict[idx] = emb_dict[idx]
                    #if a[-2:] == 'ap':
                        #emb_dict_ap[idx] = emb
                    #elif a[-2:] == 'tp':
                        #emb_dict_tp[idx] = emb
                    #else:
                        #emb_dict_vp[idx] = emb
    #for node_name in emb_dict:
        #temp = np.concatenate([emb_dict_ap[node_name], emb_dict_tp[node_name], emb_dict_vp[node_name]])
        #concate_emb_dict[node_name] = list(temp)
    with open(label_path, 'r') as f_in_label:
        f_new_label_name = os.path.join(new_label_path, new_label)
        with open(f_new_label_name, 'w') as f_out_label:
            for line_in in f_in_label:
                index, label = line_in.strip().split()
                node_name = "p:" + str(index)
                if node_name in emb_dict:
                    label_dict[node_name] = label
                    label_list.append(label)
                    emb_list.append(emb_dict[node_name])
                    f_out_label.write(node_name + ' ')
                    f_out_label.write(label + '\n')

    my_svm(emb_list, label_list)
    print( "concatenate has been processed.")