# SPDX-License-Identifier: MIT

from tqdm import tqdm
from tqdm.utils import CallbackIOWrapper

import os
import requests

FIRMWARE_FILE = 'firmware.bin'
TARGET = '192.168.64.100'
UPDATE_URL = f'http://{TARGET}/api/firmware'

file_path = os.path.abspath(FIRMWARE_FILE)
file_size = os.stat(file_path).st_size
with open(file_path, "rb") as f:
    with tqdm(total=file_size, unit="B", unit_scale=True, unit_divisor=1024) as t:
        wrapped_file = CallbackIOWrapper(t.update, f, "read")
        requests.post(UPDATE_URL, data=wrapped_file)