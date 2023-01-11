import os
from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()


class Settings(BaseSettings):
    app_name: str = 'gtfs-flex-validation-service-python'
    listening_topic_name: str = os.environ.get('UPLOAD_TOPIC', None)
    publishing_topic_name: str = os.environ.get('VALIDATION_TOPIC', None)
    upload_subscription: str = os.environ.get('UPLOAD_SUBSCRIPTION', None)
    validation_topic: str = os.environ.get('VALIDATION_TOPIC', None)
