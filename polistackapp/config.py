from django.core.cache import cache
from django.http import HttpResponse
from .models import *
import requests
from .constants import *
import pymongo
from .utils import get_db_handle


class Config:
    def __init__(self) -> None:
        self.store_congress_data()

    def store_congress_data(self):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Clear the existing data in the collection
        bill_collection.delete_many({})

        # Fetch data from the Congress API
        params = {"api_key": API_KEY, "limit": BILLS_COUNT}
        response = requests.get(API_URL_GET_BILLS, params=params)

        # Parse the API response
        if response.status_code == 200:
            data_from_api = response.json()
        else:
            data_from_api = []

        # print("API data:", str(data_from_api))

        bills = data_from_api.get("bills", [])

        if bills:
            # Store data in the 'bill' collection
            bill_collection.insert_many(bills)

        # Close the MongoDB connection
        client.close()

        return data_from_api
    
    def fetch_bills(self, page, items_per_page):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Calculate the skip value based on the current page and items per page
        skip = (page - 1) * items_per_page

        # Fetch bills from the database with pagination
        bills = list(bill_collection.find().skip(skip).limit(items_per_page))

        # Calculate the total number of bills
        total_bills = bill_collection.count_documents({})

        # Close the MongoDB connection
        client.close()

        return {
            'bills': bills,
            'total_bills': total_bills,
        }

