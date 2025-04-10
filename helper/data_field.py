from pymongo import MongoClient
import os
def data_field(data_src):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        x = mycol.find_one({"data_field": data_src})
        x = x["result"]["question"]
        #st.write(x)
        return x