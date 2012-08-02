__author__ = "Diego Dayan"
__version__ = "0.1"

from src.arff.ArffFile import *

class ArffFileWriter(object):
    def __init__(self, arff, file):
        assert isinstance(arff, ArffFile)
        self.arff = arff
        self.file = file
        self.outputStream = None

    def write(self):
        self.outputStream = open(self.file, "w")
        self._writeHeader()
        self._writeAttributes()
        self._writeRecords()
        self.outputStream.close()

    def _writeHeader(self):
        self.outputStream.write("@RELATION " + self.arff.relationName + "\n")

    def _writeAttributes(self):
        self.outputStream.write("\n")
        for attr in self.arff.attributes:
            line = "@ATTRIBUTE"\
                   + " " + attr.name + "\t"
            if attr.isContinuous:
                line += " NUMERIC"
            else:
                line += " {"
                for value in attr.getValues():
                    line += str(value) + ", "
                line = line.strip(", ") + "}"
            self.outputStream.write(line + "\n")

    def _writeRecords(self):
        self.outputStream.write("\n@DATA\n")
        for record in self.arff.records:
            line = ""
            for value in record.values:
                line += str(value) + ", "
            line = line.strip(", ")
            self.outputStream.write(line + "\n")
