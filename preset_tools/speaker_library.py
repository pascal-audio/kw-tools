import json
import gzip
import base64
from uuid import uuid1 as uid

from connection import Connection

class SpeakerLibrary:
    def __init__(self, c: Connection, name: str, version: str, vendor_id: int = 0):
        self._c = c
        
        self._d = {}
        
        self._d['name'] = name
        self._d['id'] = str(uid())
        self._d['version'] = version
        self._d['vendorId'] = vendor_id
        self._d['children'] = []

    def _get_preset_folder(self, name: str) -> list:
        folder = next((x for x in self._d['children'] if x['name'] == name), None)

        if not folder:
            d = {}
            d['name'] = name
            d['id'] = str(uid())
            d['children'] = []
            #d['parent_id'] = None

            self._d['children'].append(d)

            folder = d

        return folder

    async def add_preset(self, folder: str, name: str, path: str):
        d = {}

        with open(path, 'rb') as f:
            buf = f.read()

        preset_data = await self._c.decode_preset(path)

        d['id'] = str(uid())
        d['name'] = preset_data['name']
        d['presetId'] = preset_data['id']
        d['vendorId'] = preset_data['vendorId']
        d['preset'] = base64.b64encode(buf).decode('ascii')

        vendor_id = preset_data['vendorId']

        if vendor_id != 0:
            if self._d['vendorId'] != 0 and vendor_id != self._d['vendorId']:
                raise 'Invalid Vendor ID'
            else:
                self._d['vendorId'] = vendor_id

        preset_dict = self._get_preset_folder(folder)
        preset_dict['children'].append(d)

    def to_json(self):
        return json.dumps(self._d)

    def to_preset_file(self):
        j = self.to_json().encode('utf8')

        return gzip.compress(j)
