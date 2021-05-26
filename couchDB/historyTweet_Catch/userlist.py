import json
import pandas as pd

file_input = './area/city_7days_0517.json'
file_output = './area/user_list_0517.csv'

# load the existing user list
# user_list = pd.read_csv("user_list.csv")
# user_id = list(user_list['userID'])

# user_list = pd.read_csv("./area/user_list_0513.csv")
# user_id = list(user_list['userID'])

user_id = []
# new_user_id = []

with open (file_input, 'r') as f:
    json_input = json.load(f)
    for i in range(0,len(json_input)):
        new_user = json_input[str(i)]['user_Id']
        if new_user not in user_id:
            user_id.append(new_user)

# with open (file_input, 'r') as f:
#     json_input = json.load(f)
#     for i in range(0,len(json_input)):
#         new_user = json_input[str(i)]['user_Id']
#         if new_user not in user_id:
#             new_user_id.append(new_user)

# user_list = pd.DataFrame({'userID':user_id})
# user_list.to_csv(file_output, index=False, sep=',')

user_list = pd.DataFrame({'userID':user_id})
user_list.to_csv(file_output, index=False, sep=',')