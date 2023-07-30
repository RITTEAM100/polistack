API_KEY = 'Y1hRdQCbKpOFFQVY1sUsxyiAzZ3XQgejdC45GRP1'
# API URLS
BASE_URL = 'https://api.congress.gov/v3'

API_URL_GET_BILLS = BASE_URL + '/bill'
API_URL_GET_BILL_DETAIL = BASE_URL + '/bill/{congress}/{bill_type}/{bill_number}'

# MongoDB
USERNAME = "rishabharora3"
PASSWORD = "BylXEdTOV7AQMEgH"
CLUSTER_NAME = "polistack.xrwxjxj.mongodb.net"
# URI = f"mongodb+srv://{USERNAME}:{PASSWORD}@{CLUSTER_NAME}/?retryWrites=true&w=majority"
URI = "mongodb+srv://vercel-admin-user:hwSjfWkmwxKWbnOB@polistack.xrwxjxj.mongodb.net/myFirstDatabase?retryWrites=true&w=majority"
DB_NAME = "polistack_db"
BILLS_COLLECTION_NAME = "bill"
BILL_DETAIL_COLLECTION_NAME = "bill_detail"
TWEETS_COLLECTION_NAME = "tweets"

BILLS_COUNT = 1000
ITEMS_PER_PAGE = 10