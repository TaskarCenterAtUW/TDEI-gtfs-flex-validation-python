import os
import json
import uuid
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_FILE_PATH = os.path.join(ROOT_DIR, 'assets')


def send(settings=None):
    publish_topic = Core.get_topic(topic_name=settings.subscription_topic_name)
    file_data = open(f'{ASSETS_FILE_PATH}/msg-gtfs-flex-upload.json')
    upload_data = json.load(file_data)
    message_id = uuid.uuid1().hex[0:24]
    print(f'Publishing new message with ID: {message_id} \n')
    upload_data['messageId'] = message_id
    data = QueueMessage.data_from(upload_data)
    publish_topic.publish(data=data)
    return message_id
