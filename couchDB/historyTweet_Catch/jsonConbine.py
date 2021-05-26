import json

# input files
input_file_1 = './result_all_1_20_cityCollection_7523_0514added.json'
# input_file_1 = './area/city_7days_0517.json'
input_file_2 = './area/tweets_0517_all.json'

# store result in one json file
json_out = './result_all_1_20_cityCollection_7523_0517added.json'
# json_out = './area/tweets_0517_all.json'
list_input_1_id = []

list_output = []


# write the input_file_1 all object in output list and store id in another file
with open (input_file_1, 'r') as f_1:
    json_1 = json.load(f_1)
    # print(len(json_1))
for i in range(0,len(json_1)):
    tem_ob = json_1[str(i)]
    tem_id = tem_ob['id']
    list_input_1_id.append(tem_id)
    list_output.append(tem_ob)

# deal with the input_file_2, duplicates remove
add_ob = []

with open (input_file_2, 'r') as f_2:
    json_2 = json.load(f_2)
for i in range(0,len(json_2)):
    tem_ob2 = json_2[str(i)]
    tem_id2 = tem_ob2['id']
    if tem_id2 not in list_input_1_id:
        add_ob.append(tem_ob2)
    else:
        pass

for o in add_ob:
    list_output.append(o)

# print(list_output)



output_dic = {}
for i in range(0, len(list_output)):
    output_dic[i] = list_output[i]


with open(json_out, 'w') as fw:
    json.dump(output_dic, fw, indent=4)