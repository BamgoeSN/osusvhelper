# Refer to https://osu.ppy.sh/wiki/en/osu!_File_Formats/Osu_(file_format)
# for detailed .osu file format.

'''
"Position" is used for pointing timelines, instead of ms(miliseconds).
The position works just as identical as the fraction notation from the
beginning of target interval to the target timing point, and its type
is fractions.Fraction.
'''

from abc import ABCMeta, abstractmethod
import bisect as bi



class Timeline(metaclass=ABCMeta):
    @abstractmethod
    def elmType(self):
        pass
    @abstractmethod
    def getPos(self):
        pass



class Interval(Timeline):
    def __init__(self, startPos, startValue, endPos, endValue, easeType, io):
        self.startPos = startPos             # fraction
        self.startValue = startValue         # float
        self.endPos = endPos                 # fraction
        self.endValue = endValue             # float
        self.easeType = easeType             # string
        self.io = io                         # string

    def elmType(self):
        return "interval"

    def getPos(self):
        '''
        getPos is for getting startPos for preventing interval overlap.
        This will be used when inserting elements in Palette.data.
        '''
        return self.startPos



class Point(Timeline):
    def __init__(self, pos, value):
        self.pos = pos                       # fraction
        self.value = value                   # float

    def elmType(self):
        return "point"

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


    def isValidPoint(self, point):
        elmPos = point.getPos()
        ind = bi.bisect_left(self.pos, elmPos)
        if ind == 0:
            return ind
        elif self.pos[ind] == elmPos:
            return -1
        elif (self.data[ind-1].elmType() == "interval") and (self.data[ind-1].endPos > elmPos):
            return -1
        return ind

    def isValidInterval(self, interval):
        # TODO
        elmPos = interval.getPos()
        ind = bi.bisect_left(self.pos, elmPos)

    def isValid(self, element):
        '''
        Checks if the element does not overlap with other elements.
        Returns -1 if the element is not valid.
        Returns the position the element should be inserted if it's valid.
        For example, if self.pos==[0,1,2] and element.getPos()==1.5,
        self.isValid(element) == 2.
        '''
        if element.elmType() == "point":
            return self.isValidPoint(element)
        elif element.elmType() == "interval":
            return self.isValidInterval(element)
        else:
            raise TypeError("Invalid type of element")


    def insert(self, element):
        ind = self.isValid(element)
        if ind == -1:
            raise ValueError("Invalid element: the element overlaps with another element already presents")
        else:
            self.data.insert(ind, element)
            self.pos.insert(ind, element.getPos())

    def delete(self, index):
        '''
        Deletes self.data[ind] and self.pos[ind]
        '''
        del self.data[index]
        del self.pos[index]



class Data:
    def __init__(self, startTime, initialBPM, intervalLength):
        self.sv = Palette(startTime, initialBPM, intervalLength, "sv")
        self.vo = Palette(startTime, initialBPM, intervalLength, "vo")
