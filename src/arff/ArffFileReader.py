__author__ = "Diego Dayan"
__version__ = "0.1"

from src.config.Config import *
from src.arff.ArffFile import *

class ArffFileReader(object):
    def __init__(self, filename):
        self.arff = ArffFile()
        self.inputStream = None
        try:
            self._readFile(filename)
        except IOError, e:
            print '\n*** Cannot open ARFF file', e
            exit()
        except Exception, e:
            print "\n*** Error while reading file at line %d:" % (-1), '"' + str(e) + '"'
            exit()

    def getArff(self):
        return self.arff

    def _readFile(self, filename):
        """
        We'll have 3 stages
        - stage 0 is for reading the relation name, @RELATION
        - stage 1 is for reading the attributes definition, @ATTRIBUTE
        - stage 2 is for reading the records, right after we see @DATA
        """
        stage = 0
        self.arff.relationName = None
        self.arff.countOfAttributes = 0
        self.arff.countOfRecords = 0
        self.inputStream = open(filename, "r")
        for l in self.inputStream.readlines():
            line = l.replace("\n", "").replace("\r", "")

            # skip comment or empty line
            if line[0:1] in ["%", " "] or len(line) == 0:
                continue

                # relation name - only at stage 0
            elif stage == 0 and line[0:9].upper() == "@RELATION":
                stage = 1
                self.arff.relationName = line[9:].strip()
                continue

            # attribute - only at stage 1
            elif stage == 1 and line[0:10].upper() == "@ATTRIBUTE":
                sanitizedLine = line[10:].replace("\t", " ").strip()
                attribute = sanitizedLine.split(" ")
                name = attribute[0]
                rest = sanitizedLine.replace(name, "").strip()
                self.arff.attributes.append(ArffAttribute(self.arff.countOfAttributes, name, rest))
                self.arff.countOfAttributes += 1
                continue

            # data - switch to stage 2, be ready to receive records
            elif stage == 1 and line[0:5].upper() == "@DATA":
                stage = 2
                continue

            # data records - only at stage 2
            elif stage == 2:
                values = line.split(",", self.arff.countOfAttributes)
                values = [value.strip() for value in values]
                for i in range(self.arff.countOfAttributes):
                    if self.arff.attributes[i].isContinuous and values[i] != "?":
                        values[i] = float(values[i])
                self.arff.records.append(ArffRecord(values))
                self.arff.countOfRecords += 1
                continue

            # oops!
            else:
                self.inputStream.close()
                raise Exception("IOException: Bad formed ARFF file!")

        self.inputStream.close()
        return self.arff