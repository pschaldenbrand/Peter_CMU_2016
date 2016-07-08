import math
import sys

def main():
	allLines = open('MegaData.txt','r').readlines()
		
	fields = []
	for fieldName in allLines[0].split('\t'):
		fields.append(fieldName)
	print allLines[0][0:len(allLines[0])-1]

	if (True):		#getting the field indexes
		inputIndex = fields.index('Input')
		outcomeIndex = fields.index('Outcome')
		selectionIndex = fields.index('Selection')
		sidIndex = fields.index('Anon Student Id')
		problemNameIndex = fields.index('Problem Name')
		eqIndex = fields.index('CF (preEqSys)')
		feedbackIndex = fields.index('Feedback Text')
		assignmentIndex = fields.index('Level (Assignment)')
		
	for i in range(1, len(allLines)):
		line = allLines[i]
		tokens = line.split('\t')
		assignment = tokens[assignmentIndex]
			
		if assignment != 'Lynnette Tutor':
			continue
		print line[0:len(line)-1]
		
		
if __name__ == "__main__": main()