import os
import shutil
import json
import zipfile
from typing import Tuple, Union, Any

from python_ms_core import Core

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path used for download file generation.
DOWNLOAD_FILE_PATH = os.path.join(ROOT_DIR, 'downloads')


class GTFSFlexValidation:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_relative_path = file_path.split('/')[-1]

    # Facade function to validate the file
    # Focuses on the file name with file name validation
    # Use `is_gtfs_valid` to do more processing
    def validate(self) -> tuple[bool, str]:
        return self.is_gtfs_flex_valid()
        # dummy_validation = self.is_file_name_valid(self.file_relative_path)
        # return dummy_validation

    # use this method to do the actual validation
    # when ready to replace, replace the call in the 
    # above function.
    def is_gtfs_flex_valid(self) -> tuple[Union[bool, Any], Union[str, Any]]:
        file_download_path = self.download_file(self.file_path)
        # file is downloaded to above path
        # use the remaining logic to validate 
        # and create other test cases.

        is_valid = False
        validation_message = ''
        # Check the file extension
        downloaded_file_path = os.path.join(DOWNLOAD_FILE_PATH, self.file_relative_path)

        if file_download_path.endswith('.json'):
            with open(downloaded_file_path, 'rb') as msg_file:
                msg_data = json.load(msg_file)
                is_valid = msg_data['is_valid']
                validation_message = msg_data['valid_message']
        elif file_download_path.endswith('.zip'):
            zip_extraction_folder = downloaded_file_path.replace('.zip', '')
            with zipfile.ZipFile(downloaded_file_path, 'r') as zip:
                zip.extractall(os.path.join(DOWNLOAD_FILE_PATH, zip_extraction_folder))
                # TODO: Do something with the zip file to validate it
            # Removing extract folder
            shutil.rmtree(os.path.join(DOWNLOAD_FILE_PATH, zip_extraction_folder), ignore_errors=False)

        # Removing the file
        os.remove(downloaded_file_path)
        return is_valid, validation_message

    # dummy validation code with just file name.
    def is_file_name_valid(self, file_full_name=None) -> tuple[bool, str]:
        file_name = file_full_name.split('/')[-1]
        if file_name.find('invalid') != -1:
            print('Invalid file')
            return False, 'Invalid file'
        elif file_name.find('valid') != -1:
            print('Valid file')
            return True, 'Valid file'
        else:
            print(f'No regex found in file {file_name}')
            return False, f'No regex found in file {file_name}'

    # Downloads the file to local folder of the server
    # file_upload_path is the fullUrl of where the 
    # file is uploaded.
    def download_file(self, file_upload_path=None) -> str:
        is_exists = os.path.exists(DOWNLOAD_FILE_PATH)
        if not is_exists:
            os.makedirs(DOWNLOAD_FILE_PATH)

        storage_client = Core.get_storage_client()
        file = storage_client.get_file_from_url('gtfsflex', file_upload_path)
        file_path = f'{DOWNLOAD_FILE_PATH}/{self.file_relative_path}'
        try:
            if file.file_path:
                file_path = file.file_path.split('/')[-1]
                with open(f'{DOWNLOAD_FILE_PATH}/{file_path}', 'wb') as blob:
                    blob.write(file.get_stream())
                print(f'File downloaded to location: {DOWNLOAD_FILE_PATH}/{file_path}')
                return file_path
            else:
                print('File not found!')
        except Exception as e:
            print(e)
