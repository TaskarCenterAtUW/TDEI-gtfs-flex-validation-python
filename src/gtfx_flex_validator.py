import os
import uuid
import urllib.parse
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from .config import Settings
from .validation import Validation
from .serializer.gtfx_flex_serializer import GTFSFlexUpload

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
ASSETS_FILE_PATH = os.path.join(ROOT_DIR, 'assets')


def download_local(file_upload_path=None):
    storage_client = Core.get_storage_client()
    file = storage_client.get_file_from_url('gtfsflex', file_upload_path)
    try:
        if file.file_path:
            file_name = file.file_path.split('/')[-1]
            with open(f'{ASSETS_FILE_PATH}/{file_name}', 'wb') as blob:
                blob.write(file.get_stream())
            print(f'File download to location: {ASSETS_FILE_PATH}/{file_name}')
        else:
            print('File not found!')
    except Exception as e:
        print(e)


class GTFSFlexValidator:
    _settings = Settings()

    def __init__(self):
        Core.initialize()
        settings = Settings()
        self._subscription_name = settings.subscription_name
        self.listening_topic = Core.get_topic(topic_name=settings.subscription_topic_name)
        self.publish_topic = Core.get_topic(topic_name=settings.publishing_topic_name)
        self.logger = Core.get_logger()
        self.subscribe()

    def subscribe(self):
        def process(message):
            if message is not None:
                gtfs_upload_message = QueueMessage.to_dict(message)
                upload_message = GTFSFlexUpload.data_from(gtfs_upload_message)
                file_upload_path = urllib.parse.unquote(upload_message.data.file_upload_path)
                if file_upload_path:
                    validation = Validation(file_path=file_upload_path)
                    self.send_status(valid=validation.is_valid, upload_message=upload_message,
                                     validation_message=validation.validation_message)
                    # Example to get the stream of a file
                    # Uncomment the below code to download the file in local machine
                    # download_local(file_upload_path=file_upload_path)
            else:
                print('No Message')

        self.listening_topic.subscribe(subscription=self._subscription_name, callback=process)

    def send_status(self, valid: bool, upload_message: GTFSFlexUpload, validation_message: str = ''):
        upload_message.data.is_valid = valid
        upload_message.data.validation_message = validation_message if not valid else ''
        message_id = uuid.uuid1().hex[0:24]
        print(f'Publishing new message with ID: {message_id}')
        data = QueueMessage.data_from({
            'messageId': message_id,
            'message': 'Validation complete',
            'messageType': 'gtfsflexvalidation',
            'data': upload_message.data.to_json()
        })
        self.publish_topic.publish(data=data)
        return
