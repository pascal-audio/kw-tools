# SPDX-License-Identifier: MIT

from connection import Connection, ExportPresetParams
from preset import *
import asyncio
import random

TARGET = '192.168.64.100'


async def async_main():
    print('Creating Speaker Preset')
    sp = SpeakerPreset()
    sp.output_mode = OutputMode.OUTPUT_MODE_8R
    sp.polarity = 1
    sp.output_highpass = None  # None or [20 - 20000]

    sp.crossover.bypass = False
    sp.crossover.gain = 12
    sp.crossover.lowpass_type = CrossoverType.BES48
    sp.crossover.lowpass_freq = 1200
    sp.crossover.highpass_type = CrossoverType.BES12
    sp.crossover.highpass_freq = 80

    for i in range(15):
        sp.equalizer[i].bypass = False
        sp.equalizer[i].type = EqualizerType.BANDPASS
        sp.equalizer[i].gain = i
        sp.equalizer[i].freq = 1000 + 100 * i
        sp.equalizer[i].q = 1 + 0.1 * i

    sp.clip_limiter.bypass = False
    sp.clip_limiter.mode = ClipLimiterMode.FAST

    sp.peak_limiter.bypass = False
    sp.peak_limiter.auto = False
    sp.peak_limiter.threshold = 17
    sp.peak_limiter.attack = 0.05
    sp.peak_limiter.release = 0.1
    sp.peak_limiter.hold = 0.1
    sp.peak_limiter.knee = 6

    sp.rms_limiter.bypass = False
    sp.rms_limiter.threshold = 17
    sp.rms_limiter.attack = 0.05
    sp.rms_limiter.release = 0.1
    sp.rms_limiter.hold = 0.1
    sp.rms_limiter.knee = 6

    sp.fir.bypass = False
    sp.fir.taps = [random.random() for i in range(512)]

    print('Connecting to Amp...')
    c = Connection()
    await c.async_connect(TARGET)

    print('Setting Preset...')
    await c.set_preset(1, sp)

    print('Generating Speaker Preset...')

    channel = 1
    preset_name = 'preset20'
    vendor_lock = False
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
        # ExportPresetParams.Equalizer,
        # ExportPresetParams.Crossover,
        # ExportPresetParams.Delay,
        # ExportPresetParams.Limiter,
        # ExportPresetParams.OutputMode,
        # ExportPresetParams.Fir,
        # ExportPresetParams.Polarity
    ]
    (filename, data) = await c.create_preset(channel, preset_name, vendor_lock, store_flags, protect_flags)

    with open(filename, 'wb') as f:
        f.write(data)

    print(f'Preset written to "{filename}"')
    await c.async_disconnect()
    print(f'SUCCESS!\n')


asyncio.run(async_main())
