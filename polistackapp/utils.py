from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import ssl
from .constants import URI


def get_db_handle(db_name, host="localhost", port=27017):
    """
    Establishes a connection to MongoDB and returns the database handle.

    Args:
        db_name (str): The name of the database.
        host (str, optional): The MongoDB host. Defaults to 'localhost'.
        port (int, optional): The MongoDB port. Defaults to 27017.

    Returns:
        db_handle: The database handle.
        client: The MongoDB client object.
    """
    # Create a new client and connect to the server
    client = MongoClient(
        host=URI, server_api=ServerApi("1"), ssl_cert_reqs=ssl.CERT_NONE
    )

    # Send a ping to confirm a successful connection
    try:
        client.admin.command("ping")
        print("Pinged your deployment. You successfully connected to MongoDB!")
    except Exception as e:
        print(e)

    db_handle = client[db_name]
    return db_handle, client
