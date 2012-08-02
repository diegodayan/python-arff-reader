__author__ = "Diego Dayan"
__version__ = "0.1"

class ArffDiscretizer:
	
	def __init__(self, arff):
		self._arff = arff
	
	def discretizeUsingBins(self):	
		for attr in self._arff.attributes:
			if attr.isContinuous:
				attr.isContinuous = 0
				attr.dataType = "NOMINAL"
				attr.values = self.createBins(attr.nbrOfBins)
				for value in attr.values:
					attr.valuesCount[str(value)] = 0
				for record in self._arff.records:
					record.values[attr.index] = self.getBinFor(record.values[attr.index], attr.max, attr.min, attr.nbrOfBins)
					
	def getBinFor(self, value, max, min, nbrOfBins):
		""" From 0 to nbrOfBins - 1 """
		if value == max:
			return nbrOfBins - 1
		else:
			binSize = (float(max) - float(min)) / float(nbrOfBins)
			return int(round(float(value - min) / binSize))
		
	def createBins(self, nbrOfBins):
		return range(nbrOfBins)