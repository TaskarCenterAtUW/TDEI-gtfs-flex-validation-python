class Validation:
    def __init__(self, file_path=None):
        self.file_relative_path = file_path.split('/')[-1]
        self.is_valid, self.validation_message = self.is_file_validate(file_full_name=self.file_relative_path)

    @classmethod
    def is_file_validate(cls, file_full_name=None):
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
