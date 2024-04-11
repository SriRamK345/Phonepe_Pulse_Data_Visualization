import os
import json
import pandas as pd
import mysql.connector

path_1 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/aggregated/transaction/country/india/state/"
Agg_tran = os.listdir(path_1)

Agg_tra = {'State': [], 'Year': [], 'Quarter': [], 'Trans_type': [], 'Trans_count': [], 'Trans_amount': []}

for i in Agg_tran:
    path_i = path_1 + i + "/"
    agg_year = os.listdir(path_i)

    for j in agg_year:
        path_j = path_i + j + "/"
        agg_json = os.listdir(path_j)

        for k in agg_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            data = load['data']['transactionData']
            for A in data:
                name = A["name"]
                count = A ["paymentInstruments"][0]["count"]
                amount = A ["paymentInstruments"][0]["amount"]
                Agg_tra['State'].append(i)
                Agg_tra['Year'].append(j)
                Agg_tra['Quarter'].append(int(k.strip('.json')))
                Agg_tra['Trans_type'].append(name)
                Agg_tra['Trans_count'].append(count)
                Agg_tra['Trans_amount'].append(amount)

df_aggregated_transaction = pd.DataFrame(Agg_tra)

path_2 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/aggregated/user/country/india/state/"
Agg_user_state = os.listdir(path_2)
Agg_user = {'State': [], 'Year': [], 'Quarter': [], 'Brands': [], 'User_Count': [], 'User_Percentage': []}

for i in Agg_user_state:
    path_i = path_2 + i + "/"
    agg_year = os.listdir(path_i)

    for j in agg_year:
        path_j = path_i + j + "/"
        agg_json = os.listdir(path_j)

        for k in agg_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            try:
                data_1 = load['data']["usersByDevice"]
                for A in data_1:
                    ALL_percentage = A["percentage"]
                    brand = A["brand"]
                    count = A["count"]
                    Agg_user['State'].append(i)
                    Agg_user['Year'].append(j)
                    Agg_user['Quarter'].append(int(k.strip('.json')))
                    Agg_user["Brands"].append(brand)
                    Agg_user["User_Count"].append(count)
                    Agg_user["User_Percentage"].append(ALL_percentage*100)
                    
            except:
                pass

df_aggregated_user = pd.DataFrame(Agg_user)

path_3 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/map/transaction/hover/country/india/state/"
map_tran = os.listdir(path_3)
map_tra = {'State': [], 'Year': [], 'Quarter': [], 'District': [], 'Trans_Count': [], 'Trans_Amount': []}

for i in map_tran:
    path_i = path_3 + i + "/"
    map_year = os.listdir(path_i)

    for j in map_year:
        path_j = path_i + j + "/"
        map_json = os.listdir(path_j)

        for k in map_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            data_2 = load['data']['hoverDataList']
            for A in data_2:
                name = A ["name"]
                count = A ["metric"][0]["count"]
                amount = A ["metric"][0]["amount"]
                map_tra['State'].append(i)
                map_tra['Year'].append(j)
                map_tra['Quarter'].append(int(k.strip('.json')))
                map_tra["District"].append(name)
                map_tra["Trans_Count"].append(count)
                map_tra["Trans_Amount"].append(amount)

df_map_transaction = pd.DataFrame(map_tra)            


path_4 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/map/user/hover/country/india/state/"        
map_user = os.listdir(path_4)
map_user_info = {"State": [], "Year": [], "Quarter": [], "District": [], "User_id": []}

for i in map_user:
    path_i = path_4 + i + "/"
    map_year = os.listdir(path_i)

    for j in map_year:
        path_j = path_i + j + "/"
        map_json = os.listdir(path_j)

        for k in map_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            data_3 = load['data']['hoverData']
            for A in data_3.items():                 # items is used to convert dist_items to tuple values 
                name = A [0]
                registereduser = A[1]["registeredUsers"]
                map_user_info['State'].append(i)
                map_user_info['Year'].append(j)
                map_user_info['Quarter'].append(int(k.strip('.json')))
                map_user_info["District"].append(name)
                map_user_info["User_id"].append(registereduser)

df_map_user = pd.DataFrame(map_user_info)           

path_5 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/top/transaction/country/india/state/"        
top_tran = os.listdir(path_5)
top_trans = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'Trans_Count': [], 'Trans_Amount': []}

for i in top_tran:
    path_i = path_5 + i + "/"
    top_year = os.listdir(path_i)

    for j in top_year:
        path_j = path_i + j + "/"
        top_json = os.listdir(path_j)

        for k in top_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            data_4= load["data"]["pincodes"]
            for A in data_4:
                entityName = A ["entityName"]
                count = A ["metric"]["count"]
                amount = A ["metric"]["amount"] 
                top_trans['State'].append(i)
                top_trans['Year'].append(j)
                top_trans['Quarter'].append(int(k.strip('.json')))
                top_trans["District_Pincode"].append(entityName)
                top_trans["Trans_Count"].append(count)
                top_trans["Trans_Amount"].append(amount)

df_top_transaction = pd.DataFrame(top_trans)            

path_6 = "G:/Guvi/VS code/.venv/Phonepe pro/Gitclone/pulse-master/data/top/user/country/india/state/"        
top_user = os.listdir(path_6)
top_user_info = {'State': [], 'Year': [], 'Quarter': [], 'District_Pincode': [], 'User_id': []}

for i in top_user:
    path_i = path_6 + i + "/"
    top_year = os.listdir(path_i)

    for j in top_year:
        path_j = path_i + j + "/"
        top_json = os.listdir(path_j)

        for k in top_json:
            path_k = path_j + k
            json_open = open(path_k, "r")
            load = json.load(json_open)

            data = load["data"]["pincodes"]
            for A in data:
                name= A["name"]
                registeredUser = A["registeredUsers"]
                top_user_info['State'].append(i)
                top_user_info['Year'].append(j)
                top_user_info['Quarter'].append(int(k.strip('.json')))
                top_user_info['District_Pincode'].append(name)
                top_user_info['User_id'].append(registeredUser)

df_top_user = pd.DataFrame(top_user_info)

# Create a new database and use
cursor = conn.cursor()
cursor.execute("CREATE DATABASE IF NOT EXISTS Phonepe")

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)

cursor = conn.cursor()
table_1 = cursor.execute("""CREATE TABLE IF NOT EXISTS aggregated_transaction(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                Trans_type VARCHAR(100),
                                Trans_count INT,
                                Trans_amount FLOAT
)""")
conn.commit()

insert_query1 = """INSERT INTO aggregated_transaction(State, Year, Quarter, Trans_type, Trans_count, Trans_amount)
                                                VALUES (%s,%s,%s,%s,%s,%s)"""

values = df_aggregated_transaction.values.tolist()
cursor.executemany(insert_query1,values)
conn.commit()

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()
table_2 = cursor.execute("""CREATE TABLE IF NOT EXISTS aggregated_user(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                Brands VARCHAR(50),
                                User_Count INT,
                                User_Percentage FLOAT
)""")
conn.commit()

insert_query2 = """INSERT INTO aggregated_user(State, Year, Quarter, Brands, User_Count, User_Percentage)
                                                VALUES (%s,%s,%s,%s,%s,%s)"""

values = df_aggregated_user.values.tolist()
cursor.executemany(insert_query2,values)
conn.commit()

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()
table_3 = cursor.execute("""CREATE TABLE IF NOT EXISTS map_transaction(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                District VARCHAR(80),
                                Trans_Count INT,
                                Trans_Amount FLOAT
)""")
conn.commit()

insert_query3 = """INSERT INTO map_transaction(State, Year, Quarter, District, Trans_Count, Trans_Amount)
                                                VALUES (%s,%s,%s,%s,%s,%s)"""

values = df_map_transaction.values.tolist()
cursor.executemany(insert_query3,values)
conn.commit()
# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()
table_4 = cursor.execute("""CREATE TABLE IF NOT EXISTS map_user(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                District VARCHAR(80),
                                User_id BIGINT
                                
)""")
conn.commit()

insert_query4 = """INSERT INTO map_user(State, Year, Quarter, District, User_id)
                                                VALUES (%s,%s,%s,%s,%s)"""

values = df_map_user.values.tolist()
cursor.executemany(insert_query4,values)
conn.commit()

# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()
table_5 = cursor.execute("""CREATE TABLE IF NOT EXISTS top_transaction(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                District_Pincode INT,
                                Trans_Count INT,
                                Trans_Amount FLOAT
)""")
conn.commit()

insert_query5 = """INSERT INTO top_transaction(State, Year, Quarter, District_Pincode, Trans_Count, Trans_Amount)
                                                VALUES (%s,%s,%s,%s,%s,%s)"""

values = df_top_transaction.values.tolist()
cursor.executemany(insert_query5,values)
conn.commit()# Establish a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="India@123",
    database="Phonepe",
    port=3306
)
cursor = conn.cursor()
table_6 = cursor.execute("""CREATE TABLE IF NOT EXISTS top_user(
                                State VARCHAR(100),
                                Year INT,
                                Quarter INT,
                                District_Pincode INT,
                                User_id BIGINT
                                
)""")
conn.commit()

insert_query6 = """INSERT INTO top_user(State, Year, Quarter, District_Pincode, User_id)
                                                VALUES (%s,%s,%s,%s,%s)"""

values = df_top_user.values.tolist()
cursor.executemany(insert_query6,values)
conn.commit()

