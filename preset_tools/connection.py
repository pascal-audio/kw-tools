# SPDX-License-Identifier: MIT

import asyncio
import re
import requests
import websockets
from jsonrpcclient import Ok, parse, request
from preset import *
from enum import Enum
import base64
from pathlib import Path


class ExportPresetParams(str, Enum):
    Equalizer = 'equalizer'
    Crossover = 'crossover'
    Delay = 'delay'
    Limiter = 'limiter'
    OutputMode = 'output_mode'
    Fir = 'fir'
    Polarity = 'polarity'

    def __str__(self):
        return self.value


class Response:
    def __init__(self) -> None:
        self.valid: bool = False
        self.register: str
        self.result_str: str
        self.updates: list = []
        self.unexpected: None


class Connection:
    def __init__(self) -> None:
        self._host = None
        self._websocket = None
        self._response = None

    async def async_connect(self, host: str):
        self._host = host
        if not self._websocket:
            self._websocket = await websockets.connect(f'ws://{host}/ws')

    async def async_disconnect(self):
        if self._websocket:
            await self._websocket.close()
            self._websocket = None

    async def async_read_response(self):
        while 1:
            response = await self._websocket.recv()

            for line in response.splitlines():
                if line.startswith(('#', '*')):
                    self._response.result_str = line
                    return line
                elif line.startswith(('+')):
                    m = re.match(r'[+]([^ ]+) (.+)', line)
                    if not m:
                        raise Exception(f'Invalid Response')
                    reg = m[1]
                    val = m[2]

                    self._response.updates.append((reg, val))
                else:
                    self._response.unexpected = line
                    raise Exception()

    async def async_execute_command_internal(self, cmd, timeout=2.0):
        try:
            await self._websocket.send(cmd + '\n')

            line = await asyncio.wait_for(self.async_read_response(), timeout)
            cmd = cmd.strip("\r\n\t ")
            if line == f'*{cmd}':
                return
            else:
                raise Exception(line)

        except asyncio.exceptions.CancelledError:
            raise TimeoutError()

    async def async_execute_command(self, cmd, timeout=2.0):
        self._response = Response()
        await self.async_execute_command_internal(cmd, timeout)

    async def async_get_reg(self, reg: str, responseCount=1, timeout: float = 2.0):
        self._response = Response()
        self._response.register = reg

        cmd = f'GET {reg}'
        await self.async_execute_command_internal(cmd)

        count = len(self._response.updates)
        if responseCount > 0 and count != responseCount:
            raise Exception(f'Invalid number of updates: {count}')

        if responseCount == 1:
            update = self._response.updates[0]

            if update[0] != reg:
                raise Exception(f'Invalid Register')

            return update[1]
        return None

    async def async_set_reg(self, reg: str, value, timeout=2.0):
        self._response = Response()
        self._response.register = reg

        cmd = f'SET {reg} {value}'
        await self.async_execute_command_internal(cmd)

    async def unchecked_get_reg(self, reg: str, timeout: float = 2.0):
        try:
            await self.async_get_reg(reg, timeout)
        except:
            pass

        return self._response.result_str

    async def unchecked_set_reg(self, reg: str, value, timeout=2.0):
        try:
            await self.async_set_reg(reg, value, timeout)
        except:
            pass

        return self._response.result_str

    def call_jrpc(self, name, args):
        response = requests.post(f"http://{self._host}/jrpc", json=request(name, args))

        parsed = parse(response.json())
        if isinstance(parsed, Ok):
            return(parsed.result)
        else:
            raise Exception(parsed.message)

    async def set_value(self, name: str, value):
        value = await self.async_set_reg(name, value)

    async def set_str(self, name: str, value: str):
        await self.set_value(name, f'"{value}"')

    async def set_int(self, name: str, value: int):
        await self.set_value(name, f'{value}')

    async def set_bool(self, name: str, value: bool):
        await self.set_value(name, f'{1 if value else 0}')

    async def set_float(self, name: str, value: float):
        await self.set_value(name, f'{value}')

    async def set_speaker_equalizer(self, ch: int, index: int, eq: Equalizer):
        base = f'OUT-{ch}.SPEAKER_EQ-{index}'

        await self.set_bool(f'{base}.BYPASS', eq.bypass)
        await self.set_str(f'{base}.TYPE', str(eq.type))
        await self.set_float(f'{base}.GAIN', eq.gain)
        await self.set_float(f'{base}.FREQ', eq.freq)
        await self.set_float(f'{base}.Q', eq.q)

    async def set_crossover(self, ch: int, xr: Crossover):
        base = f'OUT-{ch}.XR'

        await self.set_bool(f'{base}.BYPASS', xr.bypass)
        await self.set_float(f'{base}.GAIN', xr.gain)
        await self.set_str(f'{base}.LOWPASS_TYPE', str(xr.lowpass_type))
        await self.set_float(f'{base}.LOWPASS_FREQUENCY', xr.lowpass_freq)
        await self.set_str(f'{base}.HIGHPASS_TYPE', str(xr.highpass_type))
        await self.set_float(f'{base}.HIGHPASS_FREQUENCY', xr.highpass_freq)

    async def set_speaker_delay(self, ch: int, delay: Delay):
        base = f'OUT-{ch}.SPEAKER_DELAY'

        await self.set_bool(f'{base}.BYPASS', delay.bypass)
        await self.set_float(f'{base}.TIME', delay.time / 48000)

    async def set_clip_limiter(self, ch: int, lim: ClipLimiter):
        base = f'OUT-{ch}.CLIP_LIMITER'

        await self.set_bool(f'{base}.BYPASS', lim.bypass)
        await self.set_str(f'{base}.MODE', str(lim.mode))

    async def set_peak_limiter(self, ch: int, lim: PeakLimiter):
        base = f'OUT-{ch}.PEAK_LIMITER'

        assert(lim.release >= lim.attack)

        await self.set_bool(f'{base}.BYPASS', lim.bypass)
        await self.set_bool(f'{base}.AUTO', lim.auto)
        await self.set_float(f'{base}.THRESHOLD', lim.threshold)
        await self.set_float(f'{base}.ATTACK', 0)
        await self.set_float(f'{base}.RELEASE', lim.release)
        await self.set_float(f'{base}.ATTACK', lim.attack)
        await self.set_float(f'{base}.HOLD', lim.hold)
        await self.set_float(f'{base}.KNEE', lim.knee)

    async def set_rms_limiter(self, ch: int, lim: RmsLimiter):
        base = f'OUT-{ch}.RMS_LIMITER'

        assert(lim.release >= lim.attack)

        await self.set_bool(f'{base}.BYPASS', lim.bypass)
        await self.set_float(f'{base}.THRESHOLD', lim.threshold)
        await self.set_float(f'{base}.ATTACK', 0)
        await self.set_float(f'{base}.RELEASE', lim.release)
        await self.set_float(f'{base}.ATTACK', lim.attack)
        await self.set_float(f'{base}.HOLD', lim.hold)
        await self.set_float(f'{base}.KNEE', lim.knee)

    async def set_output_mode(self, ch: int, mode: OutputMode):
        assert(mode in OutputMode)
        await self.set_str(f'OUT-{ch}.OUTPUT_MODE', str(mode))

    async def set_output_highpass(self, ch: int, freq: Optional[float]):
        await self.set_float(f'OUT-{ch}.OUTPUT_HIGHPASS', 0 if not freq else freq)

    async def set_output_polarity(self, ch: int, polarity: int):
        assert(polarity in [-1, 1])
        await self.set_int(f'OUT-{ch}.POLARITY', polarity)

    async def set_fir(self, ch: int, fir: Fir):
        await self.set_bool(f'OUT-{ch}.FIR.BYPASS', fir.bypass or len(fir.taps) == 0)
        if len(fir.taps) > 0:
            args = {
                'channel': ch,
                'taps': fir.taps
            }

            self.call_jrpc('apply_fir', args)
        else:
            args = {
                'channel': ch
            }

            self.call_jrpc('clear_fir', args)

    async def clear_preset(self, channel: int):
        args = { 
            "channel": channel,
        }

        return self.call_jrpc('clear_preset', args)

    async def decode_preset(self, infile: str):
        with open(infile, 'rb') as f:
            preset = f.read()

        args = {
            'preset': base64.b64encode(preset).decode('ascii')
        }
        
        return self.call_jrpc('decode_preset', args)

    async def set_preset(self, ch: int, sp: SpeakerPreset):
        await self.clear_preset(ch)

        await self.set_output_mode(ch, sp.output_mode)
        await self.set_output_highpass(ch, sp.output_highpass)
        await self.set_output_polarity(ch, sp.polarity)
        for idx, eq in enumerate(sp.equalizer):
            await self.set_speaker_equalizer(ch, idx + 1, eq)
        await self.set_crossover(ch, sp.crossover)
        await self.set_clip_limiter(ch, sp.clip_limiter)
        await self.set_peak_limiter(ch, sp.peak_limiter)
        await self.set_rms_limiter(ch, sp.rms_limiter)
        await self.set_fir(ch, sp.fir)

    async def protect_preset(self, ch: int, infile: str, outfile: str, store_flags=[ExportPresetParams], protect_flags=[ExportPresetParams]):
        with open(infile, 'rb') as f:
            preset = f.read()

        args = {
            "channel": 1,
            'preset': base64.b64encode(preset).decode('ascii')
        }

        self.call_jrpc('apply_preset', args)

        name = Path(infile).stem

        args = {
            'channel': ch,
            'name': name,
            'vendor_lock': True,
            'store': store_flags,
            'protect': protect_flags
        }

        j = self.call_jrpc('create_preset', args)

        filename = j.get('filename')
        data = base64.b64decode(j.get('data'))

        with open(outfile, 'wb') as f:
            f.write(data)


    async def create_preset(self, ch: int, name: str, vendor_lock: bool, store_flags=[ExportPresetParams], protect_flags=[ExportPresetParams]):
        args = {
            'channel': ch,
            'name': name,
            'vendor_lock': vendor_lock,
            'store': store_flags,
            'protect': protect_flags
        }

        j = self.call_jrpc('create_preset', args)

        filename = j.get('filename')
        data = base64.b64decode(j.get('data'))

        return (filename, data)
