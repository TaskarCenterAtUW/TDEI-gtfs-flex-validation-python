import uuid
import urllib.parse
from python_ms_core import Core
from python_ms_core.core.queue.models.queue_message import QueueMessage
from .config import Settings
from .serializer.gtfx_flex_serializer import GTFSFlexUpload


class Validation:
    def __init__(self, message):
        settings = Settings()
        self.publishing_topic = Core.get_topic(topic_name=settings.publishing_topic_name)
        if len(message) > 0:
            gtfs_upload_message = QueueMessage.to_dict(message)
            for msg in gtfs_upload_message:
                upload_message = GTFSFlexUpload.data_from(msg.__dict__)
                file_upload_path = upload_message.data.file_upload_path
                file_relative_path = file_upload_path.split('/')[-1]
                if file_relative_path:
                    file_path_clean = urllib.parse.unquote(file_relative_path)
                    file_name = file_path_clean.split('/')[-1]

                    if file_name.find('invalid') != -1:
                        print('Invalid file')
                        self.send_status(valid=False, upload_message=upload_message, validation_message='Invalid file')
                    elif file_name.find('valid') != -1:
                        print('Valid file')
                        self.send_status(valid=True, upload_message=upload_message)
                    else:
                        print('Invalid file.. No regex found')
                        self.send_status(valid=False, upload_message=upload_message,
                                         validation_message=f'No regex found in file {file_name}')
        else:
            print('No Message')

    def send_status(self, valid: bool, upload_message: GTFSFlexUpload, validation_message: str = ''):
        upload_message.data.is_valid = valid
        upload_message.data.validation_message = validation_message
        data = QueueMessage.data_from({
            'messageId': uuid.uuid1().hex[0:24],
            'message': 'Validation complete',
            'messageType': 'gtfsflexvalidation',
            'data': upload_message.data.to_json()
        })
        self.publishing_topic.publish(data=data)
