import unittest
from unittest.mock import MagicMock, patch, call
from src.gtfx_flex_validator import GTFSFlexValidator


class TestGTFSFlexValidator(unittest.TestCase):

    @patch('src.gtfx_flex_validator.Settings')
    @patch('src.gtfx_flex_validator.Core')
    def setUp(self, mock_core, mock_settings):
        mock_settings.return_value.request_subscription = 'test_subscription'
        mock_settings.return_value.request_topic_name = 'test_request_topic'
        mock_settings.return_value.response_topic_name = 'test_response_topic'
        mock_settings.return_value.max_concurrent_messages = 10
        mock_settings.return_value.get_unique_id.return_value = '123'
        mock_settings.return_value.container_name = 'test_container'

        # Mock Core
        mock_core.return_value.get_topic.return_value = MagicMock()
        mock_core.return_value.get_storage_client.return_value = MagicMock()

        # Initialize GTFSFlexValidator with mocked dependencies
        self.validator = GTFSFlexValidator()
        self.validator.storage_client = MagicMock()
        self.validator.container_name = 'test_container'
        self.sample_message = {
            'messageId': '1234',
            'data': {
                'file_upload_path': 'https://tdeisamplestorage.blob.core.windows.net/gtfsflex/tests/success_1_all_attrs.zip',
                'user_id': 'c59d29b6-a063-4249-943f-d320d15ac9ab',
                'tdei_project_group_id': '0b41ebc5-350c-42d3-90af-3af4ad3628fb'
            }
        }

    @patch('src.gtfx_flex_validator.QueueMessage')
    @patch('src.gtfx_flex_validator.FileUploadMsg')
    def test_subscribe_with_valid_message(self, mock_request_message, mock_queue_message):
        # Arrange
        mock_message = MagicMock()
        mock_queue_message.to_dict.return_value = self.sample_message
        mock_request_message.from_dict.return_value = mock_request_message
        self.validator.process_message = MagicMock()

        # Act
        self.validator.subscribe()
        callback = self.validator.request_topic.subscribe.call_args[1]['callback']
        callback(mock_message)

        # Assert
        self.validator.process_message.assert_called_once_with(mock_request_message)


    @patch('src.gtfx_flex_validator.GTFSFlexValidation')
    def test_process_message_with_valid_file_path(self, mock_gtfs_flex_validation):
        # Arrange
        mock_request_message = MagicMock()
        mock_request_message.data.file_upload_path = 'test_dataset_url'
        mock_request_message.data.user_id = 'user_id'
        mock_request_message.data.tdei_project_group_id = 'tdei_project_group_id'
        mock_gtfs_flex_validation_instance = mock_gtfs_flex_validation.return_value
        mock_gtfs_flex_validation_instance.validate.return_value = True, 'Validation successful'

        self.validator.send_status = MagicMock()

        # Act
        self.validator.process_message(mock_request_message)

        # Assert

        self.validator.send_status.assert_called_once_with(valid=True, upload_message=mock_request_message,
                                                         validation_message='Validation successful')

    @patch('src.gtfx_flex_validator.GTFSFlexValidation')
    def test_process_message_when_file_path_is_none_and_valid_is_false(self, mock_gtfs_flex_validation):
        # Arrange
        mock_request_message = MagicMock()
        mock_request_message.data.file_upload_path = 'test_dataset_url'
        mock_request_message.data.user_id = 'user_id'
        mock_request_message.data.tdei_project_group_id = 'tdei_project_group_id'
        mock_gtfs_flex_validation.return_value.validate.return_value = False, 'Validation error'
        self.validator.send_status = MagicMock()

        # Act
        self.validator.process_message(mock_request_message)

        self.validator.send_status.assert_called_once_with(
            valid=False,
            upload_message=mock_request_message,
            validation_message='Validation error'
        )


    @patch('src.gtfx_flex_validator.GTFSFlexValidation')
    def test_process_message_when_exception_is_raised(self, mock_gtfs_flex_validation):
        # Arrange
        mock_request_message = MagicMock()
        mock_request_message.data.file_upload_path = 'test_dataset_url'
        mock_request_message.data.user_id = 'user_id'
        mock_request_message.data.tdei_project_group_id = 'tdei_project_group_id'
        self.validator.send_status = MagicMock()

        # Mock Inclination to raise an exception
        mock_gtfs_flex_validation.side_effect = Exception('Some error occurred')

        # Act
        self.validator.process_message(mock_request_message)

        # Assert
        self.validator.send_status.assert_called_once_with(
            valid=False,
            upload_message=mock_request_message,
            validation_message='Some error occurred'
        )

    @patch('src.gtfx_flex_validator.QueueMessage')
    def test_send_status_success(self, mock_queue_message):
        # Arrange
        mock_request_message = MagicMock()
        mock_response_topic = self.validator.core.get_topic.return_value
        mock_data = {'messageId': '1234', 'messageType': 'test', 'data': {'success': True}}
        mock_queue_message.data_from.return_value = mock_data

        # Act
        self.validator.send_status(
            valid=True,
            upload_message=mock_request_message,
            validation_message='Validation successful'
        )

        # Assert
        mock_queue_message.data_from.assert_called_once()
        mock_response_topic.publish.assert_called_once_with(data=mock_data)


if __name__ == '__main__':
    unittest.main()
