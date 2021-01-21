# Refer to https://osu.ppy.sh/wiki/en/osu!_File_Formats/Osu_(file_format)
# for detailed .osu file format.

'''
"Position" is used for pointing timelines, instead of ms(miliseconds).
The position works just as identical as the fraction notation from the
beginning of target interval to the target timing point, and its type
is fractions.Fraction.
'''



class Interval:
    def __init__(self, startPos, startValue, endPos, endValue, easeType, io):
        self.startPos = startPos             # fraction
        self.startValue = startValue         # float
        self.endPos = endPos                 # fraction
        self.endValue = endValue             # float
        self.easeType = easeType             # string
        self.io = io                         # string

    def getPos(self):
        '''
        getPos is for getting startPos for preventing interval overlap.
        This will be used when inserting elements in Palette.data.
        '''
        return self.startPos



class Point:
    def __init__(self, pos, value):
        self.pos = pos                       # fraction
        self.value = value                   # float

    def getPos(self):
        '''
        getPos is for getting pos for preventing interval overlap.
        This will be used when inserting elements in Palette.data.
        '''
        return self.pos



class Palette:
    def __init__(self, startTime, initialBPM, intervalLength, target):
        self.startTime = startTime           # float, in ms
        self.initialBPM = initialBPM         # int
        self.intervalLength = intervalLength # fraction
        self.data = []                       # list of Intervals and Points
        self.pos = []                        # list of positions of Intervals and Points in self.data
        self.type = target                   # string: "sv" or "vol"



class Data:
    def __init__(self, startTime, initialBPM, intervalLength):
        self.sv = Palette(startTime, initialBPM, intervalLength, "sv")
        self.vo = Palette(startTime, initialBPM, intervalLength, "vo")
