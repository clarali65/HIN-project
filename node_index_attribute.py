import os
data_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/HIN_dataset'
dirs = os.listdir(data_path)
dirs_list = []
# attribute_node_dict = {"U": [], "C": [], "T": []}
attribute_node_list = []
for path in dirs:
    if os.path.splitext(path)[1] == ".hin":
        dirs_list.append(path)

node_index = 'node_index'
if not os.path.exists(node_index):
    os.mkdir(node_index)

for hin_path in dirs_list:
    with open(hin_path, 'r') as f_in:
        hin_path = hin_path[:-4] + "_attribute_node" + ".node"
        f_new_hin_name = os.path.join(node_index, hin_path)
        with open(f_new_hin_name, 'w') as f_out:
            for line in f_in:
                left_node, right_node, weight, edge_type = line.strip().split()
                if right_node in attribute_node_list:
                    continue
                else:
                    attribute_node_list.append(right_node)
                    #attribute_node = right_node
                    f_out.write(right_node + '\n')
                #if left_node in attribute_node_list:
                #    continue
                #else:
                #    attribute_node_list.append(left_node)
                #    f_out.write(left_node + '\n')

        print(hin_path[:-4] + " has been processed.")