from pymongo import MongoClient
from pydantic import AnyUrl
import datetime
from pprint import pprint
import os
from dotenv import load_dotenv

dotenv_path = r'E:\Projects\URLShortener\.env' #path to .env
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)

db_host = os.environ.get('db_host')
db_port = os.environ.get('db_port')

class MongoDB(object):
    def __init__(self, host: str = db_host,
                 port: int = db_port,
                 db_name: str | None = None,
                 collection: str | None = None):
        self._client = MongoClient(f'mongodb://{host}:{port}')
        self._collection = self._client[db_name][collection]

    def add_shortCode(self, url: AnyUrl, shortCode: str):
        if self._collection.find_one({'shortCode': shortCode}):
            return 0
        data = {}
        id = len(self._collection.find().to_list()) + 1
        data['id'] = id
        data['url'] = url
        data['shortCode'] = shortCode
        data['createdAt'] = str(datetime.datetime.now())
        data['updatedAt'] = str(datetime.datetime.now())
        data['accessCount'] = 0

        self._collection.insert_one(data)
        print('Added new shortcode')
        return data
    
    def get_url(self, shortCode: str):
        try:
            data = self._collection.find_one({"shortCode": shortCode})
            self._collection.update_one({'shortCode': shortCode}, {'$set': {'accessCount': data['accessCount']+1}})

            print("Get URL")
            return data
        except Exception as e:
            print(e)
    
    def update(self, shortCode: str, url: AnyUrl):
        self._collection.update_one({'shortCode': shortCode}, {'$set': {'url': url}})
        print(f'{shortCode} url updated.')
        return self._collection.find_one({"shortCode":shortCode})
    
    def delete(self, shortCode: str):
        if self._collection.find_one({'shortCode': shortCode}) == None:
            raise ValueError
        self._collection.delete_one({'shortCode': shortCode})
        print(f'{shortCode} deleted. Bye!')

    def get_stats(self, shortCode: str):
        data = self._collection.find_one({'shortCode': shortCode})
        return data
        pprint(data)
