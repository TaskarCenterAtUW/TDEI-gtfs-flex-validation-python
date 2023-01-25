import json
from python_ms_core import Core
from pydantic import BaseSettings
import os
import datetime

class Settings(BaseSettings):
    subscription_topic_name: str = os.environ.get('UPLOAD_TOPIC', None)
    publishing_topic_name: str = os.environ.get('VALIDATION_TOPIC', None)
    subscription_name: str = os.environ.get('UPLOAD_SUBSCRIPTION', None)
    validation_topic: str = os.environ.get('VALIDATION_TOPIC', None)
    container_name: str = os.environ.get('CONTAINER_NAME', None)

def do_test(test, settings: Settings):
    #upload test["Input_file"] to blob storage
    
    print(test)
    print("Performing test: ", test["Name"])
    storage_client = Core.get_storage_client()

    container = storage_client.get_container(container_name=settings.container_name)
    basename = os.path.basename(test["Input_file"])

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    base_name, base_ext = os.path.splitext(basename)
    file_name = "_".join([base_name, suffix])+base_ext
    test_file = container.create_file(file_name, 'txt/plain')
    with open(test["Input_file"], "rb") as data:
        test_file.upload(data)

    # TODO: get the remote url
    # blob_url = test_file.get_remote_url()

    #prepare upload message
    #post upload message to the topic
    with open("../src/assets/msg-gtfs-flex-upload.json") as msgfile:
        upload_message = json.load(msgfile)
    # print(upload_message)

    # TODO: replace the file_upload_path in the upload_message with the blob_url
    #   post the message to the upload_topic
    #   wait for the response message from the validation topic
    #   check if the validation results from the message is same as test["Output"]


def test_harness():
    #Initialize core..
    Core.initialize()
    settings = Settings() 

    with open("./tests.json") as test_file:
        tests = json.load(test_file)
        # print(tests)
    
    for test in tests["Tests"]:
        do_test(test, settings)

if __name__ == "__main__":
    print("Hello")
    test_harness()
