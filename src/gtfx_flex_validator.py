import uuid
import urllib.parse
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from .config import Settings
from .validation import Validation
from .serializer.gtfx_flex_serializer import GTFSFlexUpload


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
        self.storage_client = Core.get_storage_client()

    def subscribe(self):
        def process(message):
            if message is not None:
                gtfs_upload_message = QueueMessage.to_dict(message)
                upload_message = GTFSFlexUpload.data_from(gtfs_upload_message)
                file_upload_path = urllib.parse.unquote(upload_message.data.file_upload_path)
                if file_upload_path:
                    validation = Validation(file_path=file_upload_path)
                    is_file_valid = validation.is_valid
                    if is_file_valid:
                        # Example to get the stream of a file
                        self.get_file(file_upload_path=file_upload_path)

                    validation_message = validation.validation_message
                    self.send_status(valid=is_file_valid, upload_message=upload_message,
                                     validation_message=validation_message)
            else:
                print('No Message')

        self.listening_topic.subscribe(subscription=self._subscription_name, callback=process)

    def get_file(self, file_upload_path=None):
        file_path = file_upload_path
        if 'http' in file_upload_path:
            file_path = '/'.join(urllib.parse.unquote(file_upload_path).split('/')[4:])

        container = self.storage_client.get_file('gtfsflex', file_path)
        # Uncomment the below line to read the stream
        # body = container.get_stream()

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
