import os

file_path = 'C:/Users/ausu/Desktop/Dissertation/aspem-master/emb_project/blog_data/node_emb/aspect/'
attribute_path = os.path.join(file_path, 'blogcatalog_k.o_0.2_simple_attribute.emb')
center_path = os.path.join(file_path, 'blogcatalog_k.o_0.2_simple_center.emb')

# initial center node dictionary
node_dict = {}
with open(center_path, 'r') as f_inC:
    lines = f_inC.readlines()
    for line in lines:
        index, emb = line.split(' ')[0], line.split(' ')[1:]
        if index[0] == 'p':
            node_dict[index] = emb
    print('start writing average embedding')

# find multiple node embedding
with open(attribute_path, 'r') as f_inA:
    lines = f_inA.readlines()
    with open('all_nodes_k.o_0.2.emb', 'w') as f_out:
        for line in lines:
            node = line.split(' ')[0]
            if node not in node_dict:
                f_out.writelines([line])
            else:
                center_emb = node_dict[node]
                attribute_emb = line.split(' ')[1:]
                average_emb = []
                for i in range(len(center_emb)-1):
                    ave = round(((eval(attribute_emb[i]) + eval(center_emb[i])) / 2), 6)
                    average_emb.append(ave)
                temp = ' '.join(str(val) for val in average_emb)
                f_out.writelines([node + ' ' + temp + '\n'])
        print('processed complete.')