from pymongo import MongoClient
import os
def data_field(data_src):
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_data"]
        x = mycol.find_one({"data_field": data_src},
                sort=[('timestamp', -1)])
        x = x["result"]
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


def get_marketplace_response(data_src):
    try:
        mongodb_uri = os.getenv("MONGODB_URI")
        myclient = MongoClient(mongodb_uri)
        mydb = myclient.get_database()
        mycol = mydb["df_response"]
        
        # Find the most recent document matching the data_src
        document = mycol.find_one(
            {"data_field": data_src},
            sort=[('timestamp', -1)]
        )
        
        # Check if document exists and has the result field
        if document and "result" in document:
            # Extract amazon and ebay data separately
            amazon_data = document["result"].get("amazon", [])
            ebay_data = document["result"].get("ebay", [])
            
            # Combine both datasets into a single list
            combined_data = amazon_data + ebay_data
            
            return combined_data
        else:
            print(f"No matching document or 'result' field found for data_src: {data_src} in df_response. 404")
            return None
    except Exception as e:
        print(f"Error retrieving data: {str(e)}")
        return None
    finally:
        if myclient:
            myclient.close()
        