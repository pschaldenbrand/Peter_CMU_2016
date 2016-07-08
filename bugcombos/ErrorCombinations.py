import math
import sys
import os
import datetime

filename = 'gill_period3.txt'
fileOutput = 'testIncentiveDelete.txt'

canonize = True
MAX_GROUPS_PER_CELL = 16
MINIMUM_PROBABILITY = -15
MAX_TOP_GROUPS = 5000000
INCENTIVE = .1				#value to add incentive to keep larger clusters. smaller value, larger cluster.

allErrors = {}			#dictionary of all error equations to number of times appeared
studentToError = {}		#dict of all students to the errors they have made

errorProbability = {}	
clusters = []

def main():
	getListOfErrors(allErrors, studentToError)
	#print allErrors
	getProbStudentHasError()
	
	#for er in errorProbability.keys():
	#	print er + '\t'+ str(errorProbability[er])
	d = datetime.datetime.now()
	print 'starting clustering:  \t'+str(d)
	createClusterTable()
	print 'finished making table:\t'+str(datetime.datetime.now())
	#printClusters()
	#print 'finished printing:    \t'+str(datetime.datetime.now())
	
'''	Reads the specified file and parses the equations.  A list of 
	every error is returned'''
def getListOfErrors(eqOfAllErrors, studentToError ):
	allLines = open(filename,'r').readlines()
	
	#eqOfAllErrors = []
	#studentToError = {}
	
	'''get the field names'''
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
	
	'''parse the equations'''
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
		#transID = tokens[transactionIndex]
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
			#printInstance(prevEq, currEqL+'='+currEqR, outcome, sid)
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
			#printInstance(prevEq, currEqL+'='+currEqR, outcome, sid)
			
			fullEq = prevEq+' => '+currEqL+'='+currEqR
			
			if canonize:
				fullEq = convertConstants(fullEq)
				
			if sid not in studentToError.keys():
				studentToError[sid] = []
			if fullEq not in eqOfAllErrors.keys():
				eqOfAllErrors[fullEq] = 0
			eqOfAllErrors[fullEq] += 1
			if fullEq not in studentToError[sid]:
				studentToError[sid].append(fullEq)
	

'''	helper fcn for getting the errors. converts spaces to pluses'''
def problemNameToEquation(pn):
	pn = pn.replace(' ','+')
	pn = pn.replace('\s+','')
	return pn

'''	Find the probability that a student has a error.  It's equal to 
	the number of students with the error divided by the total number
	of students.  Logs are used becuase of small numbers. '''
def getProbStudentHasError():
	numErrors = len(allErrors.keys())
	
	numStudents = len(studentToError.keys())
	
	'''figure out how many students made each error'''
	numStdWhoMadeError = {}
	for er in allErrors.keys():
		numStdWhoMadeError[er] = 0
		for std in studentToError.keys():
			if er in studentToError[std]:
				numStdWhoMadeError[er] += 1
	
	for er in numStdWhoMadeError.keys():
		studentWithError = -99999999.9
		if numStdWhoMadeError[er] != 0:
			studentWithError = math.log(float(numStdWhoMadeError[er]))
		logProb = float(studentWithError) - math.log(numStudents)
		#print 'log= '+str(logProb) + '\t\treal= '+str(numStdWhoMadeError[er]/float(numStudents))
		errorProbability[er] = logProb

		
def createClusterTable():
	n =  len(allErrors.keys())
	print 'n = '+str(n)
	top = TopGroups(MAX_TOP_GROUPS)
	
	for i in range(0,n):
		clusters.append([])
	#initialize the clusters 2d array 
	
	for i in range(0,n):
		if i < n-1:
			clusters.append([])
		for j in range(0,n):
			g = Groups()
			clusters[i].append(g)
	
	#initialize the first diagonal in clusters
	c = 0
	for er in allErrors.keys():
		gs = Groups()
		gs.addGroup(errorProbability[er],[er])
		clusters[c][c] = gs
		c += 1
	
	f = open(fileOutput,"w")
	f.close() #clear the file
	ers = allErrors.keys()
	for i in range(1,n):
		print str(i)+ ' out of '+str(n)
		for j in range(i-1,-1,-1):
			if j < 0:
				continue
			#print str(i) + '\t'+str(j)
			setNewGroups = Groups()
			leftCombinedGroups = []
			upCombinedGroups = []
			for t in clusters[i-1][j].groups:
				leftCombinedGroups.append(Group(t.logProb,t.memory[:]))
			for t in clusters[i][j+1].groups:
				upCombinedGroups.append(Group(t.logProb,t.memory[:]))
			#print 'making new groups'
			newGroups = Groups()
			for t in leftCombinedGroups:
				newGroups.addGroup(t.logProb, t.memory[:])
				oldMem = t.memory[:]
				newMem = clusters[i][i].groups[0].memory[:]
				newError = ""
				
				for m in newMem:		#should only loop once
					contains = False
					if m in oldMem:
						continue
					else:
						newError = m
						oldMem.append(m)
				if newError != "":
					newlp = errorProbability[m]
				else: 
					newlp = 0.0
				newGroups.addGroup(t.logProb+newlp,oldMem)
			for t in upCombinedGroups:
				newGroups.addGroup(t.logProb, t.memory[:])
				oldMem = t.memory[:]
				newMem = clusters[j][j].groups[0].memory[:]
				newError = ""

				for m in oldMem:
					contains = False
					if m in oldMem:
						continue
					else:
						newError = m
						oldMem.append(m)
				if newError != "":
					newlp = errorProbability[m]
				else: 
					newlp = 0.0
				newGroups.addGroup(t.logProb+newlp,oldMem)
			#print 'done making new groups'
			biggestIndex = -1
			biggestVal = -9999999
			#print 'lookingforbiggest'
			'''for t in range(0,len(newGroups.groups)):
				g = newGroups.groups[t]
				if g.logProb > biggestVal:
					biggestVal = g.logProb
					biggestIndex = t'''
			#print 'foundbiggest'
			newGroups.sort()
			#if len(newGroups.groups) > 1:
				#print str(newGroups.groups[0].logProb) + "\t"+str(newGroups.groups[1].logProb)
			setNewGroups.addGroup(newGroups.groups[0].logProb,newGroups.groups[0].memory[:])
			clusters[i][j] = setNewGroups.returnCopy()
			
			#print 'looking to add newgroups\t\t'+str(len(newGroups.groups))
			#newGroups.sort()
			for k in range(0,len(newGroups.groups)):
				if k > MAX_GROUPS_PER_CELL:
					break
				if k == biggestIndex:
					continue
				l = Group(newGroups.groups[k].logProb,newGroups.groups[k].memory[:])
				temp = top.add(l,i,j)
				if temp:
					setNewGroups.addGroup(l.logProb, l.memory[:])
					clusters[i][j] = setNewGroups.returnCopy()
			#print 'done adding new groups'
		
		f = open(fileOutput,"a")
		for k in range(0,i):
			gs = clusters[i][k]
			for g in gs.groups:
				f.write(str(g.logProb)+'\t')
				for m in g.memory:
					f.write(m+'\t')
				f.write('\n')
			f.flush()
		f.close()

	
class Group (object):
	def __init__(self, logProb, memory):
		self.logProb = logProb
		self.memory = memory[:]

class Groups (object):
	def __init__(self, groups):
		self.groups = groups
	def __init__(self):
		self.groups = []
	def addGroup(self, logProb, memory):
		if self.contains(logProb, memory[:]):
			#don't want duplicates
			return False
		newGroup = Group(logProb,memory[:])
		self.groups.append(newGroup)
		return True
	def contains( self, logProb, memory):
		for i in self.groups:
			lp = i.logProb
			mem = i.memory[:]
			allMatch = True
			for m in mem:
				if m not in memory:
					allMatch = False
					break
			if allMatch and lp == logProb:
				return True
		return False
	def returnCopy(self):
		newGroups = Groups()
		for g in self.groups:
			newGroups.addGroup(g.logProb, g.memory[:])
		return newGroups
	def removeGroup(self, logProb, memory):
		removeInd = -1
		c = 0
		for i in self.groups:
			lp = i.logProb
			mem = i.memory[:]
			allMatch = True
			for m in mem:
				if m not in memory:
					allMatch = False
					break
			if allMatch and lp == logProb:
				removeInd = c
			c+=1
		for i in range(0,len(self.groups)-1):
			if i <= c:
				continue
			self.groups[i] = self.groups[i+1]
	def sort(self):
		self.mergeSort(self.groups)
		
	def mergeSort(self, alist):
		if len(alist)>1:
			mid = len(alist)//2
			lefthalf = alist[:mid]
			righthalf = alist[mid:]

			self.mergeSort(lefthalf)
			self.mergeSort(righthalf)

			i=0
			j=0
			k=0
			while i < len(lefthalf) and j < len(righthalf):
				if (lefthalf[i].logProb/(len(lefthalf[i].memory)*INCENTIVE)) > (righthalf[j].logProb/(len(righthalf[j].memory)*INCENTIVE)):
					alist[k]=lefthalf[i]
					i=i+1
				else:
					alist[k]=righthalf[j]
					j=j+1
				k=k+1

			while i < len(lefthalf):
				alist[k]=lefthalf[i]
				i=i+1
				k=k+1

			while j < len(righthalf):
				alist[k]=righthalf[j]
				j=j+1
				k=k+1
	
class TopGroups (object):
	def __init__(self, max):
		self.max = max
		self.allGroups = []
	def add(self, g, i, j):
		#return True
		if self.shouldBeIn(g) == False:
			#print 'shouldnt be in'
			return False
		if len(self.allGroups) < self.max:
			g.i = i
			g.j = j
			self.allGroups.append(g)
			#print 'got in because len is less than max'
			return True
		#print 'ran out of top spots making more'
		indOfWorst = -1
		worstProb = 0
		for x in range(0,len(self.allGroups)):
			topGroup = self.allGroups[x]
			if topGroup.logProb < worstProb:
				indOfWorst = x
				worstProb = topGroup.logProb
		worstTopGroup = self.allGroups[indOfWorst]
		clusters[worstTopGroup.i][worstTopGroup.j].removeGroup( worstTopGroup.logProb, worstTopGroup.memory[:])
		g.i = i
		g.j = j 
		self.allGroups[indOfWorst] = g
		return True
	
	def shouldBeIn(self, g):
		if g.logProb < MINIMUM_PROBABILITY:		#pruning
			return False
		if self.alreadyContains(g):
			#print 'alreadycontains'
			return False
		lp = g.logProb
		if len(self.allGroups) < self.max:
			return True
		for i in self.allGroups:
			topLP = i.logProb
			if lp >= topLP:
				return True
		return False
	def alreadyContains(self, g):
		lp = g.logProb 
		mem = g.memory[:]
		for i in self.allGroups:
			currlp = i.logProb 
			currmem = i.memory[:]
			allMatch = True
			if len(mem) != len(currmem):
				continue
			for m in mem:
				if m not in currmem:
					allMatch = False
					break
			if allMatch and lp == currlp:
				return True
		return False
			

def printClusters():
	return
	f = open("clusters.txt","w")
	f.close() #clear the file
	n = len(allErrors)
	for i in range(0,n):
		f = open("clusters.txt","a")
		for j in range(0,i):
			gs = clusters[i][j]
			for g in gs.groups:
				f.write(str(g.logProb)+'\t')
				for m in g.memory:
					f.write(m+'\t')
				f.write('\n')
			f.flush()
		f.close()
			
		
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