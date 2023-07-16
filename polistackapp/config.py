from .models import *
import requests
from .constants import *
from .utils import get_db_handle
import datetime


class Config:
    def __init__(self) -> None:
        self.store_congress_data()
        # self.remove_duplicate_tweets()

    def store_congress_data(self):
        """
        Fetches the bills from the API and stores them in the database.
        """
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
    
    def remove_duplicate_tweets(self):
        """
        Removes duplicate entries in the 'tweet_text' field of the 'tweets' collection.
        """
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'tweets' collection
        tweet_collection = db_handle[TWEETS_COLLECTION_NAME]

        # Create an aggregation pipeline to find and remove duplicate tweets
        pipeline = [
            {"$group": {"_id": "$tweet_text", "duplicates": {"$addToSet": "$_id"}, "count": {"$sum": 1}}},
            {"$match": {"count": {"$gt": 1}}},
        ]

        # Execute the aggregation pipeline
        duplicates = list(tweet_collection.aggregate(pipeline))

        if duplicates:
            # Extract the duplicate IDs from the aggregation results
            duplicate_ids = []
            for group in duplicates:
                for i, id in enumerate(group["duplicates"]):
                    if i > 0:
                        duplicate_ids.append(id)

            # Delete the duplicate tweets
            delete_result = tweet_collection.delete_many({"_id": {"$in": duplicate_ids}})

            # Print the number of deleted documents
            print("Number of duplicate tweets deleted:", delete_result.deleted_count)
        else:
            print("No duplicate tweets found.")

        # Close the MongoDB connection
        client.close()

    def fetch_bills(self, search_query, page, items_per_page):
        """
        Fetches the bills from the database with pagination and text search (if any).
        """
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)

        # Access the 'bill' collection
        bill_collection = db_handle[BILLS_COLLECTION_NAME]

        # Calculate the skip value based on the current page and items per page
        skip = (page - 1) * items_per_page

        # Add text search if search_query is provided and is not empty string or None
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
        """
        Fetches the bill details from the database if available, otherwise fetches them from the API and stores them in the database.
        """
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

    def perform_sentiment_analysis(self, search_query):
        """
        Performs sentiment analysis on the tweets and returns the sentiment data.
        """
        if not search_query:
            return {
                "tweet_data": [],
                "sentiment_data": {},
                "tweet_data_length": 0,
            }

        tweets = self.search_tweets(search_query)  # Search for tweets based on the search query
        sentiment_data = self.sentiment_analysis(tweets)  # Perform sentiment analysis on the tweets

        first_5_tweets = tweets[:5]  # Get the first 5 tweets
        for tweet in first_5_tweets:
            timestamp = tweet.get("timestamp")
            if timestamp:
                tweet["formatted_timestamp"] = datetime.datetime.strptime(timestamp, "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %Y")
        tweet_data_length = len(tweets)  # Get the length of the tweets

        return {
            "tweet_data": first_5_tweets,
            "sentiment_data": sentiment_data,
            "tweet_data_length": tweet_data_length,
        }


    def search_tweets(self, search_query):
        # Connect to the MongoDB database
        db_handle, client = get_db_handle(DB_NAME)
        tweet_collection = db_handle[TWEETS_COLLECTION_NAME]

        find_query = {"$text": {"$search": search_query, "$caseSensitive": False}}
        projection = {"score": {"$meta": "textScore"}}
        sort = [("score", {"$meta": "textScore"})]

        # Search for tweets matching the search query
        tweets = tweet_collection.find(find_query, projection).sort(sort)

        # Convert the cursor to a list of tweets
        tweets = list(tweets)

         # Close the MongoDB connection
        client.close()

        # Return the list of tweets
        return tweets


    def sentiment_analysis(self, tweets):
        total_score = 0

        for tweet in tweets:
            sentiment = tweet.get("sentiment")  # Get the sentiment value from the tweet

            if sentiment == "positive":
                sentiment_score = 0.8  # Assign a positive sentiment score
            elif sentiment == "negative":
                sentiment_score = -0.8  # Assign a negative sentiment score
            else:
                sentiment_score = 0  # Assign a neutral sentiment score

            # Add the sentiment score to the total score
            total_score += sentiment_score

        # Calculate the average score
        if len(tweets) > 0:
            average_score = total_score / len(tweets)
        else:
            average_score = 0

        # Create a dictionary with the total score and average score
        sentiment_data = {
            "total_score": round(total_score, 3),
            "average_score": round(average_score, 3),
        }

        return sentiment_data