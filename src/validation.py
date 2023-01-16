import urllib.parse


class Validation:
    def __init__(self, file_name=None):
        self.is_valid, self.validation_message = self.is_file_validate(file_full_name=file_name)

    @classmethod
    def is_file_validate(cls, file_full_name=None):
        file_path_clean = urllib.parse.unquote(file_full_name)
        file_name = file_path_clean.split('/')[-1]

        if file_name.find('invalid') != -1:
            print('Invalid file')
            return False, 'Invalid file'
        elif file_name.find('valid') != -1:
            print('Valid file')
            return True, 'Valid file'
        else:
            print('Invalid file.. No regex found')
            return False, f'No regex found in file {file_name}'
