import json

from google.cloud import storage,datastore


def import_from_gcs_to_datastore():
    # create storage client
    storage_client = storage.Client.from_service_account_json('/home/puja/Downloads/tripbot-cloud-dda1f4e5fdab.json')
    # get bucket with name
    bucket = storage_client.get_bucket('data-import-gcs')
    project_id = 'tripbot-cloud'
    # get bucket data as blob
    blob = bucket.get_blob('doc1.json')

    # convert to string
    json_data_string = blob.download_as_string().decode('utf-8').replace("'", '"')
    data = json.loads(json_data_string)
    # create datastore entity
    imported_json = datastore.Entity(key=datastore.Client(project_id).key("data"))
    # update datastore entity with the imported json
    imported_json.update(data)
    datastore.Client(project_id).put(imported_json)


import_from_gcs_to_datastore()