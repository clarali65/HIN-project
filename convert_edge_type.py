import os
data_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/data/HIN_dataset'
dirs = os.listdir(data_path)
dirs_list = []
for path in dirs:
    if os.path.splitext(path)[1] == ".hin":
        dirs_list.append(path)

new_hin_folder = 'new_hin_folder'
if not os.path.exists(new_hin_folder):
    os.mkdir(new_hin_folder)

for hin_path in dirs_list:
    with open(hin_path, 'r') as f_in:
        f_new_hin_name = os.path.join(new_hin_folder, hin_path)
        with open(f_new_hin_name, 'w') as f_out:
            for line in f_in:
                a = len(line.strip().split())
                if len(line.strip().split()) == 4:
                    left_node, right_node, weight_str, edge_type = line.strip().split()
                    center_node = left_node
                    attribute_node = right_node
                    f_out.write(attribute_node + ' ')
                    f_out.write(center_node + ' ')
                    f_out.write(str(weight_str) + ' ')
                    f_out.write(attribute_node[0] + center_node[0] + "\n")
                else:
                    left_node, right_node = line.strip().split()
                    center_node = left_node
                    attribute_node = right_node
                    weight_str = 1
                    f_out.write(attribute_node + ' ')
                    f_out.write(center_node + ' ')
                    f_out.write(str(weight_str) + ' ')
                    f_out.write(attribute_node[0] + center_node[0] + "\n")