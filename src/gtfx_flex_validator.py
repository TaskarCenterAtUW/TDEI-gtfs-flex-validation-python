import uuid
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
        self.listening_topic = Core.get_topic(topic_name=settings.subscription_topic_name, callback=self.process)
        self.publish_topic = Core.get_topic(topic_name=settings.publishing_topic_name)
        self.logger = Core.get_logger()
        self.listening_topic.subscribe(subscription=settings.subscription_name)

    def process(self, instance):
        message = instance.get_messages()
        if message is not None:
            gtfs_upload_message = QueueMessage.to_dict(message)
            upload_message = GTFSFlexUpload.data_from(gtfs_upload_message)
            file_upload_path = upload_message.data.file_upload_path
            file_relative_path = file_upload_path.split('/')[-1]
            if file_relative_path:
                validation = Validation(file_name=file_relative_path)
                is_file_valid = validation.is_valid
                validation_message = validation.validation_message
                self.send_status(valid=is_file_valid, upload_message=upload_message,
                                 validation_message=validation_message)
        else:
            print('No Message')

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
