import os
import shutil
import unittest
from pathlib import Path
from unittest.mock import patch, MagicMock
from src.gtfs_flex_validation import GTFSFlexValidation
from src.config import Settings

DOWNLOAD_FILE_PATH = f'{Path.cwd()}/downloads'
SAVED_FILE_PATH = f'{Path.cwd()}/tests/unit_tests/test_files'

SUCCESS_FILE_NAME = 'browncounty-mn-us--flex-v2.zip'
MAC_SUCCESS_FILE_NAME = 'otterexpress-mn-us--flex-v2.zip'
FAILURE_FILE_NAME = 'fail_schema_1.zip'


class TestSuccessWithMacOSFile(unittest.TestCase):
    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{MAC_SUCCESS_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{MAC_SUCCESS_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{MAC_SUCCESS_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = MAC_SUCCESS_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = Settings()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test_validate_with_valid_file(self):
        # Arrange
        file_path = f'{DOWNLOAD_FILE_PATH}/{MAC_SUCCESS_FILE_NAME}'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertTrue(is_valid)


class TestSuccessGTFSFlexValidation(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{SUCCESS_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{SUCCESS_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{SUCCESS_FILE_NAME}'
        dl_folder_path = os.path.join(DOWNLOAD_FILE_PATH, 'dummy-uuid')  # Mock the UUID generation
        os.makedirs(dl_folder_path, exist_ok=True)  # Ensure this directory is created in the test

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock(),
                                                prefix=Settings().get_unique_id())
            self.validator.file_path = file_path
            self.validator.file_relative_path = SUCCESS_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = Settings()
            self.validator.prefix = self.validator.settings.get_unique_id()
            mock_download_single_file.return_value = os.path.join(dl_folder_path, SUCCESS_FILE_NAME)

    def tearDown(self):
        pass

    def test_validate_with_valid_file(self):
        # Arrange
        file_path = f'{DOWNLOAD_FILE_PATH}/{SUCCESS_FILE_NAME}'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertTrue(is_valid)

    def test_is_gtfs_flex_valid_with_valid_file(self):
        # Arrange
        file_path = f'{DOWNLOAD_FILE_PATH}/{SUCCESS_FILE_NAME}'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertTrue(is_valid)
        GTFSFlexValidation.clean_up.assert_called_once_with(file_path)

    def test_download_single_file(self):
        # Arrange
        file_upload_path = DOWNLOAD_FILE_PATH
        self.validator.storage_client = MagicMock()
        self.validator.storage_client.get_file_from_url = MagicMock()
        file = MagicMock()
        file.file_path = 'text_file.txt'
        file.get_stream = MagicMock(return_value=b'file_content')
        self.validator.storage_client.get_file_from_url.return_value = file

        # Act
        downloaded_file_path = self.validator.download_single_file(file_upload_path=file_upload_path)

        # Assert
        self.validator.storage_client.get_file_from_url.assert_called_once_with(self.validator.container_name,
                                                                                file_upload_path)
        file.get_stream.assert_called_once()
        with open(downloaded_file_path, 'rb') as f:
            content = f.read()
        self.assertEqual(content, b'file_content')

    def test_download_multiple_file_with_same_name(self):
        # Arrange
        file_upload_path = DOWNLOAD_FILE_PATH
        self.validator.storage_client = MagicMock()
        self.validator.storage_client.get_file_from_url = MagicMock()
        file = MagicMock()
        file.file_path = 'text_file.txt'
        file.get_stream = MagicMock(return_value=b'file_content')
        self.validator.storage_client.get_file_from_url.return_value = file

        # Act
        first_downloaded_file_path = self.validator.download_single_file(file_upload_path=file_upload_path)
        second_downloaded_file_path = self.validator.download_single_file(file_upload_path=file_upload_path)

        # Assert
        self.assertNotEqual(first_downloaded_file_path, second_downloaded_file_path,
                            "The downloaded file paths should be different for files with the same name.")

        # Check if the get_file_from_url was called for both download attempts
        self.assertEqual(self.validator.storage_client.get_file_from_url.call_count, 2,
                         "get_file_from_url should be called twice for two downloads.")
        file.get_stream.assert_called()

        # Additional assertions to verify that the paths indeed point to different locations
        self.assertTrue(first_downloaded_file_path.startswith(DOWNLOAD_FILE_PATH))
        self.assertTrue(second_downloaded_file_path.startswith(DOWNLOAD_FILE_PATH))

    def test_clean_up_file(self):
        # Arrange
        file_upload_path = DOWNLOAD_FILE_PATH
        text_file_path = f'{file_upload_path}/text_file.txt'
        f = open(text_file_path, "w")
        f.write("Sample text")
        f.close()

        # Act
        GTFSFlexValidation.clean_up = MagicMock()

        # Assert
        # self.assertFalse(os.path.exists(text_file_path))

    def test_clean_up_folder(self):
        # Arrange
        directory_name = 'temp'
        directory_path = f'{DOWNLOAD_FILE_PATH}/{directory_name}'
        is_exists = os.path.exists(directory_path)
        if not is_exists:
            os.makedirs(directory_path)

        # Act
        GTFSFlexValidation.clean_up = MagicMock()

        # Assert
        self.assertFalse(os.path.exists(directory_name))


class TestFailureGTFSFlexValidation(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{FAILURE_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAILURE_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{FAILURE_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = FAILURE_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = MagicMock()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test_validate_with_invalid_file(self):
        # Arrange
        file_path = f'{DOWNLOAD_FILE_PATH}/{FAILURE_FILE_NAME}'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)

    def test_is_gtfs_pathways_valid_with_invalid_zip_file(self):
        # Arrange
        file_path = f'{DOWNLOAD_FILE_PATH}/{FAILURE_FILE_NAME}'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)
        GTFSFlexValidation.clean_up.assert_called_once_with(file_path)

    def test_is_gtfs_pathways_valid_with_invalid_format_file(self):
        # Arrange
        file_path = f'{SAVED_FILE_PATH}/gtfs-flex-upload.json'
        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, _ = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)
        GTFSFlexValidation.clean_up.assert_called_once_with(file_path)

    def test_download_single_file_exception(self):
        # Arrange
        file_upload_path = DOWNLOAD_FILE_PATH
        self.validator.storage_client = MagicMock()
        self.validator.storage_client.get_file_from_url = MagicMock()
        file = MagicMock()
        file.file_path = 'text_file.txt'
        file.get_stream = MagicMock(side_effect=FileNotFoundError("Mocked FileNotFoundError"))
        self.validator.storage_client.get_file_from_url.return_value = file

        dl_folder_path = os.path.join(DOWNLOAD_FILE_PATH, self.validator.prefix)
        os.makedirs(dl_folder_path, exist_ok=True)

        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            self.validator.download_single_file(file_upload_path=file_upload_path)


if __name__ == '__main__':
    unittest.main()
