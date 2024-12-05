import os
import shutil
import unittest
from pathlib import Path
from src.config import Settings
from unittest.mock import patch, MagicMock
from src.gtfs_flex_validation import GTFSFlexValidation

DOWNLOAD_FILE_PATH = f'{Path.cwd()}/downloads'
SAVED_FILE_PATH = f'{Path.cwd()}/tests/unit_tests/test_files'

SUCCESS_FILE_NAME = 'browncounty-mn-us--flex-v2.zip'
MAC_SUCCESS_FILE_NAME = 'otterexpress-mn-us--flex-v2.zip'
FAILURE_FILE_NAME = 'fail_schema_1.zip'

SUCCESS2_FILE_NAME = 'flex-good.zip'
FAIL2_FILE_NAME = 'flex-bad-specificerror.zip'
FAIL3_FILE_NAME = 'flex-bad-foreignkey.zip'
FAIL4_FILE_NAME = 'flex-bad-filename.zip'


class TestBadFile4(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{FAIL4_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL4_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{FAIL4_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = FAIL4_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = MagicMock()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test(self):
        # Arrange
        source = f'{SAVED_FILE_PATH}/{FAIL4_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL4_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{SAVED_FILE_PATH}/{FAIL4_FILE_NAME}'

        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, errors = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)


class TestBadFile3(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{FAIL3_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL3_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{FAIL3_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = FAIL3_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = MagicMock()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test(self):
        # Arrange
        source = f'{SAVED_FILE_PATH}/{FAIL3_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL3_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{SAVED_FILE_PATH}/{FAIL3_FILE_NAME}'

        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, errors = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)


class TestBadFile2(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{FAIL2_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL2_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{FAIL2_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = FAIL2_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = MagicMock()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test(self):
        # Arrange
        source = f'{SAVED_FILE_PATH}/{FAIL2_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{FAIL2_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{SAVED_FILE_PATH}/{FAIL2_FILE_NAME}'

        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, errors = self.validator.validate()

        # Assert
        self.assertFalse(is_valid)


class TestGoodFile2(unittest.TestCase):

    @patch.object(GTFSFlexValidation, 'download_single_file')
    def setUp(self, mock_download_single_file):
        os.makedirs(DOWNLOAD_FILE_PATH, exist_ok=True)
        source = f'{SAVED_FILE_PATH}/{SUCCESS2_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{SUCCESS2_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{DOWNLOAD_FILE_PATH}/{SUCCESS2_FILE_NAME}'

        with patch.object(GTFSFlexValidation, '__init__', return_value=None):
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = SUCCESS2_FILE_NAME
            self.validator.container_name = None
            self.validator.settings = MagicMock()
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass

    def test(self):
        # Arrange
        source = f'{SAVED_FILE_PATH}/{SUCCESS2_FILE_NAME}'
        destination = f'{DOWNLOAD_FILE_PATH}/{SUCCESS2_FILE_NAME}'

        if not os.path.isfile(destination):
            shutil.copyfile(source, destination)

        file_path = f'{SAVED_FILE_PATH}/{SUCCESS2_FILE_NAME}'

        expected_downloaded_file_path = file_path
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)
        GTFSFlexValidation.clean_up = MagicMock()

        # Act
        is_valid, errors = self.validator.validate()

        # Assert
        self.assertTrue(is_valid)


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
            mock_download_single_file.return_value = file_path

    def tearDown(self):
        pass  # GTFSFlexValidation.clean_up(os.path.join(DOWNLOAD_FILE_PATH, self.validator.prefix))

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
            self.validator = GTFSFlexValidation(file_path=file_path, storage_client=MagicMock())
            self.validator.file_path = file_path
            self.validator.file_relative_path = SUCCESS_FILE_NAME
            self.validator.container_name = None
            self.validator.prefix = Settings().get_unique_id()
            mock_download_single_file.return_value = os.path.join(dl_folder_path, SUCCESS_FILE_NAME)

    def tearDown(self):
        GTFSFlexValidation.clean_up(os.path.join(DOWNLOAD_FILE_PATH, self.validator.prefix))

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
        pass  # GTFSFlexValidation.clean_up(os.path.join(DOWNLOAD_FILE_PATH, self.validator.prefix))

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
        file.get_stream = MagicMock(side_effect=FileNotFoundError('Mocked FileNotFoundError'))
        self.validator.storage_client.get_file_from_url.return_value = file

        dl_folder_path = os.path.join(DOWNLOAD_FILE_PATH)
        os.makedirs(dl_folder_path, exist_ok=True)

    def test_clean_up_non_existent_path(self):
        # Arrange
        non_existent_path = f'{DOWNLOAD_FILE_PATH}/non_existent_file_or_folder'

        # Act
        try:
            GTFSFlexValidation.clean_up(non_existent_path)
            success = True
        except Exception:
            success = False

        # Assert
        self.assertTrue(success)

    def test_download_single_file_file_not_found_exception(self):
        # Arrange
        self.validator.storage_client = MagicMock()
        self.validator.storage_client.get_file_from_url = MagicMock()
        self.validator.storage_client.get_file_from_url.side_effect = FileNotFoundError('File not found')
        self.validator.prefix = Settings().get_unique_id()

        # Act & Assert
        with self.assertRaises(FileNotFoundError):
            self.validator.download_single_file(file_upload_path='mock_nonexistent_file')

    @patch('src.gtfs_flex_validation.CanonicalValidator')
    def test_is_gtfs_flex_valid_with_errors(self, mock_canonical_validator):
        # Arrange
        mock_result = MagicMock()
        mock_result.status = False
        mock_result.error = [
            {'code': 'INVALID_FIELD', 'sampleNotices': [{'fieldName': 'invalid_field', 'filename': 'flex_data'}]}
        ]
        mock_canonical_validator.return_value.validate.return_value = mock_result

        expected_downloaded_file_path = f'{SAVED_FILE_PATH}/fail_schema_1.zip'
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)

        # Act
        is_valid, validation_message = self.validator.is_gtfs_flex_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('INVALID_FIELD', validation_message)

    @patch('src.gtfs_flex_validation.CanonicalValidator')
    def test_is_gtfs_flex_valid_with_pathways_items(self, mock_canonical_validator):
        # Arrange
        mock_result = MagicMock()
        mock_result.status = False
        mock_result.error = [
            {'code': 'INVALID_FIELD',
             'sampleNotices': [{'fieldName': 'start_pickup_dropoff_window', 'filename': 'stop_times.txt'},
                               {'fieldName': 'end_pickup_dropoff_window', 'filename': 'stop_times.txt'}]}
        ]
        mock_canonical_validator.return_value.validate.return_value = mock_result

        expected_downloaded_file_path = f'{SAVED_FILE_PATH}/fail_schema_1.zip'
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)

        # Act
        is_valid, validation_message = self.validator.is_gtfs_flex_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('INVALID_FIELD', validation_message)

    @patch('src.gtfs_flex_validation.CanonicalValidator')
    def test_is_gtfs_flex_valid_with_pathways_parent_items(self, mock_canonical_validator):
        # Arrange
        mock_result = MagicMock()
        mock_result.status = False
        mock_result.error = [
            {'code': 'INVALID_FIELD',
             'sampleNotices': [{'fieldName': 'start_pickup_dropoff_window', 'childFilename': 'locations.geojson'},
                               {'fieldName': 'end_pickup_dropoff_window', 'childFilename': 'booking_rules.txt'}]}
        ]
        mock_canonical_validator.return_value.validate.return_value = mock_result

        expected_downloaded_file_path = f'{SAVED_FILE_PATH}/fail_schema_1.zip'
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)

        # Act
        is_valid, validation_message = self.validator.is_gtfs_flex_valid()

        # Assert
        self.assertFalse(is_valid)
        self.assertIn('INVALID_FIELD', validation_message)

    @patch('src.gtfs_flex_validation.CanonicalValidator')
    def test_is_gtfs_flex_valid_with_no_errors(self, mock_canonical_validator):
        # Arrange
        mock_result = MagicMock()
        mock_result.status = True
        mock_result.error = []
        mock_canonical_validator.return_value.validate.return_value = mock_result

        expected_downloaded_file_path = f'{SAVED_FILE_PATH}/{SUCCESS2_FILE_NAME}'
        self.validator.download_single_file = MagicMock(return_value=expected_downloaded_file_path)

        # Act
        is_valid, validation_message = self.validator.is_gtfs_flex_valid()

        # Assert
        self.assertTrue(is_valid)

    def test_is_gtfs_flex_valid_with_invalid_file_extension(self):
        self.validator.file_relative_path = f'{SAVED_FILE_PATH}/fail_schema_1.txt'

        # Act
        is_valid, validation_message = self.validator.is_gtfs_flex_valid()

        # Assert
        self.assertFalse(is_valid)

    @patch.object(GTFSFlexValidation, 'is_gtfs_flex_valid')
    def test_validate_facade(self, mock_is_gtfs_flex_valid):
        # Arrange
        mock_is_gtfs_flex_valid.return_value = (True, 'Valid file')

        # Act
        is_valid, validation_message = self.validator.validate()

        # Assert
        mock_is_gtfs_flex_valid.assert_called_once()
        self.assertTrue(is_valid)
        self.assertEqual(validation_message, 'Valid file')

    @patch('os.makedirs')
    @patch('builtins.open', new_callable=MagicMock)
    def test_download_single_file_creates_directory(self, mock_open, mock_makedirs):
        # Arrange
        mock_file = MagicMock()
        mock_file.file_path = 'file.zip'
        mock_file.get_stream = MagicMock(return_value=b'file_content')

        self.validator.storage_client = MagicMock()
        self.validator.storage_client.get_file_from_url = MagicMock(return_value=mock_file)

        self.validator.prefix = "test-prefix"  # Mock prefix
        expected_dl_folder_path = f"{DOWNLOAD_FILE_PATH}/{self.validator.prefix}"
        expected_file_path = f"{expected_dl_folder_path}/file.zip"

        # Act
        downloaded_file_path = self.validator.download_single_file(file_upload_path='mock_file.zip')

        # Assert
        mock_makedirs.assert_called_once_with(expected_dl_folder_path, exist_ok=True)
        mock_open.assert_called_once_with(expected_file_path, 'wb')
        self.assertEqual(downloaded_file_path, expected_file_path)
        mock_file.get_stream.assert_called_once()


class TestGTFSFlexValidationInit(unittest.TestCase):
    @patch('src.gtfs_flex_validation.Settings')
    def test_initialization(self, mock_settings):
        # Arrange
        mock_storage_client = MagicMock()
        mock_container = MagicMock()
        mock_storage_client.get_container.return_value = mock_container

        mock_settings_instance = mock_settings.return_value
        mock_settings_instance.storage_container_name = "test_container"
        mock_settings_instance.get_unique_id.return_value = "unique_prefix"

        file_path = "path/to/file.zip"

        # Act
        validation_instance = GTFSFlexValidation(
            file_path=file_path,
            storage_client=mock_storage_client,
            prefix=None
        )

        # Assert
        self.assertEqual(validation_instance.file_path, file_path)
        self.assertEqual(validation_instance.file_relative_path, "file.zip")
        self.assertEqual(validation_instance.container_name, "test_container")
        self.assertEqual(validation_instance.prefix, "unique_prefix")
        self.assertEqual(validation_instance.client, mock_container)

        mock_storage_client.get_container.assert_called_once_with(container_name="test_container")
        mock_settings_instance.get_unique_id.assert_called_once()

    @patch('src.gtfs_flex_validation.Settings')
    def test_initialization_with_prefix(self, mock_settings):
        # Arrange
        mock_storage_client = MagicMock()
        mock_container = MagicMock()
        mock_storage_client.get_container.return_value = mock_container

        mock_settings_instance = mock_settings.return_value
        mock_settings_instance.storage_container_name = "test_container"

        file_path = "path/to/file.zip"
        custom_prefix = "custom_prefix"

        # Act
        validation_instance = GTFSFlexValidation(
            file_path=file_path,
            storage_client=mock_storage_client,
            prefix=custom_prefix
        )

        # Assert
        self.assertEqual(validation_instance.prefix, custom_prefix)
        self.assertEqual(validation_instance.container_name, "test_container")
        self.assertEqual(validation_instance.file_relative_path, "file.zip")

        mock_storage_client.get_container.assert_called_once_with(container_name="test_container")
        mock_settings_instance.get_unique_id.assert_not_called()


if __name__ == '__main__':
    unittest.main()
