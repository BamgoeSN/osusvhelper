from abc import ABCMeta, abstractmethod

class Timing(metaclass=ABCMeta):
    time = "time"
    sampleSet = "sampleSet"
    sampleIndex = "sampleIndex"
    volume = "volume"
    effects = "effects"
    @abstractmethod
    def getString(self):
        pass


class Inherited(Timing):
    def __init__(self, time, sv, sampleSet, sampleIndex, volume, effects):
        self.time = time
        self.sv = sv
        self.sampleSet = sampleSet
        self.sampleIndex = sampleIndex
        self.volume = volume
        self.effects = effects
    def getBeatLength(self):
        return -100/self.sv
    def getString(self):
        return f"{self.time},{self.getBeatLength()},0,{self.sampleSet},{self.sampleIndex},{self.volume},0,{self.effects}"


class Unnherited(Timing):
    def __init__(self, time, bpm, meter, sampleSet, sampleIndex, volume, effects):
        self.time = time
        self.bpm = bpm
        self.meter = meter
        self.sampleSet = sampleSet
        self.sampleIndex = sampleIndex
        self.volume = volume
        self.effects = effects
    def getBeatLength(self):
        return 60000/self.bpm
    def getString(self):
        return f"{self.time},{self.getBeatLength()},{self.meter},{self.sampleSet},{self.sampleIndex},{self.volume},1,{self.effects}"