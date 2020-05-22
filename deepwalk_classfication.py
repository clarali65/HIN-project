import os
import numpy as np
import sklearn
from sklearn import svm
import warnings
warnings.filterwarnings("ignore")

# data preprocessing

data_path = 'C:/Users/ausu/Desktop/Dissertation/deepwalk-master/hin/'
dirs = os.listdir(data_path)
dirs_list = []
node_list = []
node_dict = {}
classification_list = []
for path in dirs:
    if os.path.splitext(path)[1] == ".hin":
        dirs_list.append(path)

graphs_folder = 'graphs'
if not os.path.exists(graphs_folder):
    os.mkdir(graphs_folder)

for hin_path in dirs_list:
    new_hin_path = os.path.join(data_path, hin_path)
    with open(new_hin_path, 'r') as f_in:
        for line in f_in:
            left_node = line.rstrip().split()[0]
            right_node = line.rstrip().split()[1]
            l = int(left_node[2:])
            if left_node[0] == 'a' and l not in classification_list:
                classification_list.append(int(left_node[2:]))
            if int(left_node[2:]) in node_list:
                left_node = int(left_node[2:])
                node_dict[left_node].append(int(right_node[2:]))
            else:
                left_node = int(left_node[2:])
                node_list.append(left_node)
                node_dict[left_node] = []
                node_dict[left_node].append(int(right_node[2:]))
    print(hin_path[:-4] + " left node has been processed.")

    with open(new_hin_path, 'r') as f_in:
        for line in f_in:
            left_node = line.rstrip().split()[0]
            right_node = line.rstrip().split()[1]
            r = int(right_node[2:])
            if right_node[0] == 'a'and r not in classification_list:
                classification_list.append(int(right_node[2:]))
            if int(right_node[2:]) in node_list:
                right_node = int(right_node[2:])
                node_dict[right_node].append(int(left_node[2:]))
            else:
                right_node = int(right_node[2:])
                node_list.append(right_node)
                node_dict[right_node] = []
                node_dict[right_node].append(int(left_node[2:]))
    print(hin_path[:-4] + " right node has been processed.")

    f_adj_list = os.path.join(graphs_folder, hin_path[:-4]) + ".adjlist"
    with open(f_adj_list, 'w') as f_out:
        for node in node_dict:
            f_out.write(str(node))
            s = str(node_dict[node]).replace('[', ' ').replace(']', '').replace(',', '')
            f_out.write(s + '\n')
    print(hin_path[:-4] + " graph has been processed.")

# classification
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

label_path = 'C:/Users/ausu/Desktop/Dissertation/deepwalk-master/label/dblp_author_label.txt'
emb_file_path = 'C:/Users/ausu/Desktop/Dissertation/deepwalk-master/graphs/'
new_label_path = 'C:/Users/ausu/Desktop/Dissertation/deepwalk-master/label/'
new_label = 'new_dblp_author_label.txt'

emb_dict = {} #key:node index,value:node_embedding
label_dict = {} #key:node_index,value:node_label
emb_list = []
label_list = []

# preprocessing for embedding
dirs = os.listdir(emb_file_path)
for path in dirs:
    if os.path.splitext(path)[1] == '.embeddings':
        path = os.path.join(emb_file_path, path)
    else:
        continue
    with open(path, 'r') as f_in_emb:
        for line_emb in f_in_emb:
            idx = line_emb.rstrip().split()[0]
            emb = [float(ele) for ele in line_emb.rstrip().split()[1:]]
            if int(idx) in classification_list:
                emb_dict[idx] = emb

# preprocessing of label
with open(label_path, 'r') as f_in_label:
    for line_in in f_in_label:
        index, label = line_in.strip().split()
        if index in emb_dict:
            label_list.append(label)
            emb_list.append(emb_dict[index])

my_svm(emb_list, label_list)
print(" embedding has been processed.")