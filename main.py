import os
import json
from google.cloud import storage, datastore

PROJECT_ID = os.getenv('PROJECT_ID')
SERVICE_ACCOUNT_JSON = os.getenv('SERVICE_ACCOUNT_JSON')
BUCKET_NAME = os.getenv('BUCKET_NAME')


def main():
    # create storage client
    storage_client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_JSON)
    # get bucket with name
    bucket = storage_client.get_bucket(BUCKET_NAME)
    # get bucket data as blob
    blob = bucket.get_blob('doc4.json')
    data = json.loads(blob.download_as_string())
    # create datastore entity
    imported_json = datastore.Entity(key=datastore.Client(PROJECT_ID).key("data"))
    # update datastore entity with the imported json
    imported_json.update(data)
    datastore.Client(PROJECT_ID).put(imported_json)


def query_entity():
    entities = datastore.Client(PROJECT_ID).query(kind="data")
    entities.add_filter("ContentsList.L5", "=", "Power button")
    entities_list = list(entities.fetch())
    if not entities_list:
        print("No result is returned")
    else:
        for i in entities_list:
            print(i["DocumentNo"])


if __name__ == "__main__":
    query_entity()
