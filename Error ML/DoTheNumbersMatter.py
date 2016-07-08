import math
import sys
import os

model = []

def main():
	for l in range(0,2):
		canonize = False
		if l == 1:
			canonize = True
		allLines = open('legtersOutput.txt','r').readlines()
		
		model.append(ErrorProb())
		
		for line in allLines:
			tokens = line.split('\t')
			eq = tokens[0]
			outcome = tokens[2]
			if canonize:
				eq = convertConstants(eq)
			
			model[l].add(eq, outcome)
		#model[l].printModel()
		#print '\n\n\n\n\n'
		testModel(model[l], canonize)
		
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
	def getProb(self, eq):
		return (float(self.prob[eq][0])/self.prob[eq][1])
	def printModel(self):
		for key in self.prob.keys():
			print key +'\t'+ str(float(self.prob[key][0])/self.prob[key][1])

def testModel(m, canonize):
	fn = 'roberts3output.txt'
	results = {}
	for line in open(fn,'r').readlines():
		tokens = line.split('\t')
		eq = tokens[0]
		if canonize:
			eq = convertConstants(eq)
		
		if eq not in m.prob.keys():
			continue
		
		probOfIncorr = m.getProb(eq)
		theoretical = 'incorrect'
		if probOfIncorr < .5:
			theoretical = 'correct'
			
		result = tokens[2].lower()
		
		modelCorrect = False
		
		if theoretical == result:
			modelCorrect = True
		
		if eq not in results.keys():
			results[eq] = [0,0]
		
		if modelCorrect:
			results[eq][0] = results[eq][0] + 1
		results[eq][1] = results[eq][1] + 1
	'''print results
	for key in results.keys():
		if results[key][0] > 0:
			print results[key]
	print '\n\n\n\n'''
	total = 0
	times = 0
	for key in results.keys():
		total += results[key][1]
		times += results[key][0]
	print canonize
	print times
	print total
	print float(times)/total
	print

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