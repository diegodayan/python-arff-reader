__author__ = "Diego Dayan"
__version__ = "0.1"

from src.arff.ArffFile import ArffFile

class ArffMetadataComputer(object):
    def __init__(self, arff):
        assert isinstance(arff, ArffFile)
        self.arff = arff

    def preprocess(self):
        for attr in self.arff.attributes:
            attr.missing = 0
            attr.sum = 0.
            attr.max = 0.
            attr.min = 0.
            attr.stdDev = 0.
            attr.valuesCount = {}
        for record in self.arff.records:
            for attr in self.arff.attributes:
                value = record.values[attr.index]
                if  value in ["?", None]:
                    attr.missing += 1
                    continue
                elif attr.isContinuous:
                    attr.sum += float(value)
                    if attr.max is None or value > attr.max:
                        attr.max = value
                    elif attr.min is None or value < attr.min:
                        attr.min = value
                elif record.values[attr.index] in attr.valuesCount:
                    attr.valuesCount[record.values[attr.index]] += 1
                else:
                    attr.valuesCount[record.values[attr.index]] = 1
        for attr in self.arff.attributes:
            if attr.isContinuous:
                attr.mean = float(attr.sum) / float(self.arff.countOfRecords)
                values = []
                for record in self.arff.records:
                    values.append(record.values[attr.index])
                values.sort()
                attr.median = values[int(len(values) / 2)]
            else:
                maxValue = 0
                for key, value in attr.valuesCount.items():
                    if value > maxValue:
                        attr.mode = key
                        maxValue = value