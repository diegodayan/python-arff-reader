__author__ = "Diego Dayan"
__version__ = "0.1"

class ArffIntegrityChecker:
    def __init__(self, arff):
        self._arff = arff

    def check(self):
        self.countAttributes()
        self.checkDistinctAttributes()
        self.countRecords()
        self.countColumns()

    def countAttributes(self):
        count = 0
        for _ in self._arff.attributes:
            count += 1
        assert count == self._arff.countOfAttributes

    def countRecords(self):
        count = 0
        for _ in self._arff.records:
            count += 1
        assert count == self._arff.countOfRecords

    def countColumns(self):
        for record in self._arff.records:
            count = 0
            for _ in record.values:
                count += 1
            assert count == self._arff.countOfAttributes

    def checkDistinctAttributes(self):
        dict = {}
        for attr in self._arff.attributes:
            assert attr.name not in dict
            dict[attr.name] = 1

    def containsMissingValues(self):
        for record in self._arff.records:
            for value in record.values:
                if value in ["?", None]:
                    return True
        return False