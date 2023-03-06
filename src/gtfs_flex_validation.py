import os
import shutil
from typing import Union, Any
from config import Settings

from python_ms_core import Core
from tdei_gtfs_csv_validator import gcv_test_release
from tdei_gtfs_csv_validator import exceptions as gcvex

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path used for download file generation.
DOWNLOAD_FILE_PATH = os.path.join(ROOT_DIR, 'downloads')

DATA_TYPE = 'gtfs_flex'
SCHEMA_VERSION = 'v2.0'


class GTFSFlexValidation:
    def __init__(self, file_path=None):
        core = Core()
        self.container_name = Settings.storage_container_name
        self.storage_client = core.get_storage_client()
        self.file_path = file_path
        self.file_relative_path = file_path.split('/')[-1]
        self.client = self.storage_client.get_container(container_name=self.container_name)

    # Facade function to validate the file
    # Focuses on the file name with file name validation
    # Use `is_gtfs_valid` to do more processing
    def validate(self) -> tuple[bool, str]:
        return self.is_gtfs_flex_valid()

    # use this method to do the actual validation
    # when ready to replace, replace the call in the 
    # above function.
    def is_gtfs_flex_valid(self) -> tuple[Union[bool, Any], Union[str, Any]]:
        dest = DOWNLOAD_FILE_PATH
        is_valid = False
        validation_message = ''
        if self.file_relative_path.endswith('.json') or self.file_relative_path.endswith('.zip'):
            downloaded_file_path = self.download_single_file(self.file_path)
            try:
                gcv_test_release.test_release(DATA_TYPE, SCHEMA_VERSION, downloaded_file_path)
                is_valid = True
            except Exception as err:
                validation_message = str(err)
            finally:
                # Removing the file
                os.remove(downloaded_file_path)
        else:
            source = '/'.join(self.file_path.split('/')[4:])
            blobs = self.ls_files(source, recursive=True)
            if blobs:
                if not source == '' and not source.endswith('/'):
                    source += '/'
                if not dest.endswith('/'):
                    dest += '/'
                dest += os.path.basename(os.path.normpath(source)) + '/'
                blobs = [source + blob for blob in blobs]
                for blob in blobs:
                    blob_dest = dest + os.path.relpath(blob, source)
                    self.download_file(blob, blob_dest)
            else:
                self.download_file(source, dest)
            try:
                gcv_test_release.test_release(DATA_TYPE, SCHEMA_VERSION, dest)
                is_valid = True
            except Exception as err:
                validation_message = str(err)
            finally:
                # Removing extract folder
                shutil.rmtree(os.path.join(DOWNLOAD_FILE_PATH, dest), ignore_errors=False)

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
    def download_single_file(self, file_upload_path=None) -> str:
        is_exists = os.path.exists(DOWNLOAD_FILE_PATH)
        if not is_exists:
            os.makedirs(DOWNLOAD_FILE_PATH)

        file = self.storage_client.get_file_from_url(self.container_name, file_upload_path)
        try:
            if file.file_path:
                file_path = file.file_path.split('/')[-1]
                with open(f'{DOWNLOAD_FILE_PATH}/{file_path}', 'wb') as blob:
                    blob.write(file.get_stream())
                print(f'File downloaded to location: {DOWNLOAD_FILE_PATH}/{file_path}')
                return f'{DOWNLOAD_FILE_PATH}/{file_path}'
            else:
                print('File not found!')
        except Exception as e:
            print(e)

    def download_file(self, source, dest):
        # dest is a directory if ending with '/' or '.', otherwise it's a file
        if dest.endswith('.'):
            dest += '/'
        blob_dest = dest + os.path.basename(source) if dest.endswith('/') else dest

        print(f'Downloading {source} to {blob_dest}')
        os.makedirs(os.path.dirname(blob_dest), exist_ok=True)
        bc = self.storage_client.get_file(container_name=self.container_name, file_name=source)

        with open(blob_dest, 'wb') as file:
            file.write(bc.get_stream())
        return blob_dest

    def ls_files(self, path, recursive=False):
        if not path == '' and not path.endswith('/'):
            path += '/'

        blob_iter = self.client.list_files(name_starts_with=path)
        files = []
        for blob in blob_iter:
            relative_path = os.path.relpath(blob.name, path)
            if recursive or not '/' in relative_path:
                files.append(relative_path)
        return files
