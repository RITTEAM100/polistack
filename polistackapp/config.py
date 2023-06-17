from django.core.cache import cache
from django.http import HttpResponse
from .models import *
import requests
from .constants import *


class Config:
    # def __init__(self) -> None:
    # self.store_congress_data()

    def store_congress_data(self, limit, offset):
        # Fetch data from the Congress API

        params = {"api_key": API_KEY, "limit": limit}
        response = requests.get(API_URL_GET_BILLS, params=params)

        # Parse the API response
        if response.status_code == 200:
            data_from_api = response.json()
        else:
            data_from_api = []
        print("api data:" + str(data_from_api))
        return data_from_api

        # Store the data in MongoDB
        # client = MongoClient('mongodb://localhost:27017/')
        # db = client['your_database_name']
        # collection = db['your_collection_name']
        # collection.insert_many(data_from_api)
