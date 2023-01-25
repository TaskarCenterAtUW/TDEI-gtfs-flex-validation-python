from python_ms_core import Core
import os

ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
# Path used for asset file generation.
ASSETS_FILE_PATH = os.path.join(ROOT_DIR, 'assets')


class GTFSFlexValidation:
    def __init__(self, file_path=None):
        self.file_path = file_path
        self.file_relative_path = file_path.split('/')[-1]

    # Facade function to validate the file
    # Focuses on the file name with file name validation
    # Use `is_gtfs_valid` to do more processing
    def validate(self) -> tuple[bool, str]:
        dummy_validation = self.is_file_name_valid(self.file_relative_path)
        return dummy_validation

    # use this method to do the actual validation
    # when ready to replace, replace the call in the 
    # above function.
    def is_gtfs_flex_valid(self) -> None:
        file_download_path = self.download_file(self.file_path)
        # file is downloaded to above path
        # use the remaining logic to validate 
        # and create other test cases.
        # TODO:
        #   download the file to a local directory (downloads)
        #   file_details = json.load(file..)
        #   ret_values = validate(downloaded_file)
        #   delete the local file in downloads folder
        # return file_details['valid'], file_details['valid_message]
        # return ret_values

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
        storage_client = Core.get_storage_client()
        file = storage_client.get_file_from_url('gtfsflex', file_upload_path)
        file_path = '{ASSETS_FILE_PATH}/{file_name}'
        try:
            if file.file_path:
                file_name = file.file_path.split('/')[-1]
                with open(f'{ASSETS_FILE_PATH}/{file_name}', 'wb') as blob:
                    blob.write(file.get_stream())
                print(f'File download to location: {ASSETS_FILE_PATH}/{file_name}')
                return file_path
            else:
                print('File not found!')
        except Exception as e:
            print(e)
