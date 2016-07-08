#Peter Schaldenbrand
#Read through a log file and output a file that is easier to use
#for machine learning

import math
import sys
import os

inputIndex = 0
outcomeIndex = 0
selectionIndex = 0
sidIndex = 0
problemNameIndex = 0
eqIndex = 0
feedbackIndex = 0;
transactionIndex = 0;
assignmentIndex = 0;
def main():
	
	#for fn in os.listdir('./datasets'):
		#allLines = open('datasets/'+fn,'r').readlines()
		allLines = open('bug-combine-unlike-terms-make-constant.txt','r').readlines()
		
		fields = []
		for fieldName in allLines[0].split('\t'):
			fields.append(fieldName)
		
		if (True):		#getting the field indexes
			inputIndex = fields.index('Input')
			outcomeIndex = fields.index('Outcome')
			selectionIndex = fields.index('Selection')
			sidIndex = fields.index('Anon Student Id')
			problemNameIndex = fields.index('Problem Name')
			eqIndex = fields.index('CF (preEqSys)')
			feedbackIndex = fields.index('Feedback Text')
			assignmentIndex = fields.index('Level (Assignment)')
			#transactionIndex = fields.index('CF (orig_trans_id)')
		
		
		prevPName = ''
		
		prevEq = ''
		currEqR = ''
		currEqL = ''
		
		leftCorrect = False
		rightCorrect = False
		
		for i in range(1, len(allLines)):
			line = allLines[i]
			
			tokens = line.split('\t')
			problemName = tokens[problemNameIndex]
			probEQ = tokens[eqIndex]
			sid = tokens[sidIndex]
			input = tokens[inputIndex]
			outcome = tokens[outcomeIndex].lower()
			selection = tokens[selectionIndex].lower()
			bug = tokens[feedbackIndex].lower()
			transID = tokens[transactionIndex]
			assignment = tokens[assignmentIndex]
			
			if assignment != 'Lynnette Tutor':
				continue
			
			if outcome != 'correct' and outcome != 'incorrect':
				#print "not correct or incorrect"
				continue
			
			if leftCorrect and rightCorrect:
				#print "you have completed it"
				continue
			
			if prevPName == '' or prevPName != problemName:
				#onto a new problem
				newEq = problemNameToEquation(problemName)
				leftCorrect = False
				rightCorrect = False
				prevEq = newEq
				currEqL = ''
				currEqR = ''
				prevPName = problemName
			
			if selection[:len(selection)-1] != 'solveleft' and selection[:len(selection)-1] != 'solveright':
				continue
			
			if outcome == 'correct':
				if selection[:len(selection)-1] == 'solveleft':
					leftCorrect = True
					currEqL = input
					if not rightCorrect:
						currEqR = '$'
				if selection[:len(selection)-1] == 'solveright':
					rightCorrect = True
					currEqR = input
					if not leftCorrect:
						currEqL = '$'
				#print 'correct left '+str(leftCorrect)+'\tright '+str(rightCorrect)
#				#printInstance(prevEq, currEqL+'='+currEqR, outcome, sid)
				fullEq = prevEq+' => '+currEqL+'='+currEqR
				print transID + '\t'+fullEq
				if leftCorrect and rightCorrect:
					leftCorrect = False
					rightCorrect = False
					prevEq = currEqL + '=' + currEqR
					currEquationL = ''
					currEquationR = ''
				continue
			
			if outcome == 'incorrect':
				##DO THE STUFF WITH PUTTING IT IN THE EQUATION AND STUFF
				if selection[:len(selection)-1] == 'solveleft':
					currEqL = input
					if not rightCorrect:
						currEqR = '$'
				if selection[:len(selection)-1] == 'solveright':
					currEqR = input
					if not leftCorrect:
						currEqL = '$'
				if selection[:len(selection)-1] != 'solveleft' and selection[:len(selection)-1] != 'solveright':
					continue
				#print 'incorrect left '+str(leftCorrect)+'\tright '+str(rightCorrect)
#				#printInstance(prevEq, currEqL+'='+currEqR, outcome, sid)
				fullEq = prevEq+' => '+currEqL+'='+currEqR
				print transID + '\t'+fullEq
				#print bug+'\t'+convertConstants(fullEq)+'\t'+fullEq
			
def printInstance(pEq, cEq, outcome, sid):
	print pEq +'\t'+ cEq +'\t'+ outcome +'\t'+ sid
	
def problemNameToEquation(pn):
	pn = pn.replace(' ','+')
	pn = pn.replace('\s+','')
	return pn

class ErrorProb (object):
	prob = {}
	def __init__(self):
		self.prob = {}
	def add(self, eq, outcome):
		if eq not in self.prob.keys():
			self.prob[eq] = [0,0]
		
		if outcome == 'incorrect':
			self.prob[eq][0] = self.prob[eq][0] + 1
		
		self.prob[eq][1] = self.prob[eq][1] + 1
				
def convertConstants( s ):
	num =  0
	ret = ''
	j = 0
	while( j < len(s) ):
		char = s[j]
		if char in ['1','2','3','4','5','6','7','8','9','0']:
			const = char
			if j != len(s)-1:
				if s[j+1] in ['1','2','3','4','5','6','7','8','9','0']:
					const = const +s[j+1]
					j = j + 1
			constantValue = 'c'+str(num)
			num+=1
			ret = ret + constantValue
		else:
			ret = ret + char
		j+=1
	return ret

if __name__ == "__main__": main()