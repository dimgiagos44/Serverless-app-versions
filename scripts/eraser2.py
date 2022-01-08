import json
import sys
from minio import Minio
import urllib3
from datetime import datetime, timedelta, tzinfo

client = Minio(
        "10.102.201.185:80",
        access_key="7bde2761-ccfe-4c09-9018-15198e31caaf",
        secret_key="7ed4980e-9480-4eb0-a507-fe44f60c4470",
        secure=False,
        http_client=urllib3.PoolManager(cert_reqs="CERT_NONE")
)

objects = client.list_objects('mybucket')
#minutes period to be deleted
minutes = int(sys.argv[1])
for object in objects:
        if (datetime.now(object._last_modified.tzinfo) - timedelta(minutes=minutes) < object._last_modified):
                client.remove_object('mybucket', object._object_name)