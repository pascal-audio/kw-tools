# SPDX-License-Identifier: MIT

from connection import Connection, ExportPresetParams
from speaker_library import SpeakerLibrary
from preset import *
import asyncio
import os
import glob
from natsort import natsorted

TARGET = '192.168.64.100'

async def async_main():
    print('Connecting to Amp...')
    c = Connection()
    await c.async_connect(TARGET)

    name = 'Pascal Library'
    version = '1'
    outfile = f'out/speaker_lib_R{version}.zcl'
    outfile = os.path.abspath(outfile)

    os.chdir('./lib')

    files = glob.glob('**/*.zcp', recursive=True)
    files = natsorted(files)

    print('Create Speaker Library...')
    spl = SpeakerLibrary(c, name, version)

    for file in files:
        print(f'Adding file {file}')
        (dir, name) = os.path.split(file)
        name = os.path.basename(name)

        await spl.add_preset(dir, name, file)

    print('Write Library...')
    with open(outfile, 'wb') as f:
        f.write(spl.to_preset_file())

    await c.async_disconnect()


asyncio.run(async_main())
