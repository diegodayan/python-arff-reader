__author__ = "Diego Dayan"
__version__ = "0.1"

from src.config.Config import *

class ArffAttribute(object):
    """
    Name can be any alphanumerical value
    DataType can be any of STRING, NUMERIC or NOMINAL
    """

    def __init__(self, index, name, dataType):
        self.index = index
        self.name = name
        self.isContinuous = False
        self.dataType = dataType.strip()
        self.values = None
        self.valuesCount = {}
        self.missing = 0
        self.mean = 0
        self.median = 0
        self.mode = None
        self.sum = 0
        self.min = None
        self.max = None
        self.stdDev = 0
        self.nbrOfBins = 0

        if self.dataType in ["NUMERIC", "INTEGER", "REAL"]:
            self.isContinuous = True

        elif dataType not in ["NUMERIC", "INTEGER", "REAL", "STRING"]:
            self.values = self.dataType[1:-1].split(",")
            self.nbrOfBins = len(self.values)
            self.dataType = "NOMINAL"
            for i in range(self.nbrOfBins):
                self.values[i] = self.values[i].strip()

    def getValues(self):
        values = []
        for k in self.valuesCount.iterkeys():
            values.append(k)
        return values

    def __str__(self):
        output = "Name: %s, DataType: %s, IsContinuos: %d, Missing values: %d" % (
            self.name, self.dataType, self.isContinuous, self.missing)

        if self.isContinuous == 1:
            output += "\n\tMean: %.3f" % self.mean
            output += "\n\tMedian: %.3f" % self.median
            output += "\n\tMax: %.3f" % self.max
            output += "\n\tMin: %.3f" % self.min

        else:
            output += ", Mode: %s" % self.mode
            for key, value in self.valuesCount.items():
                output += "\n\tValue %s: %4d" % (key, value)

        return output


class ArffRecord(object):
    def __init__(self, values):
        self.values = []
        if isinstance(values, str):
            self.values = values.strip().split(",")
        else:
            self.values = values

    def __str__(self):
        return str(self.values)


class ArffFile(object):
    def __init__(self):
        self.relationName = ""
        self.records = []
        self.attributes = []
        self.countOfAttributes = 0
        self.countOfRecords = 0

    def getNameForAttribute(self, index):
        return self.attributes[index].name

    def getIndexForAttribute(self, name):
        for attr in self.attributes:
            if attr.name == name:
                return attr.index
        return -1

    def handleMissingValues(self, strategy):
        if strategy == DISCARD_RECORD:
            originalRecords = self.records # keep a copy
            self.records = [] # clear array
            for record in originalRecords:
                discard = False
                for attr in self.attributes:
                    if record.values[attr.index] == "?":
                        discard = True
                if not discard:
                    self.records.append(record)
        elif strategy == MOST_PROBABLE:
            for record in self.records:
                for attr in self.attributes:
                    if record.values[attr.index] == "?":
                        if attr.isContinuous:
                            record.values[attr.index] = attr.median
                        else:
                            record.values[attr.index] = attr.mode
        else:
            raise Exception("Unknown strategy")