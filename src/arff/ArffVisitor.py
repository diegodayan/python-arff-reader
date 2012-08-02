#!/usr/bin/python
# Filename: ArffVisitor.py

version = "0.1"
author = "Diego Dayan"

class ArffFileVisitor:
	
	def __init__(self, arff):
		self._arff = arff
		
	def visitHeader(self):
		print "\nVisting ARFF..."
		print "Relation name is %s. It has %d attributes and %d records." % (self._arff.relationName, self._arff.countOfAttributes, self._arff.countOfRecords)
		
	def visitAttributes(self):
		print "\nAttributes are:"
		count = 1
		for attr in self._arff.attributes:
			print " %2d) %s" % (count, str(attr))
			count += 1
			
	def visitRecords(self):
		print "\nDisplaying records:"
		count = 1
		for record in self._arff.records:
			print " %4d) %s" % (count, str(record))
			count += 1	
	
	def visitRecordsSample(self):		
		print "\nDisplaying a few records:"
		count = 1
		for record in self._arff.records:
			if count <= 15:
				print " %2d) %s" % (count, str(record))
				count += 1
		
	def visitSample(self):
		self.visitHeader()
		self.visitAttributes()
		self.visitRecordsSample()
		
	def visitAll(self):
		self.visitHeader()
		self.visitAttributes()
		self.visitRecords()

# End of ArffVisitor.py