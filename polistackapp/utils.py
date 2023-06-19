from pymongo import MongoClient


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
    client = MongoClient(host=host, port=port)
    db_handle = client[db_name]
    return db_handle, client
