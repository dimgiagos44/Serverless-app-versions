from minio import Minio
import urllib3
import uuid
import json
import sys
import io

client = Minio(
        "10.102.201.185:80",
        access_key="7bde2761-ccfe-4c09-9018-15198e31caaf",
        secret_key="7ed4980e-9480-4eb0-a507-fe44f60c4470",
        secure=False,
        http_client=urllib3.PoolManager(cert_reqs="CERT_NONE")
)

def unique_name(name):
        name, extension = name.split('.')
        return '{name}.{random}.{extension}'.format(
                    name=name,
                    extension=extension,
                    random=str(uuid.uuid4()).split('-')[0]
                )

def download_stream(bucket, file):
        data = client.get_object(bucket, file)
        return data.read()

def upload_stream(bucket, file, bytes_data):
        key_name = unique_name(file)
        client.put_object(bucket, key_name, bytes_data, bytes_data.getbuffer().nbytes)
        return key_name

def handle(req):
    output_bucket = 'mybucket'
    data = req 
    #data = '[{"Data":[{"predictions":["stage","caldron","breastplate"],"bucket":"image-output","key":"frame.802fb3e3.jpg"}]},{"Data":[{"predictions":["web_site","analog_clock","cornet"],"bucket":"image-output","key":"frame.c683e1fd.jpg"}]},{"Data":[{"predictions":[],"bucket":"image-output","key":"frame.4b53f36f.jpg"}]}]'
    data_as_bytes = data.encode()
    key = 'version1.result'
    key_name = upload_stream(output_bucket, key, io.BytesIO(data_as_bytes))

    
    return key_name

