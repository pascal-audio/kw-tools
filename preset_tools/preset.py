# SPDX-License-Identifier: MIT

from enum import Enum, auto
from typing import List, Optional


class EqualizerType(Enum):
    PARAMETRIC = auto()
    LOW_PASS_12 = auto()
    HIGH_PASS_12 = auto()
    LOW_SHELF_Q = auto()
    HIGH_SHELF_Q = auto()
    BANDPASS = auto()
    NOTCH = auto()
    ALLPASS_2 = auto()
    LOW_SHELF = auto()
    LOW_SHELF_6 = auto()
    LOW_SHELF_12 = auto()
    HIGH_SHELF = auto()
    HIGH_SHELF_6 = auto()
    HIGH_SHELF_12 = auto()
    ALLPASS_1 = auto()
    LOW_PASS_6 = auto()
    HIGH_PASS_6 = auto()

    def __str__(self):
        return self.name


class CrossoverType(Enum):
    OFF = auto()
    BUT6 = auto()
    BUT12 = auto()
    BUT24 = auto()
    BUT48 = auto()
    BES12 = auto()
    BES24 = auto()
    BES48 = auto()
    LR12 = auto()
    LR24 = auto()
    LR36 = auto()
    LR48 = auto()
    BUT18 = auto()
    BUT36 = auto()

    def __str__(self):
        return self.name


class ClipLimiterMode(Enum):
    NORMAL = auto()
    FAST = auto()

    def __str__(self):
        return self.name


class OutputMode(str, Enum):
    OUTPUT_MODE_OFF = 'OFF'
    OUTPUT_MODE_8R = '8R'
    OUTPUT_MODE_70V = '70V'
    OUTPUT_MODE_100V = '100V'
    OUTPUT_MODE_BRIDGED = 'BRIDGED'

    def __str__(self):
        return self.value


class Equalizer:
    def __init__(self) -> None:
        self._bypass = False
        self._type = EqualizerType.PARAMETRIC
        self._gain = 0
        self._freq = 100
        self._q = 0.7

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def type(self) -> EqualizerType:
        return self._type

    @type.setter
    def type(self, value: EqualizerType):
        assert(value in EqualizerType)
        self._type = value

    @property
    def gain(self) -> float:
        return self._gain

    @gain.setter
    def gain(self, value: float):
        assert(-15 < value < 15)
        self._gain = value

    @property
    def freq(self) -> float:
        return self._freq

    @freq.setter
    def freq(self, value: float):
        assert(20 < value < 20000)
        self._freq = value

    @property
    def q(self) -> float:
        return self._q

    @q.setter
    def q(self, value: float):
        assert(0.4 < value < 30)
        self._q = value


class Crossover:
    def __init__(self) -> None:
        self._bypass = True
        self._gain = 0
        self._lowpass_type = CrossoverType.OFF
        self._lowpass_freq = 19000
        self._highpass_type = CrossoverType.OFF
        self._highpass_freq = 20

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def gain(self) -> float:
        return self._gain

    @gain.setter
    def gain(self, value: float):
        assert(-15 < value < 15)
        self._gain = value

    @property
    def lowpass_type(self) -> CrossoverType:
        return self._lowpass_type

    @lowpass_type.setter
    def lowpass_type(self, value: CrossoverType):
        assert(value in CrossoverType)
        self._lowpass_type = value

    @property
    def lowpass_freq(self) -> float:
        return self._lowpass_freq

    @lowpass_freq.setter
    def lowpass_freq(self, value: float):
        assert(20 < value < 20000)
        self._lowpass_freq = value

    @property
    def highpass_type(self) -> CrossoverType:
        return self._highpass_type

    @highpass_type.setter
    def highpass_type(self, value: CrossoverType):
        assert(value in CrossoverType)
        self._highpass_type = value

    @property
    def highpass_freq(self) -> float:
        return self._highpass_freq

    @highpass_freq.setter
    def highpass_freq(self, value: float):
        assert(20 < value < 20000)
        self._highpass_freq = value


class Delay:
    def __init__(self) -> None:
        self._bypass = True
        self._time = 0

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def time(self) -> float:
        return self._time

    @time.setter
    def time(self, value: float):
        assert(0 < value < 0.01)
        self._time = value


class ClipLimiter:
    def __init__(self) -> None:
        self._bypass = True
        self._mode = ClipLimiterMode.NORMAL

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def mode(self) -> ClipLimiterMode:
        return self._mode

    @mode.setter
    def mode(self, value: ClipLimiterMode):
        assert(value in ClipLimiterMode)
        self._mode = value


class PeakLimiter:
    def __init__(self) -> None:
        self._bypass = True
        self._auto = True
        self._threshold = 0
        self._attack = 0
        self._release = 0
        self._hold = 0
        self._knee = 0

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def auto(self) -> bool:
        return self._auto

    @auto.setter
    def auto(self, value: bool):
        self._auto = value

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float):
        self._threshold = value

    @property
    def attack(self) -> float:
        return self._attack

    @attack.setter
    def attack(self, value: float):
        self._attack = value

    @property
    def release(self) -> float:
        return self._release

    @release.setter
    def release(self, value: float):
        self._release = value

    @property
    def hold(self) -> float:
        return self._hold

    @hold.setter
    def hold(self, value: float):
        self._hold = value

    @property
    def knee(self) -> float:
        return self._knee

    @knee.setter
    def knee(self, value: float):
        self._knee = value


class RmsLimiter:
    def __init__(self) -> None:
        self._bypass = True
        self._threshold = 0
        self._attack = 0
        self._release = 0
        self._hold = 0
        self._knee = 0

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def threshold(self) -> float:
        return self._threshold

    @threshold.setter
    def threshold(self, value: float):
        self._threshold = value

    @property
    def attack(self) -> float:
        return self._attack

    @attack.setter
    def attack(self, value: float):
        self._attack = value

    @property
    def release(self) -> float:
        return self._release

    @release.setter
    def release(self, value: float):
        self._release = value

    @property
    def hold(self) -> float:
        return self._hold

    @hold.setter
    def hold(self, value: float):
        self._hold = value

    @property
    def knee(self) -> float:
        return self._knee

    @knee.setter
    def knee(self, value: float):
        self._knee = value


class Fir:
    def __init__(self) -> None:
        self._bypass = True
        self._taps = []

    @property
    def bypass(self) -> bool:
        return self._bypass

    @bypass.setter
    def bypass(self, value: bool):
        self._bypass = value

    @property
    def taps(self) -> List[float]:
        return self._taps

    @taps.setter
    def taps(self, value: List[float]):
        self._taps = value


class SpeakerPreset:
    def __init__(self) -> None:
        self._output_mode = OutputMode.OUTPUT_MODE_8R
        self._polarity = 1
        self._output_highpass = None

        self._eq = [Equalizer() for i in range(15)]
        self._xr = Crossover()
        self._delay = Delay()
        self._fir = Fir()
        self._clip_limiter = ClipLimiter()
        self._peak_limiter = PeakLimiter()
        self._rms_limiter = RmsLimiter()

    @property
    def output_mode(self) -> OutputMode:
        return self._output_mode

    @output_mode.setter
    def output_mode(self, value: OutputMode):
        self._output_mode = value

    @property
    def polarity(self) -> int:
        return self._polarity

    @polarity.setter
    def polarity(self, value: int):
        assert(value in [-1, 1])
        self._polarity = value

    @property
    def output_highpass(self) -> Optional[float]:
        return self._output_highpass

    @output_highpass.setter
    def output_highpass(self, value: Optional[float]):
        assert(value is None or value in [20, 20000])
        self._output_highpass = value

    @property
    def equalizer(self) -> List[Equalizer]:
        return self._eq

    @equalizer.setter
    def equalizer(self, value: List[Equalizer]):
        self._eq = value

    @property
    def crossover(self) -> Crossover:
        return self._xr

    @crossover.setter
    def crossover(self, value: Crossover):
        self._xr = value

    @property
    def clip_limiter(self) -> ClipLimiter:
        return self._clip_limiter

    @clip_limiter.setter
    def clip_limiter(self, value: ClipLimiter):
        self._clip_limiter = value

    @property
    def peak_limiter(self) -> PeakLimiter:
        return self._peak_limiter

    @peak_limiter.setter
    def peak_limiter(self, value: PeakLimiter):
        self._peak_limiter = value

    @property
    def rms_limiter(self) -> RmsLimiter:
        return self._rms_limiter

    @rms_limiter.setter
    def rms_limiter(self, value: RmsLimiter):
        self._rms_limiter = value

    @property
    def fir(self) -> Fir:
        return self._fir

    @fir.setter
    def fir(self, value: Fir):
        self._fir = value
