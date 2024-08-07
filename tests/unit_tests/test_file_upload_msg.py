import os
import json
import unittest
from src.models.file_upload_msg import FileUploadMsg
# from src.gtfx_flex_validator import GTFSFlexValidator

current_dir = os.path.dirname(os.path.abspath(os.path.join(__file__, '../')))
parent_dir = os.path.dirname(current_dir)

TEST_JSON_FILE = os.path.join(parent_dir, 'src/assets/request-msg.json')
TEST_FILE = open(TEST_JSON_FILE)
TEST_DATA = json.loads(TEST_FILE.read())

class TestFileUploadMsg(unittest.TestCase):
    def setUp(self):
        data = TEST_DATA
        self.upload = FileUploadMsg.from_dict(data=data)
    
    def test_message_type(self):
        self.assertEqual(self.upload.messageType,"workflow_identifier")
    def test_message_id(self):
        self.upload.messageId = "abc"
        self.assertEqual(self.upload.messageId,"abc")
    def test_file_upload_path(self):
        self.assertEqual(self.upload.data.file_upload_path,'https://tdeisamplestorage.blob.core.windows.net/gtfsflex/tests/success_1_all_attrs.zip')


if __name__ == '__main__':
    unittest.main()
