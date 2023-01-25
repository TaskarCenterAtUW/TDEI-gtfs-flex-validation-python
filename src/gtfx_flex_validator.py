import os
import uuid
import urllib.parse
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from .config import Settings
from .gtfs_flex_validation import GTFSFlexValidation
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

    def subscribe(self) -> None:
        # Process the incoming message
        def process(message) -> None:
            if message is not None:
                gtfs_upload_message = QueueMessage.to_dict(message)
                upload_message = GTFSFlexUpload.data_from(gtfs_upload_message)
                file_upload_path = urllib.parse.unquote(upload_message.data.file_upload_path)
                if file_upload_path:
                    # Do the validation in the other class
                    validator = GTFSFlexValidation(file_path=file_upload_path)
                    validation = validator.validate()
                    self.send_status(valid=validation[0], upload_message=upload_message,
                                     validation_message=validation[1])
            else:
                print('No Message')

        self.listening_topic.subscribe(subscription=self._subscription_name, callback=process)

    def send_status(self, valid: bool, upload_message: GTFSFlexUpload, validation_message: str = '') -> None:
        upload_message.data.is_valid = valid
        upload_message.data.validation_message = validation_message if not valid else ''
        message_id = uuid.uuid1().hex[0:24]
        print(f'Publishing new message with ID: {message_id}')
        data = QueueMessage.data_from({
            'messageId': message_id,
            'message': upload_message.message or 'Validation complete',
            'messageType': 'gtfsflexvalidation',
            'data': upload_message.data.to_json()
        })
        self.publish_topic.publish(data=data)
        return
