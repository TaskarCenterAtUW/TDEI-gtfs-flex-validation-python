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
        core = Core()
        settings = Settings()
        self._subscription_name = settings.subscription_name
        self.listening_topic = core.get_topic(topic_name=settings.subscription_topic_name)
        self.publish_topic = core.get_topic(topic_name=settings.publishing_topic_name)
        self.logger = core.get_logger()
        self.subscribe()

    def subscribe(self) -> None:
        # Process the incoming message
        def process(message) -> None:
            if message is not None:
                gtfs_upload_message = QueueMessage.to_dict(message)
                upload_message = GTFSFlexUpload.data_from(gtfs_upload_message)
                file_upload_path = urllib.parse.unquote(upload_message.data.meta.file_upload_path)
                print(f'Received message for Record: {upload_message.data.tdei_record_id}')
                if file_upload_path:
                    # Do the validation in the other class
                    validator = GTFSFlexValidation(file_path=file_upload_path)
                    validation = validator.validate()
                    self.send_status(valid=validation[0], upload_message=upload_message,
                                     validation_message=validation[1])
                else:
                    print('No file Path found in message!')
            else:
                print('No Message')

        self.listening_topic.subscribe(subscription=self._subscription_name, callback=process)

    def send_status(self, valid: bool, upload_message: GTFSFlexUpload, validation_message: str = '') -> None:
        upload_message.data.stage = 'Flex-Validation'
        upload_message.data.meta.isValid = valid
        upload_message.data.meta.validationMessage = validation_message or 'Validation successful'
        upload_message.data.response.success = valid
        upload_message.data.response.message = validation_message or 'Validation successful'
        message_id = uuid.uuid1().hex[0:24]
        print(f'Publishing new message with ID: {message_id}')
        data = QueueMessage.data_from({
            'messageId': message_id,
            'message': upload_message.message or 'Validation complete',
            'messageType': 'gtfs-flex-validation',
            'data': upload_message.data.to_json()
        })
        self.publish_topic.publish(data=data)
        return
