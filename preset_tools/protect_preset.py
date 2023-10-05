# SPDX-License-Identifier: MIT

from connection import Connection, ExportPresetParams
from preset import *
import asyncio

TARGET = '192.168.64.100'
INFILE = 'in/preset.zcp'
OUTFILE = 'out/preset.zcp'


async def async_main():
    print('Connecting to Amp...')
    c = Connection()
    await c.async_connect(TARGET)

    channel = 1

    print('Clearing Existing Preset')
    await c.clear_preset(channel)
    
    print('Generating Protected Speaker Preset...')

    store_flags = [
        ExportPresetParams.Equalizer,
        ExportPresetParams.Crossover,
        ExportPresetParams.Delay,
        ExportPresetParams.Limiter,
        ExportPresetParams.OutputMode,
        ExportPresetParams.Fir,
        ExportPresetParams.Polarity
    ]
    protect_flags = [
        ExportPresetParams.Equalizer,
        ExportPresetParams.Crossover,
        ExportPresetParams.Delay,
        ExportPresetParams.Limiter,
        ExportPresetParams.OutputMode,
        ExportPresetParams.Fir,
        ExportPresetParams.Polarity
    ]
    
    await c.protect_preset(channel, INFILE, OUTFILE, store_flags, protect_flags)

    await c.async_disconnect()
    print(f'SUCCESS!\n')


asyncio.run(async_main())
