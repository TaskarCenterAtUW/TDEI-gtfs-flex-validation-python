from python_ms_core import Core
from .config import Settings
from .monitor import Monitor


class GTFSFlexValidator:

    def __init__(self):
        Core.initialize()
        settings = Settings()
        self.listening_topic = Core.get_topic(topic_name=settings.listening_topic_name)
        self.logger = Core.get_logger()
        self.subscription = Monitor
        self.monitor = Monitor(30, self.listening_topic.subscribe, subscription=settings.upload_subscription)
