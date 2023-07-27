import pymongo
import requests
import json
from pymongo import MongoClient


BULK_URL = 'https://api.congress.gov/v3/bill?' \
               'api_key={api_key}&limit={limit}&offset={offset}'


def fetch_data(api_key, limit, offset, pages):
    """
    Fetch bill data from congress.gov and write it to an output JSON file
    :param api_key:
    :param limit:
    :param offset:
    :param pages:
    :return:
    """

    headers = {'Content-Type': 'application/json'}
    url = BULK_URL.format(api_key=api_key, limit=limit, offset=offset)
    bills = []

    try:
        for page in range(pages):
            response = requests.request('GET', url, headers=headers)
            bill_obj = json.loads(response.text)

            # for each bill retrieved, get the bill details
            for bill in bill_obj['bills']:
                bill_details_url = bill['url']

                details_res = requests.request(
                    'GET',
                    bill_details_url + '&api_key={0}'.format(api_key)
                )
                bill_details_obj = json.loads(details_res.text)

                bill_details = bill_details_obj['bill']

                # remove redundant properties
                del bill_details['congress']
                del bill_details['number']
                del bill_details['originChamber']
                del bill_details['updateDate']
                del bill_details['title']
                del bill_details['type']
                del bill_details['latestAction']

                # add the bill details object to the bill object
                bill['details'] = bill_details

                bills.append(bill)
            url = bill_obj['pagination']['next'] + f'&api_key={api_key}'
    except Exception:
        print("Encountered an exception. Writing results to the file")

    # write the data to a file
    with open('bills-raw.json', 'a') as f:
        f.write(json.dumps(bills, indent=4))

    print("Data written to output file")


def load_to_mongo(output_file, bills_collection):

    with open(output_file) as f:
        bills = json.load(f)

        for bill in bills:
            bills_collection.insert_one(bill)

    print('Data loaded to mongo')


def main():

    # mongo params
    db_name = 'polistack_db_dev'
    coll_name = 'bill'
    host = 'localhost'
    port = 26016

    # congress.gov api key
    api_key = ''

    fetch_data(api_key, 100, 900, 9)

    # instantiate mongo client
    client = MongoClient(host, port)
    bills_collection = client[db_name][coll_name]

    # load the raw json data to mongo
    load_to_mongo(
        'bills-raw.json', bills_collection
    )

    # create text index
    bills_collection.create_index(
        [
            ('number', pymongo.TEXT),
            ('title', pymongo.TEXT),
        ],
        weights={
            'number': 12,
            'title': 10,
        },
        name='SearchIndex'
    )


if __name__ == '__main__':
    main()
