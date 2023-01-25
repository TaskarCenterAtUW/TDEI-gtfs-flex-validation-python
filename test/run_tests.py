import os
import sys
import datetime
import json
import uuid
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from pydantic import BaseSettings

# Code to import to grandparent  module
current = os.path.dirname(os.path.realpath(__file__))
parent = os.path.dirname(current)
sys.path.append(parent)

from src import gtfs_flex_validation

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
SRC_DIR = os.path.join(parent, 'src')
TEST_JSON_FILE = os.path.join(ROOT_DIR, 'tests.json')


class Settings(BaseSettings):
    subscription_topic_name: str = os.environ.get('UPLOAD_TOPIC', None)
    publishing_topic_name: str = os.environ.get('VALIDATION_TOPIC', None)
    subscription_name: str = os.environ.get('UPLOAD_SUBSCRIPTION', None)
    validation_topic: str = os.environ.get('VALIDATION_TOPIC', None)
    container_name: str = os.environ.get('CONTAINER_NAME', None)


def post_message_to_topic(msg: dict, settings: Settings):
    publish_topic = Core.get_topic(topic_name=settings.publishing_topic_name)
    data = QueueMessage.data_from(msg)
    publish_topic.publish(data=data)


def do_test(test, settings: Settings):
    print(f'Performing tests :{test["Name"]}')
    storage_client = Core.get_storage_client()

    container = storage_client.get_container(container_name=settings.container_name)
    basename = os.path.basename(test['Input_file'])

    suffix = datetime.datetime.now().strftime("%y%m%d_%H%M%S")

    base_name, base_ext = os.path.splitext(basename)
    file_name = "_".join([base_name, suffix]) + base_ext
    test_file = container.create_file(file_name)  # Removed mime-type
    with open(os.path.join(ROOT_DIR, test['Input_file']), 'rb') as data:
        test_file.upload(data)
        # FIXED: get the remote url
        blob_url = test_file.get_remote_url()
        print(f'Performing tests :{test["Name"]}:{blob_url}')
        message_id = uuid.uuid1().hex[0:24]
        # # prepare upload message
        # data = {
        #     'messageId': message_id,
        #     'messageType': 'gtfsflex',  # Change the messageType
        #     'message': 'New Data published for theOrganization:101',  # Change the message
        #     'data': {
        #         'tdei_org_id': '2CA2AA83-B99A-42E2-90AA-C187EAC48FEB',
        #         'tdei_service_id': '8EF615EF-28AB-444B-82D3-0E62E3692382',
        #         'collected_by': '6D3E5B8C-FB16-4B6A-9436-72FD24756CC9',
        #         'collection_date': '2022-11-22T09:43:07.978Z',
        #         'collection_method': 'manual',
        #         'valid_from': '2022-11-22T09:43:07.978Z',
        #         'valid_to': '2022-11-22T09:43:07.978Z',
        #         'data_source': 'local',
        #         'flex_schema_version': '1.0.0',
        #         'file_upload_path': blob_url or '',
        #         'user_id': '101-1-2-2111',
        #         'tdei_record_id': '4CA2AA83-B99A-1234-90AA-C187EAC48FEB',
        #         'polygon': {}
        #     }
        # }
        # post_message_to_topic(data, settings)
        # OR Read the uploaded message from file
        with open(os.path.join(SRC_DIR, test['Input_Message']), 'rb') as msg_file:
            data = json.load(msg_file)
            data['file_upload_path'] = blob_url or ''
            upload_message = {
                'messageId': message_id,
                'message': 'Some message',  # Change the message
                'messageType': 'Some messageType',  # Change the messageType
                'data': data
            }
            post_message_to_topic(upload_message, settings)

        # TODO: remove direct access to the validation
        #     listen to the topic that validation service posts to
        #      when receive message. check for msg[data[is_valid] & data[message]]
        validator = gtfs_flex_validation.GTFSFlexValidation(file_path=blob_url).validate()
        validation_data = test['Output']
        if validation_data['valid'] == str(validator[0]):
            print(f'Performing tests :{test["Name"]}:PASSED\n')
        else:
            print(f'Performing tests :{test["Name"]}:FAILED\n')


def test_harness():
    # Initialize core..
    Core.initialize()
    settings = Settings()
    with open(TEST_JSON_FILE) as test_file:
        tests = json.load(test_file)
        for test in tests['Tests']:
            do_test(test, settings)


if __name__ == "__main__":
    print(f'Performing tests :')
    test_harness()
