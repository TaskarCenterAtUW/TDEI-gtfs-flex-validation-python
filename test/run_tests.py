import os
import datetime
import json
import uuid
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from pydantic import BaseSettings

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
TEST_JSON_FILE = os.path.join(ROOT_DIR, 'tests.json')
TEST_FILE = open(TEST_JSON_FILE)
TEST_DATA = json.loads(TEST_FILE.read())

TESTS = TEST_DATA['Tests']


class Settings(BaseSettings):
    publishing_topic_name: str = os.environ.get('UPLOAD_TOPIC', None)
    subscription_topic_name: str = os.environ.get('VALIDATION_TOPIC', None)
    subscription_name: str = os.environ.get('VALIDATION_SUBSCRIPTION', None)
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

    input_file = os.path.join(ROOT_DIR, test['Input_file'])
    # Uploading file to blob storage
    with open(input_file, 'rb') as msg_file:
        test_file.upload(msg_file)
        # FIXED: get the remote url
        blob_url = test_file.get_remote_url()
        print(f'Performing tests :{test["Name"]}:{blob_url}')
    message_id = uuid.uuid1().hex[0:24]
    # Reading the input file
    input_data = open(input_file)
    data = json.load(input_data)
    data['file_upload_path'] = blob_url or ''
    data['message'] = test['Name']
    upload_message = {
        'messageId': message_id,
        'message': test['Name'],
        'messageType': 'Some messageType',  # Change the messageType
        'data': data
    }
    # post_message_to_topic(data, settings)
    # OR Read the uploaded message from file
    # prepare upload message
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

    # Publishing message to topic
    post_message_to_topic(upload_message, settings)


def subscribe(settings: Settings):
    def process(message) -> None:
        parsed_message = message.__dict__
        message = parsed_message['message']
        parsed_data = parsed_message['data']
        test_detail = [item for item in TESTS if item.get('Name') == message]
        if len(test_detail) > 0:
            if test_detail[0]['Output']['valid'] == parsed_data['is_valid']:
                print(f'Performing tests :{message}:PASSED\n')
            else:
                print(f'Performing tests :{message}:FAILED\n')
        else:
            print(parsed_message)
            print('Some other message received \n')

    listening_topic = Core.get_topic(topic_name=settings.subscription_topic_name)
    listening_topic.subscribe(subscription=settings.subscription_name, callback=process)


def test_harness():
    # Initialize core..
    Core.initialize()
    settings = Settings()
    subscribe(settings=settings)
    for test in TESTS:
        do_test(test, settings)


if __name__ == "__main__":
    print(f'Performing tests :')
    test_harness()
