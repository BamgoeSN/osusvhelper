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



class Element(metaclass=ABCMeta):
    @abstractmethod
    def getElmType(self):
        pass
    @abstractmethod
    def getPos(self):
        pass



class Interval(Element):
    def __init__(self, startPos, startValue, endPos, endValue, easeType, io):
        self.startPos = startPos             # fraction
        self.startValue = startValue         # float
        self.endPos = endPos                 # fraction
        self.endValue = endValue             # float
        self.easeType = easeType             # string
        self.io = io                         # string

    def getElmType(self):
        return "interval"

    def getPos(self):
        '''
        getPos is for getting startPos for preventing interval overlap.
        This will be used when inserting elements in Palette.data.
        '''
        return self.startPos



class Point(Element):
    def __init__(self, pos, value):
        self.pos = pos                       # fraction
        self.value = value                   # float

    def getElmType(self):
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
        if point.pos > self.intervalLength:
            return -2
        ind = bi.bisect_left(self.pos, point.pos)
        
        # Prev
        if ind <= len(self.pos) and ind > 0:
            prevElm = self.data[ind-1]
            if prevElm.getElmType() == "point":
                if prevElm.pos >= point.pos:
                    return -1
            elif prevElm.getElmType() == "interval":
                if prevElm.startPos >= point.pos:
                    return -1
                if prevElm.endPos > point.pos:
                    return -1
        # Next
        if ind < len(self.pos) and ind >= 0:
            nextElm = self.data[ind]
            if nextElm.getElmType() == "point":
                if nextElm.pos <= point.pos:
                    return -1
            elif nextElm.getElmType() == "interval":
                if nextElm.startPos <= point.pos:
                    return -1

        return ind


    def isValidInterval(self, interval):
        if interval.startPos > self.intervalLength or interval.endPos > self.intervalLength:
            return -2
        ind = bi.bisect_left(self.pos, interval.startPos)

        # Prev
        if ind <= len(self.pos) and ind > 0:
            prevElm = self.data[ind-1]
            if prevElm.getElmType() == "point":
                if prevElm.pos >= interval.startPos:
                    return -1
            elif prevElm.getElmType() == "interval":
                if prevElm.startPos >= interval.startPos:
                    return -1
                elif prevElm.endPos > interval.startPos:
                    return -1
        # Next
        if ind < len(self.pos) and ind >= 0:
            nextElm = self.data[ind]
            if nextElm.getElmType() == "point":
                if nextElm.pos < interval.endPos:
                    return -1
            elif nextElm.getElmType() == "interval":
                if nextElm.startPos < interval.endPos:
                    return -1

        return ind
        

    def isValid(self, element):
        '''
        Checks if the element does not overlap with other elements.
        Returns -1 if the element is not valid.
        Returns -2 if the element is out of time range
        Returns the position the element should be inserted if it's valid.
        For example, if self.pos==[0,1,2] and element.getPos()==1.5,
        self.isValid(element) == 2.
        '''
        if element.getElmType() == "point":
            return self.isValidPoint(element)
        elif element.getElmType() == "interval":
            return self.isValidInterval(element)
        else:
            raise TypeError("Invalid type of element")


    def insert(self, element):
        ind = self.isValid(element)
        if ind == -1:
            raise ValueError("Invalid element: the element overlaps with another element already presents")
        elif ind == -2:
            raise ValueError("Invalid element: position of the element is out of the palette range")
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

    def pickPalette(self, palette):
        if palette == "sv":
            return self.sv
        elif palette == "vo":
            return self.vo
        else:
            raise ValueError("Invalid palette type")

    def insertPoint(self, palette, pos, value):
        target = self.pickPalette(palette)
        point = Point(pos, value)
        target.insert(point)

    def insertInterval(self, palette, startPos, startValue, endPos, endValue, easeType, io):
        target = self.pickPalette(palette)
        interval = Interval(startPos, startValue, endPos, endValue, easeType, io)
        target.insert(interval)

    def deleteElement(self, palette, index):
        target = self.pickPalette(palette)
        target.delete(index)
