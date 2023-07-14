from .models import *
import requests
from .constants import *
from .utils import get_db_handle


class Config:
    def __init__(self) -> None:
        self.store_congress_data()

    def store_congress_data(self):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Access the 'bill_detail' collection
        bill_detail_collection = db_handle[BILL_DETAIL_COLLECTION_NAME]

        # Clear the existing data in the collection 'bill'
        bill_collection.delete_many({})

        # Clear the existing data in the 'bill_detail' collection
        bill_detail_collection.delete_many({})

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

    def fetch_bills(self, search_query, page, items_per_page):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Calculate the skip value based on the current page and items per page
        skip = (page - 1) * items_per_page

        # Add a search query to the find query if a search query is passed
        if search_query is not None and search_query.strip():
            find_query = {"$text": {"$search": search_query, "$caseSensitive": False}}
            projection = {"score": {"$meta": "textScore"}}
            sort = [("score", {"$meta": "textScore"})]
        else:
            find_query = {}
            projection = {}
            sort = None  # Set sort to None for default sorting

        # Fetch bills from the database with pagination and text search (if any)
        bills_cursor = bill_collection.find(find_query, projection)

        # Sort the cursor if sort parameter is provided
        if sort:
            bills_cursor.sort(sort)

        # Limit the cursor to the specified items_per_page
        bills_cursor.skip(skip).limit(items_per_page)

        # Fetch bills as a list
        bills = list(bills_cursor)

        # Calculate the total number of bills
        total_bills = bill_collection.count_documents(find_query)

        # Close the MongoDB connection
        client.close()

        return {
            "bills": bills,
            "total_bills": total_bills,
        }

    def fetch_bill_details(self, bill_id):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Access the 'bill_detail' collection
        bill_detail_collection = db_handle[BILL_DETAIL_COLLECTION_NAME]

        # Check if the bill details already exist in the 'bill_detail' collection
        bill = bill_detail_collection.find_one({"number": bill_id})

        if bill:
            # If the bill details are already available in the 'bill_detail' collection, return them
            return bill

        else:
            # If the bill details are not available, fetch them from the 'bill' collection
            bill_data = bill_collection.find_one({"number": bill_id})

            if bill_data:
                # Construct the API URL for the bill detail
                api_url = API_URL_GET_BILL_DETAIL.format(
                    congress=bill_data["congress"],
                    bill_type=bill_data["type"],
                    bill_number=bill_data["number"],
                )

                # Make an API call to fetch the bill detail
                url = f"{api_url}?api_key={API_KEY}"
                response = requests.get(url)

                if response.status_code == 200:
                    bill_detail_data = response.json().get("bill")

                    if bill_detail_data:
                        # Save the bill detail in the 'bill_detail' collection
                        bill_detail_collection.insert_one(bill_detail_data)

                        # Return the bill detail
                        return bill_detail_data

        # Close the MongoDB connection
        client.close()
