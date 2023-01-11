import json
import datetime
import decimal


class Jsonable(object):
    def __iter__(self):
        for attr, value in self.__dict__.iteritems():
            if isinstance(value, datetime.datetime):
                iso = value.isoformat()
                yield attr, iso
            elif isinstance(value, decimal.Decimal):
                yield attr, str(value)
            elif hasattr(value, '__iter__'):
                if hasattr(value, 'pop'):
                    a = []
                    for subval in value:
                        if hasattr(subval, '__iter__'):
                            a.append(dict(subval))
                        else:
                            a.append(subval)
                    yield attr, a
                else:
                    yield attr, dict(value)
            else:
                yield attr, value


class GTFSFlexUpload(Jsonable):

    def __init__(self, data: dict):
        upload_data = data.get('data', None)
        self.message = data.get('message', None)
        self.messageType = data.get('messageType', None)
        self.messageId = data.get('messageId', '')
        self.publishedDate = data.get('publishedDate', None)
        self.data = GTFSFlexUploadData(data=upload_data) if upload_data else {}

    def data_from(self):
        data = self
        if isinstance(data, str):
            data = json.loads(self)
        if data:
            try:
                return GTFSFlexUpload(data=data.to_dict())
            except Exception as e:
                error = str(e).replace('GTFSFlexUpload', 'Invalid parameter,')
                raise TypeError(error)


class GTFSFlexUploadData(Jsonable):
    def __init__(self, data: dict):
        polygon = data.get('polygon', None)
        self.tdei_org_id = data.get('tdei_org_id', '')
        self.tdei_record_id = data.get('tdei_record_id', '')
        self.tdei_service_id = data.get('tdei_service_id', '')
        self.collected_by = data.get('collected_by', '')
        self.collection_method = data.get('collection_method', '')
        self.file_upload_path = data.get('file_upload_path', '')
        self.user_id = data.get('user_id', '')
        self.collection_date = data.get('collection_date', '')
        self.valid_from = data.get('valid_from', '')
        self.valid_to = data.get('valid_to', '')
        self.flex_schema_version = data.get('flex_schema_version', '')
        self.data_source = data.get('data_source', '')
        self.polygon = Polygon(data=polygon) if polygon else {}
        self.is_valid = False
        self.validation_message = ''
        self.validation_time = 90


class Polygon(Jsonable):
    def __init__(self, data: dict):
        features = data.get('features', None)
        self.type = data.get('type', '')
        self.features = list(Feature(data=features)) if features > 0 else []


class Feature(Jsonable):
    def __init__(self, data: dict):
        geometry = data.get('geometry', None)
        self.type = data.get('type', '')
        self.properties = data.get('properties', {})
        self.geometry = Geometry(data=geometry) if geometry else {}


class Geometry(Jsonable):
    def __init__(self, data: dict):
        self.type = data.get('type', '')
        self.coordinates = data.get('coordinates', [])
