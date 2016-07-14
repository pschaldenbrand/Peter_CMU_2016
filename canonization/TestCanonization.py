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

schemes = [{},{},{},{},{}]

def main():
	createSchemes()
	
	#plotScheme(4)
	#printScheme(2)
	responseStatistics(2)

	
'''	Print out the scheme specified.
	prints the pattern, frequencies of patterns and responses to them,
	the correctness of a response, and the frequncy of responses'''
def printScheme(n):
	scheme = schemes[n]
	
	pattFreq = {}
	for pattern in scheme.keys():
		pattFreq[pattern] = 0
		for list in scheme[pattern]:
			pattFreq[pattern] += list[2]
	
	#sort pattFreq by Frequency of pattern
	sortedPatt = []
	sortedvals = sorted(pattFreq.values(), reverse=True)
	for val in sortedvals:
		for patt in pattFreq.keys():
			if val == pattFreq[patt]:
				sortedPatt.append(patt)
	
	for pattern in sortedPatt:
		print pattern
		
		list = scheme[pattern]
		list = sorted(list,key=itemgetter(2),reverse=True)
		score = [0,0]
		for resp in list:
			if resp[1].lower() == 'correct':
				score[0] += resp[2]
			score[1] += resp[2]
		perc = (float(score[0])/float(score[1]))*100
		print '\tFrequency: '+str(score[1])
		print '\tPercent Correct: '+str(perc)[:5]+'%'
		
		for resp in list:
			print '\t\t'+resp[0]+'\t'+resp[1]+'\t'+str(resp[2])
		
	
'''	prints out a table with columns representing:
	pattern, # of incorrect responses to pattern, total responses to pattern'''
def plotScheme(n):
	scheme = schemes[n]
	
	pattToScore = {}
	for pattern in scheme.keys():
		pattToScore[pattern] = [0,0]
		for list in scheme[pattern]:
			if list[1].lower() == 'incorrect':
				pattToScore[pattern][0] += list[2]
			pattToScore[pattern][1] += list[2]
	
	total = ()
	incorrect = ()
	
	for pat in pattToScore.keys():
		tempIncorr = (pattToScore[pat][0],)
		tempTotal = (pattToScore[pat][1],)
		
		tempStr = pat[:]
		if len(tempStr) < 1:
			continue
		if tempStr[0] == '-':		#fix excel issue
			tempStr = '(' + tempStr.replace('=',')=')
		
		print tempStr + '\t'+str(tempIncorr[0])+'\t'+str(tempTotal[0])
		
		incorrect = incorrect + tempIncorr
		total = total + tempTotal
	
	
'''	Creates all of the schemes and saves them in the global 
	variable "schemes"'''
def createSchemes():
	for line in open('megaOutputParenth.txt','r'):
		tokens = line.split('\t')
		
		'''if tokens[3] != PROBLEM_SET:
			continue'''
		
		pattern = tokens[0].replace(' ','')
		response = tokens[1].replace('$','____').replace(' ','')
		
		noNeg = noNegatives(pattern, response)
		noReusage = noReuse(pattern, response)
		reusage = reuse(pattern, response)
		smart = smartScheme(pattern,response)
		
		correctness = tokens[2]
		
		alreadyIn = False
		
		if noNeg[0] not in schemes[0].keys():
			schemes[0][noNeg[0]] = []
		for list in schemes[0][noNeg[0]]:
			if noNeg[1] in list:
				list[2]+=1
				alreadyIn = True
				break
		if not alreadyIn:
			alreadyIn = False
			schemes[0][noNeg[0]].append( [noNeg[1], correctness, 1] )
		alreadyIn = False
		
		if noReusage[0] not in schemes[1].keys():
			schemes[1][noReusage[0]] = []
		for list in schemes[1][noReusage[0]]:
			if reusage[1] in list:
				list[2]+=1
				alreadyIn = True
				break
		if not alreadyIn:
			alreadyIn = False
			schemes[1][noReusage[0]].append( [noReusage[1], correctness, 1] )
		alreadyIn = False
		
		if reusage[0] not in schemes[2].keys():
			schemes[2][reusage[0]] = []
		for list in schemes[2][reusage[0]]:
			if reusage[1] in list:
				list[2]+=1
				alreadyIn = True
				break
		if not alreadyIn:
			alreadyIn = False
			schemes[2][reusage[0]].append( [reusage[1], correctness, 1] )
		alreadyIn = False
		
		if pattern not in schemes[3].keys():
			schemes[3][pattern] = []
		for list in schemes[3][pattern]:
			if response in list:
				list[2]+=1
				alreadyIn = True
				break
		if not alreadyIn:
			alreadyIn = False
			schemes[3][pattern].append( [response, correctness,1] )
		alreadyIn = False
		
		if smart[0] not in schemes[4].keys():
			schemes[4][smart[0]] = []
		for list in schemes[4][smart[0]]:
			if smart[1] in list:
				list[2]+=1
				alreadyIn = True
				break
		if not alreadyIn:
			alreadyIn = False
			schemes[4][smart[0]].append( [smart[1], correctness, 1] )

			
'''	Experimental scheme that tries to show what the student was possibly 
	trying to do with the pattern'''
def smartScheme( pattern, response ):
	if len(pattern) > MAX_INPUT_SIZE or len(response) > MAX_INPUT_SIZE:
		return ['','']

	canonPattern = reuse(pattern, response)[0]
	
	letters = []
	for c in canonPattern:
		if c in constants:
			letters.append(c)
	
	#Get list of constants in pattern
	pattNumbers = []
	onNumber = False
	for i in range(0,len(pattern)):
		if pattern[i] in digits and onNumber == True:
			continue
		onNumber = False
		currConst = ''
		for j in range(i,len(pattern)):
			if pattern[j] in digits:
				currConst += pattern[j]
			else:
				break
		if currConst != '':
			'''if i != 0:
				if pattern[i-1] == '-':
					currConst = '-'+currConst'''
			pattNumbers.append(currConst)
			onNumber = True

	
	#Get list of constants in response
	respNumbers = []
	onNumber = False
	for i in range(0,len(response)):
		if response[i] in digits and onNumber == True:
			continue
		onNumber = False
		currConst = ''
		for j in range(i,len(response)):
			if response[j] in digits:
				currConst += response[j]
			else:
				break
		if currConst != '':
			respNumbers.append(currConst)
			'''if i != 0:
				if response[i-1] == '-':
					currConst = '-'+currConst'''
			onNumber = True
	
	valToOp = {}
	everyPossibleOperation( valToOp, pattNumbers, letters, 0, 1 )
	
	#add all the normal variables in
	for k in range(0,len(pattNumbers)):
		v = float(pattNumbers[k])
		if v < 0.0:
			v = v * -1.0
		if k >= len(letters):
			continue
		if v not in valToOp.keys():
			valToOp[v] = []
		if letters[k] not in valToOp[v]:
			valToOp[v].append(letters[k])
	
	respLetters = []
	for num in respNumbers:
		num = float(num)
		if num not in valToOp.keys():
			respLetters.append('[not sure]')
			continue
			
		if len(valToOp[num]) == 1:
			if len(valToOp[num][0]) == 1:
				respLetters.append(valToOp[num][0])
				continue
			
		lett = '['
		valToOp[num].sort()
		for i in range(0,len(valToOp[num])):
			set = valToOp[num][i]
			lett += set
			if i != len(valToOp[num])-1:
				lett += '|'
		lett += ']'
		respLetters.append(lett)
	
	#replace the canonized possible ops in the response equation
	newResponse = ''
	onNumber = False
	for i in range(0,len(response)):
		if response[i] in digits and onNumber == True:
			continue
		onNumber = False
		if response[i] not in digits:
			newResponse += response[i]
			continue
		currConst = ''
		for j in range(i,len(response)):
			if response[j] in digits:
				currConst += response[j]
			else:
				break
		if currConst != '':
			'''if i != 0:
				if response[i-1] == '-':
					currConst = '-'+currConst'''
			ind = respNumbers.index(currConst)
			var = respLetters[ind]
			newResponse += var
			onNumber = True
	
	'''print pattern + '\t' + canonPattern
	print response + '\t' + newResponse
	print '''
	
	return [canonPattern,newResponse]

	
'''	Used by smartScheme().  It's a recursive function that for every combination
	of constants in the pattern, the result of every operation between those 
	numbers.  This is then used to determine what the student did based on
	their response'''
def everyPossibleOperation( valToOp, pattNum, pattLett, f, s ):
	if len(pattNum) < 2 or len(pattLett) < 2:
		return []

	n1 = float(pattNum[f])
	n2 = float(pattNum[s])
	
	l1 = pattLett[f]
	l2 = pattLett[s]
	
	v1 = n1 + n2
	s1 = l1 + '+' + l2
	
	v2 = n1 - n2
	s2 = l1 + '-' + l2
	
	v3 = n2 - n1
	s3 = l2 + '-' + l1
	
	v4 = n1 * float(n2)
	s4 = l1 + '*' + l2
	
	if n2 != 0.0:
		v5 = n1 / float(n2)
		s5 = l1 + '/' + l2
	
	if n1 != 0.0:
		v6 = n2 / float(n1)
		s6 = l2 + '/' + l1
	
	if v1 not in valToOp.keys():
		valToOp[v1] = []
	if v2 not in valToOp.keys():
		valToOp[v2] = []
	if v3 not in valToOp.keys():
		valToOp[v3] = []
	if v4 not in valToOp.keys():
		valToOp[v4] = []
	if n2 != 0.0:
		if v5 not in valToOp.keys():
			valToOp[v5] = []
	if n1 != 0.0:
		if v6 not in valToOp.keys():
			valToOp[v6] = []
	
	if s1 not in valToOp[v1]:
		valToOp[v1].append(s1)
	if s2 not in valToOp[v2]:
		valToOp[v2].append(s2)
	if s3 not in valToOp[v3]:
		valToOp[v3].append(s3)
	if s4 not in valToOp[v4]:
		valToOp[v4].append(s4)
	if n2 != 0.0:
		if s5 not in valToOp[v5]:
			valToOp[v5].append(s5)
	if n1 != 0.0:
		if s6 not in valToOp[v6]:
			valToOp[v6].append(s6)
		
	#recursion
	if f == len(pattNum)-2:
		return valToOp
	elif s == len(pattNum)-1:
		return everyPossibleOperation( valToOp, pattNum, pattLett, f+1, f+2)
	else:
		return everyPossibleOperation( valToOp, pattNum, pattLett, f, s+1)
	

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

	
'''	Every constant gets its own letter.
	Ex.  3x-4=4x+2   ->   ax-b=cx+d   '''
def noReuse (pattern, response):
	if len(pattern) > MAX_INPUT_SIZE or len(response) > MAX_INPUT_SIZE:
		return ['','']
	ret = []
	constInd = 0
	canPatt = ''
	onNumber = False
	for i in range(0,len(pattern)):
		if pattern[i] in digits and onNumber == True:
			continue
		onNumber = False
		if pattern[i] not in digits:
			canPatt = canPatt + pattern[i]
			continue
		canPatt = canPatt + constants[constInd]
		constInd += 1
		onNumber = True
	canResp = ''
	for i in range(0,len(response)):
		if response[i] in digits and onNumber == True:
			continue
		onNumber = False
		if response[i] not in digits:
			canResp = canResp + response[i]
			continue
		canResp = canResp + constants[constInd]
		constInd += 1
		onNumber = True
	return [canPatt,canResp]

	
'''	Negative and positive constants are treated the same
	Ex.  3x-4=4x+2   ->   ax+b=cx+d   '''
def noNegatives(pattern, response):
	if len(pattern) > MAX_INPUT_SIZE or len(response) > MAX_INPUT_SIZE:
		return ['','']
	ret = []
	constInd = 0
	canPatt = ''
	onNumber = False
	for i in range(0,len(pattern)):
		if pattern[i] in digits and onNumber == True:
			continue
		onNumber = False
		if pattern[i] not in digits:
			canPatt = canPatt + pattern[i]
			continue
		canPatt = canPatt + constants[constInd]
		constInd += 1
		onNumber = True
	canResp = ''
	for i in range(0,len(response)):
		if response[i] in digits and onNumber == True:
			continue
		onNumber = False
		if response[i] not in digits:
			canResp = canResp + response[i]
			continue
		canResp = canResp + constants[constInd]
		constInd += 1
		onNumber = True
	if canPatt[0] == '-':
		canPatt = canPatt[1:]
	canPatt = canPatt.replace('-','+')
	if canResp[0] == '-':
		canResp = canResp[1:]
	canResp = canResp.replace('-','+')
	canResp = canResp.replace('=-','=')
	canResp = canResp.replace('+','+')
	return [canPatt,canResp]

	
''' Print out various statistics about the responses including their
	frequency as correct answers and incorrect answers'''
def responseStatistics(n):
	scheme = schemes[n]
	
	respCorrectness = {}
	respStats = {}
	for pattern in scheme.keys():
		for list in scheme[pattern]:
			resp = list[0]+'\t'+list[1]
			if resp not in respCorrectness.keys():
				respCorrectness[list[0]] = list[1]
			if resp not in respStats.keys():
				respStats[resp] = 0
			respStats[resp] += list[2]
	sortedStats = sorted(respStats.items(),key=operator.itemgetter(1),reverse=True)
	'''for resp in sortedStats:
		#print resp[0]+'\t'+str(resp[1]) + '\t'+respCorrectness[resp[0]]
		print resp[0]+'\t'+str(resp[1])'''
	responses = respCorrectness.keys()
	stats = []
	for r in responses:
		corr = r+'\tcorrect'
		incorr = r+'\tincorrect'
		numCorr = 0
		if corr in respStats.keys():
			numCorr = respStats[corr]
		numIncorr = 0
		if incorr in respStats.keys():
			numIncorr = respStats[incorr]
		total = numCorr + numIncorr
		stats.append([r,numCorr,numIncorr,total])
	stats.sort(key=operator.itemgetter(3),reverse=True)
	print 'Response\tTimes Correct\tTimes Incorrect\tTotal Appearances'
	for r in stats:
		print r[0]+'\t'+str(r[1])+'\t'+str(r[2])+'\t'+str(r[3])
	
if __name__ == "__main__": main()