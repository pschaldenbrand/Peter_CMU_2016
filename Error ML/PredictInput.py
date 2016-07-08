import math
import sys
import os

#leftBigram = Bigram()
#rightBigram  = Bigram()
canonize = True

givenCorrectness = True
correctness = 'incorrect'

def main():
	leftBigram = Bigram()
	rightBigram  = Bigram()
	
	makeBigrams(leftBigram, rightBigram)
	
	#print str(leftBigram.probability(convertConstants('1=9-x'),'c0'))
	#print str(leftBigram.mostLikelyOutput(convertConstants('1=9-x')))
	
	testBigrams(leftBigram,rightBigram)
	
def testBigrams( lb, rb ):
	fn = 'gill3output.txt'
	
	correct = 0
	outOf = 0
	
	for line in open(fn, 'r').readlines():
		tokens = line.split('\t')
		
		if givenCorrectness:
			if (tokens[2].lower() != correctness):
				continue
		
		given = tokens[0].replace('\s+','')
		
		leftInput = tokens[0].split('=')[0].replace('\s+','')
		rightInput= tokens[1].split('=')[0].replace('\s+','')
		
		if canonize:
			leftInput = convertConstants(leftInput)
			rightInput = convertConstants(rightInput)
			given = convertConstants(given)
		#print leftInput+'\t'+rightInput+'\t'+given
		
		predictLeft = lb.mostLikelyOutput(given)
		predictRight = rb.mostLikelyOutput(given)
		
		
		'''if leftInput != '$' and predictLeft != '':
			#print leftInput + "\t" + predictLeft
			if predictLeft == leftInput:
				correct += 1
			outOf += 1
		if rightInput != '$' and predictRight != '':
			#print rightInput + "\t" + predictRight
			if predictRight == rightInput:
				correct+= 1
			#else:
			#	print rightInput + "\t" + predictRight
			outOf += 1'''
		
		top2L = lb.topFour(given)
		top2R = rb.topFour(given)
		
		if leftInput != '$' and top2L != '':
			if leftInput in  top2L:
				correct+=1
			outOf+=1
		
		if rightInput != '$' and top2R != '':
			if rightInput in top2R:
				correct+=1
			outOf+=1
	
	print str(correct) + " / " + str(outOf)
	print str(float(correct)/outOf)

def makeBigrams( lb, rb ):
	#trainFiles = ['delete.txt','roberts2output.txt','roberts3output.txt']
	trainFiles = ['megaOutput.txt']
	
	for fn in trainFiles:
		for line in open(fn, 'r').readlines():
			tokens = line.split('\t')
			
			if givenCorrectness:
				if (tokens[2].lower() != correctness):
					continue
			
			l = tokens[1].split('=')[0].replace('\s+','')
			r = tokens[1].split('=')[1].replace('\s+','')
			
			given = tokens[0].replace('\s+','')
			
			if canonize:
				l = convertConstants(l)
				r = convertConstants(r)
				given = convertConstants(given)
			
			if l != '$':
				lb.add(given, l)
			if r != '$':
				rb.add(given, r)
		
	#lb.printWholeThing()
	#rb.printWholeThing()
	

class Bigram(object):
	counts = []
	bigram = []
	givens = []
	def __init__(self):
		self.bigram = []
		self.counts = []
		self.givens = []
	def add(self, given, cond):
		#print given + "\t"+cond
		if given not in self.givens:
			self.givens.append(given)
			self.bigram.append({})
			self.counts.append(0)
			#self.bigram[self.givens.index(given)] = {}
		index = self.givens.index(given)
		
		added = False
		for conditionalEq in self.bigram[index].keys():
			if conditionalEq == cond:
				self.bigram[index][cond] += 1
				added = True
		if not added:
			self.bigram[index][cond] = 1
		
		self.counts[index] += 1
		
	def probability (self, given, cond):
	
		if given not in self.givens:
			return -1
			
		index = self.givens.index(given)
		
		if cond not in self.bigram[index].keys():
			return-2
		
		times = self.bigram[index][cond]
		outOf = self.counts[index]
		
		return float(times)/self.calcCounts(given)
	
	def calcCounts( self, given ):		
			
		index = self.givens.index(given)
		c = 0
		for key in self.bigram[index].keys():
			c += self.bigram[index][key]
		return c
	
	def mostLikelyOutput(self, given):

		if given not in self.givens:
			return ""
		
		index = self.givens.index(given)
		
		maxProb = 0
		maxOutput = ''
		for cond in self.bigram[index].keys():
			#print '\t' + cond + ":\t" + str(self.probability(given,cond))
			if self.probability(given,cond) > maxProb:
				maxProb = self.probability(given,cond)
				maxOutput = cond
		
		return maxOutput
	
	def topTwo( self, given ):
		if given not in self.givens:
			return ""
		
		index = self.givens.index(given)
		
		maxProb = 0
		secondprob = 0
		maxOutput = ''
		second = ''
		for cond in self.bigram[index].keys():
			#print '\t' + cond + ":\t" + str(self.probability(given,cond))
			prob = self.probability(given,cond)
			if prob > maxProb:
				secondProb = maxProb
				second = maxOutput
				maxProb = self.probability(given,cond)
				maxOutput = cond
			elif prob > secondprob:
				secondprob = prob
				second = cond
		
		return [maxOutput,second]
	
	def topFour( self, given ):
		if given not in self.givens:
			return ""
		
		index = self.givens.index(given)
		
		firstProb = 0
		secondProb = 0
		thirdProb = 0
		fourthProb = 0
		first = ''
		second = ''
		third = ''
		fourth = ''
		print str(len(self.bigram[index].keys()))
		for cond in self.bigram[index].keys():
			#print '\t' + cond + ":\t" + str(self.probability(given,cond))
			prob = self.probability(given,cond)
			if prob > firstProb:
				fourthProb = thirdProb
				fourth = third
				thirdProb = secondProb
				third = second
				secondProb = firstProb
				second = first
				firstProb = prob
				first = cond
			elif prob > secondProb:
				fourthProb = thirdProb
				fourth = third
				thirdProb = secondProb
				third = second
				secondprob = prob
				second = cond
			elif prob > thirdProb:
				fourthProb = thirdProb
				fourth = third
				thirdProb = prob
				third = cond
			elif prob > fourthProb:
				fourthProb = prob
				fourth = cond
		
		return [first,second,third,fourth]
	
	def printWholeThing(self):
		for i in range(0,len(self.bigram)):
			for cond in self.bigram[i].keys():
				print self.givens[i] + " " + cond + " " + str(self.bigram[i][cond])

				
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