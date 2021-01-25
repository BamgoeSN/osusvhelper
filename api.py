from intervalFormat import *

data = 0

def initialize(startTime, initialBPM, intervalLength):
    data = Data(startTime, initialBPM, intervalLength)

def pickPalette(palette):
    if palette == "sv":
        return data.sv
    elif palette == "vo":
        return data.vo
    else:
        raise ValueError("Invalid palette type")

def insertPoint(palette, pos, value):
    target = pickPalette(palette)
    point = Point(pos, value)
    target.insert(point)

def insertInterval(palette, startPos, startValue, endPos, endValue, easeType, io):
    target = pickPalette(palette)
    interval = Interval(startPos, startValue, endPos, endValue, easeType, io)
    target.insert(interval)

def deleteElement(palette, index):
    target = pickPalette(palette)
    target.delete(index)