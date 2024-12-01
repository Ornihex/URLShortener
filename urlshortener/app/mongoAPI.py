from pymongo import MongoClient
from pydantic import AnyUrl
import datetime
from pprint import pprint
import os
from dotenv import load_dotenv

dotenv_path = os.path.join(os.path.split(os.path.dirname(__file__))[0], '.env') # path to .env file
if os.path.exists(dotenv_path):
    load_dotenv(dotenv_path)
    db_host = os.environ.get('db_host')
    db_port = os.environ.get('db_port')
else:
    db_host = 'localhost'
    db_port = '27017'

class MongoDB(object): 
    def __init__(self, host: str = db_host,
                 port: int = db_port,
                 db_name: str | None = None,
                 collection: str | None = None):
        self._client = MongoClient(f'mongodb://{host}:{port}')
        self._collection = self._client[db_name][collection]

    def add_shortCode(self, url: AnyUrl, shortCode: str) -> dict:
        '''
        add_shortcode(url, shortCode) -> dict

        This function adds the url and its short code to the database.

        arguments:
        url -- site url. Correct example: https://example.org
                         Wrong example: example.org
        shortCode -- url short code. It is generated automatically in the 'shorten' function of the module shorten.py
        '''
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
    
    def get_url(self, shortCode: str) -> dict:
        '''
        get_url(shortCode) -> dict

        This function retrieve original url from the database by short code. 

        arguments:
        shortCode -- url short code.
        '''
        try:
            data = self._collection.find_one({"shortCode": shortCode})
            self._collection.update_one({'shortCode': shortCode}, {'$set': {'accessCount': data['accessCount']+1}})

            print("Get URL")
            return data
        except Exception as e:
            print(e)
    
    def update(self, shortCode: str, url: AnyUrl) -> dict:
        '''
        update(shortCode, url) -> dict

        This function updates the url in the database by short code.

        arguments:
        shortCode -- url short code.
        url -- site url. Correct example: https://example.org
                         Wrong example: example.org
        '''
        self._collection.update_one({'shortCode': shortCode}, {'$set': {'url': url}})
        print(f'{shortCode} url updated.')
        return self._collection.find_one({"shortCode":shortCode})
    
    def delete(self, shortCode: str) -> None:
        '''
        delete(shortCode) -> None

        This function removes url short code from the databse.

        arguments:
        shortCode -- url short code.
        '''
        if self._collection.find_one({'shortCode': shortCode}) == None:
            raise ValueError
        self._collection.delete_one({'shortCode': shortCode})
        print(f'{shortCode} deleted. Bye!')

    def get_stats(self, shortCode: str) -> dict:
        '''
        get_stats(shortCode) -> dict

        This function retrieve the url short code statistics from the database.

        arguments:
        shortCode -- url short code.
        '''
        data = self._collection.find_one({'shortCode': shortCode})
        pprint(data)