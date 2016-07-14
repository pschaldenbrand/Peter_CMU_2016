#Peter Schaldenbrand

import math
import sys
import os
import operator
from operator import itemgetter, attrgetter, methodcaller

constants = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o','p','0']
digits = ['0','1','2','3','4','5','6','7','8','9']

PROBLEM_SET = "ProblemSetDashboard_1"
MAX_INPUT_SIZE = 20
BIN_SIZE_IN_MINUTES = 1

schemes = [{}]
data = {}
pattToAttempts = {}
attemptCurve = []
timeCurve = {}

def main():
	makeData()
	#learningCurveByAttempt()
	learningCurveByTime()



def makeData():
	for line in open('megaOutputTime.txt','r'):
		tokens = line.split('\t')
		
		'''if tokens[3] != PROBLEM_SET:
			continue'''
		
		pattern = tokens[0].replace(' ','')
		response = tokens[1].replace('$','____').replace(' ','')
		
		correctness = tokens[2]
		sid = tokens[4]
		timeStr = tokens[5]
		time = getTimeInSec(timeStr)
		
		reusage = reuse(pattern,response)
		canonPatt = reusage[0]
		canonResp = reusage[1]
		
		if sid not in data.keys():
			data[sid] = {}
		if canonPatt not in data[sid].keys():
			data[sid][canonPatt] = []
		newAttempt = [canonResp, correctness, time]
		data[sid][canonPatt].append(newAttempt)
		
		if canonPatt not in pattToAttempts.keys():
			pattToAttempts[canonPatt] = 0
		pattToAttempts[canonPatt] += 1
		
	sortedPatt = sorted(pattToAttempts.items(), key=operator.itemgetter(1), reverse=True)

	
def learningCurveByAttempt():
	sortedPatt = sorted(pattToAttempts.items(), key=operator.itemgetter(1), reverse=True)
	topPattern = sortedPatt[0][0]
	pattern = topPattern
	
	for sid in data.keys():
		for pat in data[sid].keys():
			if pat != pattern:
				continue
			for i in range(0,len(data[sid][pattern])):
				resp = data[sid][pattern][i]
				if i >= len(attemptCurve):
					attemptCurve.append([0,0])
				if resp[1] == 'correct':
					attemptCurve[i][0] += 1
				else:
					attemptCurve[i][1] += 1
	print pattern
	for i in range(0,len(attemptCurve)):
		rslt = attemptCurve[i]
		print str(i+1)+'\t'+str(rslt[0])+'\t'+str(rslt[1])
	
def learningCurveByTime():
	sortedPatt = sorted(pattToAttempts.items(), key=operator.itemgetter(1), reverse=True)
	topPattern = sortedPatt[0][0]
	pattern = topPattern
	
	print pattern
	
	binSize = float(BIN_SIZE_IN_MINUTES) * 60
	
	for sid in data.keys():
		if pattern not in data[sid].keys():
			continue
		list = data[sid][pattern]
		list.sort(key=operator.itemgetter(2))
		studStart = list[0][2]
		for resp in list:
			timeSinceStart = resp[2]-studStart
			bin = int(timeSinceStart / binSize)
			if bin not in timeCurve.keys():
				timeCurve[bin] = [0,0]
			if resp[1] == 'correct':
				timeCurve[bin][0] += 1
			else:
				timeCurve[bin][1] += 1
	
	sortedCurve = sorted(timeCurve.items(),key=operator.itemgetter(0))
	for bin in sortedCurve:
		print str(bin[0]*BIN_SIZE_IN_MINUTES)+'\t'+str(bin[1][0])+'\t'+str(bin[1][1])

	
'''	Same value constants get the same letter
	Ex.	3x-4=4x+2   ->   ax-b=bx+d  '''
def reuse(pattern, response):
	if len(pattern) > MAX_INPUT_SIZE or len(response) > MAX_INPUT_SIZE:
		return ['','']
	constantsUsed= {}
	ret = []
	constInd = 0
	canonEq = ''
	onNumber = False
	fullEq = pattern + "separator" + response
	
	for i in range(0,len(fullEq)):
		if fullEq[i] in digits and onNumber == True:
			continue
		onNumber = False
		if fullEq[i] not in digits:
			canonEq = canonEq + fullEq[i]
			continue
		currConst = ''
		for j in range(i,len(fullEq)):
			if fullEq[j] in digits:
				currConst += fullEq[j]
			else:
				break
		if currConst == '0':
			canonEq = canonEq + '0'
		elif currConst not in constantsUsed:
			constantsUsed[currConst] = constInd
			constInd += 1
			canonEq = canonEq + constants[constantsUsed[currConst]]
		else:
			canonEq = canonEq + constants[constantsUsed[currConst]]
		onNumber = True
	
	splitted = canonEq.split('separator')
	return splitted


def getTimeInSec(timeStr):
	hsm = timeStr.split(' ')[1].split(':')
	hours = float(hsm[0])
	minutes = float(hsm[1])
	seconds = float(hsm[2])
	
	time = (hours*60*60)+(minutes*60)+(seconds)
	return time
	
	
if __name__ == "__main__": main()