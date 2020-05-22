import os
data_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/HIN_dataset'
dirs = os.listdir(data_path)
dirs_list = []
node_dict = dict()
node_list=[]
for path in dirs:
    if os.path.splitext(path)[1] == ".hin":
        dirs_list.append(path)

node_index = 'node_index'
if not os.path.exists(node_index):
    os.mkdir(node_index)

for hin_path in dirs_list:
    with open(hin_path, 'r') as f_in:
        for line in f_in:
            left_node, right_node, weight, edge_type = line.strip().split()
            if left_node in node_list:
                node_dict[left_node[0]]+=1
            if right_node in node_list:
                node_dict[right_node[0]]+=1
            if left_node not in node_list:
                if left_node[0] in node_dict:
                    node_dict[left_node[0]]+=1
                else:
                    node_dict[left_node[0]] = 1
                node_list.append(left_node)
            if right_node not in node_list:
                if right_node[0] in node_dict:
                    node_dict[right_node[0]]+=1
                else:
                    node_dict[right_node[0]] = 1
                node_list.append(right_node)

for i in node_dict:
    print(i,node_dict[i])