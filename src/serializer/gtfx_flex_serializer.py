import json


class GTFSFlexUpload:

    def __init__(self, data: dict):
        upload_data = data.get('data', None)
        self._message = data.get('message', None)
        self._message_type = data.get('messageType', None)
        self._message_id = data.get('messageId', '')
        self._published_date = data.get('publishedDate', None)
        self.data = GTFSFlexUploadData(data=upload_data) if upload_data else {}

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, value):
        self._message = value

    @property
    def message_type(self):
        return self._message_type

    @message_type.setter
    def message_type(self, value):
        self._message_type = value

    @property
    def message_id(self):
        return self._message_id

    @message_id.setter
    def message_id(self, value):
        self._message_id = value

    @property
    def published_date(self):
        return self._published_date

    @published_date.setter
    def published_date(self, value):
        self._published_date = value

    def to_json(self):
        self.data = self.data.to_json()
        return to_json(self.__dict__)

    def data_from(self):
        message = self
        if isinstance(message, str):
            message = json.loads(self)
        if message:
            try:
                return GTFSFlexUpload(data=message)
            except Exception as e:
                error = str(e).replace('GTFSFlexUpload', 'Invalid parameter,')
                raise TypeError(error)


class GTFSFlexUploadData:
    def __init__(self, data: dict):
        polygon = data.get('polygon', None)
        request = data.get('request', None)
        meta = data.get('meta', None)

        response = data.get('response', None)
        self._stage = data.get('stage', '')
        self.request = Request(data=request) if request else {}
        self.meta = Meta(data=meta) if meta else {}
        self.response = Response(data=response) if response else {}
        self._tdei_org_id = data.get('tdei_org_id', '')
        self._tdei_record_id = data.get('tdei_record_id', '')
        self._tdei_service_id = data.get('tdei_service_id', '')
        self._collected_by = data.get('collected_by', '')
        self._file_upload_path = data.get('file_upload_path', '')
        self._user_id = data.get('user_id', '')
        self._collection_date = data.get('collection_date', '')
        self._valid_from = data.get('valid_from', '')
        self._valid_to = data.get('valid_to', '')
        self._flex_schema_version = data.get('flex_schema_version', '')
        self._data_source = data.get('data_source', '')
        self.polygon = Polygon(data=polygon).__dict__ if polygon else {}
        self._is_valid = False
        self._validation_message = ''
        self._validation_time = 90

    @property
    def stage(self): return self._stage

    @stage.setter
    def stage(self, value): self._stage = value

    @property
    def tdei_org_id(self): return self._tdei_org_id

    @tdei_org_id.setter
    def tdei_org_id(self, value): self._tdei_org_id = value

    @property
    def tdei_record_id(self): return self._tdei_record_id

    @tdei_record_id.setter
    def tdei_record_id(self, value): self._tdei_record_id = value

    @property
    def tdei_service_id(self): return self._tdei_service_id

    @tdei_service_id.setter
    def tdei_service_id(self, value): self._tdei_service_id = value

    @property
    def collected_by(self): return self._collected_by

    @collected_by.setter
    def collected_by(self, value): self._collected_by = value

    @property
    def file_upload_path(self): return self._file_upload_path

    @file_upload_path.setter
    def file_upload_path(self, value): self._file_upload_path = value

    @property
    def user_id(self): return self._user_id

    @user_id.setter
    def user_id(self, value): self._user_id = value

    @property
    def collection_date(self): return self._collection_date

    @collection_date.setter
    def collection_date(self, value): self._collection_date = value

    @property
    def valid_from(self): return self._valid_from

    @valid_from.setter
    def valid_from(self, value): self._valid_from = value

    @property
    def valid_to(self): return self._valid_to

    @valid_to.setter
    def valid_to(self, value): self._valid_to = value

    @property
    def flex_schema_version(self): return self._flex_schema_version

    @flex_schema_version.setter
    def flex_schema_version(self, value): self._flex_schema_version = value

    @property
    def data_source(self): return self._data_source

    @data_source.setter
    def data_source(self, value): self._data_source = value

    @property
    def is_valid(self): return self._is_valid

    @is_valid.setter
    def is_valid(self, value): self._is_valid = value

    @property
    def validation_message(self): return self._validation_message

    @validation_message.setter
    def validation_message(self, value): self._validation_message = value

    @property
    def validation_time(self): return self._validation_time

    @validation_time.setter
    def validation_time(self, value): self._validation_time = value

    def to_json(self):
        self.request = self.request.__dict__
        self.meta = self.meta.__dict__
        self.response = self.response.__dict__
        return to_json(self.__dict__)


class Request:
    def __init__(self, data: dict):
        self._tdei_org_id = data.get('tdei_org_id', '')
        self._tdei_service_id = data.get('tdei_service_id', '')
        self._collected_by = data.get('collected_by', '')
        self._collection_date = data.get('collection_date', '')
        self._collection_method = data.get('collection_method', '')
        self._valid_from = data.get('valid_from', '')
        self._valid_to = data.get('valid_to', '')
        self._data_source = data.get('data_source', '')
        self._polygon = data.get('polygon', {})
        self._flex_schema_version = data.get('flex_schema_version', '')

    @property
    def tdei_org_id(self): return self._tdei_org_id

    @tdei_org_id.setter
    def tdei_org_id(self, value): self._tdei_org_id = value

    @property
    def tdei_service_id(self): return self._tdei_service_id

    @tdei_service_id.setter
    def tdei_service_id(self, value): self._tdei_service_id = value

    @property
    def collected_by(self): return self._collected_by

    @collected_by.setter
    def collected_by(self, value): self._collected_by = value

    @property
    def collection_date(self): return self._collection_date

    @collection_date.setter
    def collection_date(self, value): self._collection_date = value

    @property
    def collection_method(self): return self._collection_method

    @collection_method.setter
    def collection_method(self, value): self._collection_method = value

    @property
    def valid_from(self): return self._valid_from

    @valid_from.setter
    def valid_from(self, value): self._valid_from = value

    @property
    def valid_to(self): return self._valid_to

    @valid_to.setter
    def valid_to(self, value): self._valid_to = value

    @property
    def flex_schema_version(self): return self._flex_schema_version

    @valid_to.setter
    def flex_schema_version(self, value): self._flex_schema_version = value


class Meta:
    def __init__(self, data: dict):
        self._file_upload_path = data.get('file_upload_path', '')
        self._isValid = False

    @property
    def file_upload_path(self): return self._file_upload_path

    @file_upload_path.setter
    def file_upload_path(self, value): self._file_upload_path = value

    @property
    def isValid(self): return self._isValid

    @isValid.setter
    def _isValid(self, value): self._isValid = value


class Response:

    def __init__(self, data: dict):
        self._success = data.get('success', False)
        self._message = data.get('message', '')

    @property
    def success(self): return self._success

    @success.setter
    def success(self, value): self._success = value

    @property
    def message(self): return self._message

    @message.setter
    def message(self, value): self._message = value


class Polygon:
    def __init__(self, data: dict):
        features = data.get('features', None)
        self.type = data.get('type', '')
        self.features = list(Feature(data=features).__dict__) if features else []


class Feature:
    def __init__(self, data: dict):
        geometry = data.get('geometry', None)
        self.type = data.get('type', '')
        self.properties = data.get('properties', {})
        self.geometry = Geometry(data=geometry).__dict__ if geometry else {}


class Geometry:
    def __init__(self, data: dict):
        self.type = data.get('type', '')
        self.coordinates = data.get('coordinates', [])


def remove_underscore(string: str):
    return string if not string.startswith('_') else string[1:]


def to_json(data: object):
    result = {}
    for key in data:
        value = data[key]
        key = remove_underscore(key)
        result[key] = value

    return result
