import json
import os
from pymongo import MongoClient
from dotenv import load_dotenv
 
dag_path = os.path.dirname(os.path.abspath(__file__))
load_dotenv(os.path.join(dag_path, '.env'))
 
mongo_uri = os.getenv("MONGO_URI")
mongo_db_name = os.getenv("MONGO_DB")

def load_data_to_mongo():

    dag_path = os.path.dirname(os.path.abspath(__file__))

    with open(os.path.join(dag_path, 'topic.txt'), 'r') as keyword:
        topic = keyword.read().strip()

    filename = os.path.join(dag_path, f"{topic}.json")

    if not os.path.exists(filename):
        print('no file exist')
        return

    with open(filename, "r") as video_data:
        data = json.load(video_data)

    if not data:
        print('empty data, skip mongo update')
        return

    #connect to local mongodb
    client = MongoClient(mongo_uri)
    db = client[mongo_db_name]
    collection = db[topic]

    collection.drop()
    collection.insert_many(data)

    print(f"Successfully uploaded {len(data)} videos to collection '{topic}'.")

    os.remove(filename)
    print("'{filename}' deleted")

if __name__ == "__main__":
    load_data_to_mongo()