import json
import os
from google.cloud import storage, datastore
from dotenv import load_dotenv
load_dotenv()


def main():
    # create storage client
    storage_client = storage.Client.from_service_account_json(os.getenv('service_account_json'))
    # get bucket with name
    bucket = storage_client.get_bucket(os.getenv('bucket_name'))
    project_id = os.getenv('project_id')
    # get bucket data as blob
    blob = bucket.get_blob('doc1.json')
    data = json.loads(blob.download_as_string())
    # create datastore entity
    imported_json = datastore.Entity(key=datastore.Client(project_id).key("data"))
    # update datastore entity with the imported json
    imported_json.update(data)
    datastore.Client(project_id).put(imported_json)


if __name__ == "__main__":
    main()
