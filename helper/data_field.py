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

def get_analyst_response(data_src):
        try:
                mongodb_uri = os.getenv("MONGODB_URI")
                myclient = MongoClient(mongodb_uri)
                mydb = myclient.get_database()
                mycol = mydb["df_response"]
                x = mycol.find_one({"data_field": data_src},
                sort=[('timestamp', -1)])
                if x and "result" in x:
                        return x["result"]
                else:
                        print(f"No matching document or 'result' field found for data_src: {data_src} in df_response. 404")
                        return None # Return None if no doc or 'result' field found
        finally:
                if myclient:
                        myclient.close()

#
        