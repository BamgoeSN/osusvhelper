# Refer to https://osu.ppy.sh/wiki/en/osu!_File_Formats/Osu_(file_format)
# for detailed .osu file format.

'''
"Position" is used for pointing timelines, instead of ms(miliseconds).
The position works just as identical as the fraction notation from the
beginning of target interval to the target timing point, and its type
is fractions.Fraction.
'''

import fractions as fr

class Interval:
    def __init__(self, startPos, startValue, endPos, endValue, easeType, io):
        self.startPos = startPos        # fraction
        self.startValue = startValue    # float
        self.endPos = endPos            # fraction
        self.endValue = endValue        # float
        self.easeType = easeType        # string
        self.io = io                    # string

class Point:
    def __init__(self, pos, value):
        self.pos = pos                  # fraction
        self.value = value              # float

class Palette:
    def __init__(self, type):
        self.data = []                  # list of Intervals and Points
        self.type = type                # string: "sv" or "volume"