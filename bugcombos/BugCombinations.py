#Peter Schaldenbrand
#Calculate joint probabilities of combinations of bugs

import math
import sys

bugs  = []			#list of bug names
table = [[]]		#dynamic programming table
students = []		#list of the student IDs
combinations = []	#only used if brute force
studentsBugs = [[]]	#mapping between each student and the number of times 
						#they performed a bug
memory = [[]]		#the mapping of table and the previous rules performed
bugProb = []		#probablilty of each bug being performed by a student

groupTable = [[]]

def main():
	getAllStudentErrors()
	#numBug = getUniqueNumBugs()
	#numStd = getUniqueNumStudents()
	#makeTable(numStd, numBug)
	
	#getProbOfEachBug(numBug)
	
	#table = getGroups()
	
	#setTable()
	##printWholeGroupTable()
	#printWithChainProb()

def getAllStudentErrorsNoPEQ():
	filename = 'gill3bugs.txt'
	logs = open(filename,'r')
	firstLine = logs.readline().split("\t")
	inputIndex = 0
	outcomeIndex = 0
	selectionIndex = 0
	sidIndex = 0
	problemNameIndex = 0
	eqIndex = 0
	feedbackIndex = 0;
	transactionIndex = 0;
	c = 0
	for tok in firstLine :
		if tok == "Input" and inputIndex == 0:
			inputIndex = c
		if tok == "Outcome":
			outcomeIndex = c
		if tok == "Selection":
			selectionIndex = c
		if tok == "Anon Student Id":
			sidIndex = c
		if tok == "Problem Name":
			problemNameIndex = c
		if tok == "CF (preEqSys)":
			eqIndex = c
		if tok == "Feedback Text":
			feedbackIndex = c
		if tok == "CF (orig_trans_id)":
			transactionIndex = c
		c+=1
	
	problemDict = {}
	for line in open("pnamemapping.txt",'r').readlines():
		splitLine = line.split('\t')
		problemDict[splitLine[0]] = splitLine[1]
	
	logs.close()
	prevPName = ""
	prevEquationL = ""
	prevEquationR = ''
	currEquationL = ''
	currEquationR = ''
	leftCorrect = False
	rightCorrect = False
	
	errorDict = {}
	studentDict = {}
	bugDict = {}
	strToParsed = {}
	
	noFirstLine = True
	for line in open(filename,'r').readlines():
		if noFirstLine:
			noFirstLine = False
			continue
		tokens = line.split('\t')
		problemName = tokens[problemNameIndex]
		probEQ = tokens[eqIndex]
		sid = tokens[sidIndex]
		input = tokens[inputIndex]
		outcome = tokens[outcomeIndex].lower()
		selection = tokens[selectionIndex].lower()
		bug = tokens[feedbackIndex].lower()
		transID = tokens[transactionIndex]
		
		if not studentDict.has_key(sid):
			studentDict[sid] = {}
	
		if outcome != 'correct' and outcome != 'incorrect':
			#print "not correct or incorrect"
			continue
		if leftCorrect and rightCorrect:
			#print "you have completed it"
			continue
			
		if prevPName == '' or prevPName != problemName:
			#print 'newProb'
			s = problemDict[problemName].split('=')
			if len(s)<2 :
				continue
			prevEquationL = s[0]
			prevEquationR = s[1]
			currEquationL = ''
			currEquationR = ''
			prevPName = problemName
		
		
		if outcome == 'correct':
			if selection[:len(selection)-1] == 'solveleft':
				leftCorrect = True
				currEquationL = input
			if selection[:len(selection)-1] == 'solveright':
				rightCorrect = True
				currEquationR = input
			if leftCorrect and rightCorrect:
				leftCorrect = False
				rightCorrect = False
				prevEquationL = currEquationL
				prevEquationR= currEquationR
				currEquationL = ''
				currEquationR = ''
			continue
		
		if outcome == 'incorrect':
			##DO THE STUFF WITH PUTTING IT IN THE EQUATION AND STUFF
			if selection[:len(selection)-1] == 'solveleft':
				currEquationL = input
				if not rightCorrect:
					currEquationR = '$'
			if selection[:len(selection)-1] == 'solveright':
				currEquationR = input
				if not leftCorrect:
					currEquationL = '$'
			if selection[:len(selection)-1] != 'solveleft' and selection[:len(selection)-1] != 'solveright':
				continue
			## call the method/class to put in an object
			s =  prevEquationL + " = " + prevEquationR+" => "+currEquationL + " = " + currEquationR
			#print 's=\t'+s
			pEq = ParsedEq(s)
			pEq.bug = bug
			pEq.transactionID = transID
			#print pEq.originalEquation
			if len(bug) > 20:
				if pEq.str in bugDict.keys():
					if bug not in bugDict[pEq.str]:
						bugDict[pEq.str].append(bug)
						strToParsed[pEq.str] = str(pEq.originalEquation)
				else:
					bugDict[pEq.str] = [bug]
					strToParsed[pEq.str] = str(pEq.originalEquation)
		
			
			s = pEq.str
			#print 'str=\t'+s+'\n'
			added = False
			for d in errorDict:
				if d.equals(pEq):
					#print d.str
					#print pEq.str
					#print
					errorDict[d] = errorDict[d]+1
					added = True
			if not added:
				errorDict[pEq] = 1
			added = False
			for d in studentDict[sid]:
				if d.equals(pEq):
					studentDict[sid][d] = studentDict[sid][d] + 1 
					added = True
			if not added:
				studentDict[sid][pEq] = 1
				
			print pEq.transactionID +'\t'+ pEq.bug+'\t' + pEq.str+'\t' + pEq.originalEquation
			
#Print each incorrect step with its bug (if it has one) and canonized equation
def getAllStudentErrors():
	filename = 'gill3bugs.txt'
	logs = open(filename,'r')
	firstLine = logs.readline().split("\t")
	inputIndex = 0
	outcomeIndex = 0
	selectionIndex = 0
	sidIndex = 0
	problemNameIndex = 0
	eqIndex = 0
	feedbackIndex = 0;
	transactionIndex = 0;
	c = 0
	for tok in firstLine :
		if tok == "Input" and inputIndex == 0:
			inputIndex = c
		if tok == "Outcome":
			outcomeIndex = c
		if tok == "Selection":
			selectionIndex = c
		if tok == "Anon Student Id":
			sidIndex = c
		if tok == "Problem Name":
			problemNameIndex = c
		if tok == "CF (preEqSys)":
			eqIndex = c
		if tok == "Feedback Text":
			feedbackIndex = c
		if tok == "CF (orig_trans_id)":
			transactionIndex = c
		c+=1
	
	problemDict = {}
	for line in open("pnamemapping.txt",'r').readlines():
		splitLine = line.split('\t')
		problemDict[splitLine[0]] = splitLine[1]
	
	logs.close()
	prevPName = ""
	prevEquationL = ""
	prevEquationR = ''
	currEquationL = ''
	currEquationR = ''
	leftCorrect = False
	rightCorrect = False
	
	errorDict = {}
	studentDict = {}
	bugDict = {}
	strToParsed = {}
	
	noFirstLine = True
	for line in open(filename,'r').readlines():
		if noFirstLine:
			noFirstLine = False
			continue
		tokens = line.split('\t')
		problemName = tokens[problemNameIndex]
		probEQ = tokens[eqIndex]
		sid = tokens[sidIndex]
		input = tokens[inputIndex]
		outcome = tokens[outcomeIndex].lower()
		selection = tokens[selectionIndex].lower()
		bug = tokens[feedbackIndex].lower()
		transID = tokens[transactionIndex]
		
		if not studentDict.has_key(sid):
			studentDict[sid] = {}
	
		if outcome != 'correct' and outcome != 'incorrect':
			#print "not correct or incorrect"
			continue
		if leftCorrect and rightCorrect:
			#print "you have completed it"
			continue
			
		if prevPName == '' or prevPName != problemName:
			#print 'newProb'
			s = problemDict[problemName].split('=')
			if len(s)<2 :
				continue
			prevEquationL = s[0]
			prevEquationR = s[1]
			currEquationL = ''
			currEquationR = ''
			prevPName = problemName
		
		
		if outcome == 'correct':
			if selection[:len(selection)-1] == 'solveleft':
				leftCorrect = True
				currEquationL = input
			if selection[:len(selection)-1] == 'solveright':
				rightCorrect = True
				currEquationR = input
			if leftCorrect and rightCorrect:
				leftCorrect = False
				rightCorrect = False
				prevEquationL = currEquationL
				prevEquationR= currEquationR
				currEquationL = ''
				currEquationR = ''
			continue
		
		if outcome == 'incorrect':
			##DO THE STUFF WITH PUTTING IT IN THE EQUATION AND STUFF
			if selection[:len(selection)-1] == 'solveleft':
				currEquationL = input
				if not rightCorrect:
					currEquationR = '$'
			if selection[:len(selection)-1] == 'solveright':
				currEquationR = input
				if not leftCorrect:
					currEquationL = '$'
			if selection[:len(selection)-1] != 'solveleft' and selection[:len(selection)-1] != 'solveright':
				continue
			## call the method/class to put in an object
			s =  prevEquationL + " = " + prevEquationR+" => "+currEquationL + " = " + currEquationR
			#print 's=\t'+s
			pEq = ParsedEq(s)
			pEq.bug = bug
			pEq.transactionID = transID
			#print pEq.originalEquation
			if len(bug) > 20:
				if pEq.str in bugDict.keys():
					if bug not in bugDict[pEq.str]:
						bugDict[pEq.str].append(bug)
						strToParsed[pEq.str] = str(pEq.originalEquation)
				else:
					bugDict[pEq.str] = [bug]
					strToParsed[pEq.str] = str(pEq.originalEquation)
		
			
			s = pEq.str
			#print 'str=\t'+s+'\n'
			added = False
			for d in errorDict:
				if d.equals(pEq):
					#print d.str
					#print pEq.str
					#print
					errorDict[d] = errorDict[d]+1
					added = True
			if not added:
				errorDict[pEq] = 1
			added = False
			for d in studentDict[sid]:
				if d.equals(pEq):
					studentDict[sid][d] = studentDict[sid][d] + 1 
					added = True
			if not added:
				studentDict[sid][pEq] = 1
				
			print pEq.transactionID +'\t'+ pEq.bug+'\t' + pEq.str+'\t' + pEq.originalEquation
			
	#print errorDict
	'''allErrors = []
	for key in errorDict.keys():
		#print str(errorDict[key])+"\t"+key.str
		allErrors.append(key)
	print len(errorDict)
	for student in studentDict.keys():
		sys.stdout.write(student+'\t')
		for er in allErrors:
			notzero = False
			for d in studentDict[student].keys():
				if d.equals(er):
					sys.stdout.write(str(studentDict[student][d])+'\t')
					notzero = True
					break
					#print student + "\t" +str(studentDict[student][d])+'\t'+ d.str
			if not notzero:
				sys.stdout.write('0'+'\t')
		sys.stdout.write('\n')
	studentsBugs = []'''
	
	
	
	'''for key in bugDict.keys():
		#sys.stdout.write(key+"\t")
		ar = key.split(' => ')
		sys.stdout.write(ar[0]+'\t'+ar[1]+'\t')
		sys.stdout.write(strToParsed[str(key)]+'\t')
		for b in bugDict[key]:
			sys.stdout.write(b + '\t')
		sys.stdout.write('\n')'''

#Class that holds a canonized equation
class ParsedEq (object):
	prevLeftTerms = []
	prevRightTerms = []
	currLeftTerms = []
	currRightTerms = []
	str = ''
	originalEquation = ''
	transactionID = ''
	bug = ''
	
	def __init__(self, s):
		#print 's= ' + s
		self.originalEquation = s
		s1 = s.split(" => ")
		prevS = s1[0].split('=')
		currS = s1[1].split('=')
		#print currS
		prevS.append(currS[0])
		prevS.append(currS[1])
		ar = []
		for str in prevS:
			ar.append(self.preprocess(str))
		#print
		#for str in ar:
		#	print ar
		#print
		self.setTerms(ar)
		
		for i in self.prevLeftTerms:
			self.str = self.str+i+" "
		self.str = self.str + " = "
		for i in self.prevRightTerms:
			self.str = self.str+i+" "
		self.str = self.str + ' => '
		for i in self.currLeftTerms:
			self.str = self.str+i+" "
		self.str = self.str + ' = '
		for i in self.currRightTerms:
			self.str = self.str+i+" "
		#print "str =...."+self.str
	#takes an array of the sides of the equations then turns the constants into
	#c0..cN and stores it
	def setTerms(self, s):
		#print 'setterms= '
		#print s
		#print
		num = 0
		constantMap = {}
		for i in range(0,len(s)):
			addToTerms = []
			eq = s[i]
			term = ''
			for c in eq:
				if c == ')':
					continue
				if c == '(':
					if term != '':
						addToTerms.append(term)
					term = ''
					addToTerms.append('*')
					continue
				if c in ['+','-','x','(','*']:
					if term != '':
						addToTerms.append(term)
					addToTerms.append(c)
					term = ''
					continue
				else:
					term = term + c
			if term != '':
				addToTerms.append(term)
			
			index = 0
			
			for t in addToTerms:
				constant = False
				rep = ''
				#for char in t:
				for j in range(0,len(t)):
					char = t[j]
					if char == 'n':
						rep = rep+'n'
					if char in ['1','2','3','4','5','6','7','8','9','0']:
						const = char
						if j != len(t)-1:
							if t[j+1] in ['1','2','3','4','5','6','7','8','9','0']:
								const = const +t[j+1]
								j = j + 1
						#print 'const = '+const
						constantValue = 'c'+str(num)
						if const in constantMap.keys():
							constantValue = constantMap[const]
						else:
							constantMap[const] = constantValue
						#rep = rep + 'c' + str(num)
						rep = rep + constantValue
						num+=1
						addToTerms[index] = rep
						constant = True
						break
				index += 1
					
			#print addToTerms
			if i == 0:
				self.prevLeftTerms = addToTerms[:]
			if i == 1:
				self.prevRightTerms = addToTerms[:]
			if i == 2:
				self.currLeftTerms = addToTerms[:]
			if i == 3:
				self.currRightTerms = addToTerms[:]
			##print
	
	#takes a side of an equation then parses it and does some processing
	#turns negative symbols into n so it can differentiate them from minus symbols
	def preprocess(self, side):
		ret = ''
		side = side.replace(" ","")
		prevChar = ''
		char = ''
		for c in range(0,len(side)):
			prevChar = char
			char = side[c]
			if char == 'x':
				if prevChar in ['1','2','3','4','5','6','7','8','9','0']:
					ret = ret + '*'
			if char == '-':
				if c != 0:
					if side[c-1] not in ['1','2','3','4','5','6','7','8','9','0','x',')']:
						ret = ret + 'n'
						continue
				if c == 0:
					ret = ret + 'n'
					continue
				ret = ret + char
			else:
				ret = ret + char
		return ret
	def equals(self, other):
		if len(self.prevLeftTerms) != len(other.prevLeftTerms) and len(self.prevLeftTerms) != len(other.prevRightTerms):
			return False
		if len(self.prevRightTerms) != len(other.prevRightTerms) and len(self.prevRightTerms) != len(other.prevLeftTerms):
			return False
		if len(self.currLeftTerms) != len(other.currLeftTerms) and len(self.currLeftTerms) != len(other.currRightTerms):
			return False
		if len(self.currRightTerms) != len(other.currRightTerms) and len(self.currRightTerms) != len(other.currLeftTerms):
			return False
			
		'''allEqual = True
		for i in self.prevLeftTerms:
			if i not in other.prevLeftTerms:
				allEqual = False
		for i in self.prevRightTerms:
			if i not in other.prevRightTerms:
				allEqual = False
		for i in self.currLeftTerms:
			if i not in other.currLeftTerms:
				allEqual = False
		for i in self.currRightTerms:
			if i not in other.currRightTerms:
				allEqual = False
		if allEqual:
			return True
			
		allEqual = True
		for i in self.prevLeftTerms:
			if i not in other.prevRightTerms:
				allEqual = False
		for i in self.prevRightTerms:
			if i not in other.prevLeftTerms:
				allEqual = False
		for i in self.currLeftTerms:
			if i not in other.currRightTerms:
				allEqual = False
		for i in self.currRightTerms:
			if i not in other.currLeftTerms:
				allEqual = False
		if allEqual:
			return True
		return False'''
				
		
		'''for i in range(0,len(self.prevLeftTerms)):
			if self.prevLeftTerms[i] != other.prevLeftTerms[i]:
				return False
		for i in range(0,len(self.prevRightTerms)):
			if self.prevRightTerms[i] != other.prevRightTerms[i]:
				return False
		for i in range(0,len(self.currLeftTerms)):
			if self.currLeftTerms[i] != other.currLeftTerms[i]:
				return False
		for i in range(0,len(self.currRightTerms)):
			if self.currRightTerms[i] != other.currRightTerms[i]:
				return False'''
		return self.str == other.str	
					
	
def printWithChainProb():
	n = len(bugProb)
	for i in range(0,n):
		for j in range(0,i):
			gs = groupTable[i][j]
			for g in gs.groups:
				chainProb = chainRule(g.memory)
				sys.stdout.write(str(chainProb)+'\t')
				for m in g.memory:
					sys.stdout.write(str(bugs.index(m))+'\t')
				sys.stdout.write('\n')
			sys.stdout.flush()
			
def printWholeGroupTable():
	for i in range(0,len(bugs)):
		sys.stdout.write(str(i)+'\t'+bugs[i]+'\n')
	n = len(bugProb)
	"""for i in range(0,len(bugs)):
		for k in groupTable[i][i].groups[0].memory:
			print k
	print groupTable[0][0].groups[0].memory[0]
	print n"""
	for i in range(0,n):
		for j in range(0,i):
			gs = groupTable[i][j]
			for g in gs.groups:
				sys.stdout.write(str(g.logProb)+'\t')
				for m in g.memory:
					sys.stdout.write(str(bugs.index(m))+'\t')
				sys.stdout.write('\n')
			sys.stdout.flush()
	
def setTable():
	n = len(bugProb) # number of bugs
	
	top = TopGroups(200000)
	
	#initialize
	for i in range(0,n):
		if i < n-1:
			groupTable.append([])
		for j in range(0,n):
			g = Groups()
			groupTable[i].append(g)
	for i in range(0,n):
		gs = Groups()
		gs.addGroup(bugProb[i],[bugs[i]])
		groupTable[i][i] = gs
	
	for i in range(1,n):
		for j in range(i-1,-1,-1):
			setNewGroups = Groups()
			leftCombinedGroups = []
			upCombinedGroups = []
			for t in groupTable[i-1][j].groups:
				leftCombinedGroups.append(Group(t.logProb,t.memory[:]))
			for t in groupTable[i][j+1].groups:
				upCombinedGroups.append(Group(t.logProb,t.memory[:]))
			
			allNewGroups = []
			newGroups = Groups()
			for t in leftCombinedGroups:
				newGroups.addGroup(t.logProb, t.memory[:])
				oldMem = t.memory[:]
				newMem = groupTable[i][i].groups[0].memory[:]
				newRule = ""
				
				for m in newMem:
					contains = False
					if m in oldMem:
						continue
					else:
						newRule = m
						oldMem.append(m)
				newlp = bugProb[bugs.index(newRule)]
				newGroups.addGroup(t.logProb+newlp,oldMem)
			for t in upCombinedGroups:
				newGroups.addGroup(t.logProb, t.memory[:])
				oldMem = t.memory[:]
				newMem = groupTable[j][j].groups[0].memory[:]
				newRule = ""

				for m in oldMem:
					contains = False
					if m in oldMem:
						continue
					else:
						newRule = m
						oldMem.append(m)
				if newRule != '':
					newlp = bugProb[bugs.index(newRule)]
				else:
					newlp = 0.0
				newGroups.addGroup(t.logProb+newlp,oldMem)
			
			biggestIndex = -1
			biggestVal = -9999999
			for t in range(0,len(newGroups.groups)):
				g = newGroups.groups[t]
				if g.logProb > biggestVal:
					biggestVal = g.logProb
					biggestIndex = t
					
			setNewGroups.addGroup(newGroups.groups[biggestIndex].logProb,newGroups.groups[biggestIndex].memory)
			groupTable[i][j] = setNewGroups
			###################################################3"""
			"""oldMem = combinedGroups[biggestIndex].memory[:]
			
			#oldMem.append(groupTable[i][i].groups[0].memory[0])
			p = False
			if bugs.index(oldMem[0]) == 3:
				#print 'yo'
				p = True
			
			newlp = 0.0
			if combinedGroups[biggestIndex].dir == 'left':
				newlp = groupTable[i][i].groups[0].logProb
			else:
				newlp = groupTable[j][j].groups[0].logProb
				
			
			newMem = groupTable[i][i].groups[0].memory[:]
			for o in range(0, len(groupTable[j][j].groups[0].memory)):
				newMem.append(groupTable[j][j].groups[0].memory[o])
			#print 'b4'
			if p:
				print newMem
				print oldMem
				print 'ya'
			for m in newMem:
				contains = False
				for n in oldMem:
					if n == m:
						contains = True
				if not contains:
					if p:
						print m
					ruleAdded = m
					oldMem.append(m)
					break
			#print 'after'
			newlp = bugProb[bugs.index(m)]
			#expandedGroup = Group(biggestVal + groupTable[i][i].groups[0].logProb, newMem)
			#expandedGroup = Group(biggestVal + newlp, newMem)
			expandedGroup = Group(biggestVal + newlp, newMem)
			
			newGroups.addGroup(combinedGroups[biggestIndex].logProb,combinedGroups[biggestIndex].memory)
			combinedGroups.append(expandedGroup)
			groupTable[i][j] = newGroups"""
			###############################################################33
			for k in range(0,len(newGroups.groups)):
				if k == biggestIndex:
					continue
				l = Group(newGroups.groups[k].logProb,newGroups.groups[k].memory[:])
				temp = top.add(l,i,j)
				if temp:
					setNewGroups.addGroup(l.logProb, l.memory)
					groupTable[i][j] = setNewGroups
				
			
class TopGroups (object):
	def __init__(self, max):
		self.max = max
		self.allGroups = []
	def add(self, g, i, j):
		if self.shouldBeIn(g) == False:
			#print 'shouldnt be in'
			return False
		if len(self.allGroups) < self.max:
			g.i = i
			g.j = j
			self.allGroups.append(g)
			#print 'got in because len is less than max'
			return True
		print 'ran out of top spots making more'
		indOfWorst = -1
		worstProb = 0
		for x in range(0,len(self.allGroups)):
			topGroup = self.allGroups[x]
			if topGroup.logProb < worstProb:
				indOfWorst = x
				worstProb = topGroup.logProb
		worstTopGroup = self.allGroups[indOfWorst]
		groupTable[worstTopGroup.i][worstTopGroup.j].removeGroup( worstTopGroup.logProb, worstTopGroup.memory)
		g.i = i
		g.j = j 
		self.allGroups[indOfWorst] = g
		return True
	def shouldBeIn(self, g):
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
		mem = g.memory
		for i in self.allGroups:
			currlp = i.logProb 
			currmem = i.memory
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
			

def storeGroups():
	g = Groups()
	n = len(bugProb)
	for i in range(0,n):
		for j in range(0,i):
			logProb = table[i][j]
			mem = memory[i][j].split(' => ')
			g.addGroup(logProb, mem)
	for val in g.groups:
		sys.stdout.write(str(val.logProb)+'\t')
		for m in val.memory:
			#sys.stdout.write(m+'\t')
			sys.stdout.write(str(bugs.index(m))+'\t')
		sys.stdout.write('\n')
	sys.stdout.flush()
	
#print the entire table
def printAll ():
	for i in range(0,len(bugs)):
		sys.stdout.write(str(i)+'\t'+bugs[i]+'\n')
	n = len(bugProb)
	print n
	for i in range(0,n):
		for j in range(0,i):
			if( table[i][j] != 0):
				val = str(table[i][j])
				sys.stdout.write(val+'\t')
				s = memory [i][j]
				s = s.split(" => ")
				for bug in s:
					ind = bugs.index(bug)
					ind = str(ind)
					sys.stdout.write(ind + '\t')
					sys.stdout.flush()
				sys.stdout.write('\n')
				sys.stdout.flush()
				
#prints the entry in the table with the highest probability
def printBest ():
	n = len(bugProb)
	max = -9999999.0
	maxI = 0
	maxJ = 0
	for i in range(0,n):
		for j in range(0,i-5):
			#print table[i][j]
			if (table[i][j] > max):
				if(table[i][j] !=0):
					maxI = i
					maxJ = j
					max = table[i][j]
	print table[maxI][maxJ]
	#print memory[maxI][maxJ]
	s = memory [maxI][maxJ]
	s = s.split(" => ")
	for bug in s:
		ind = bugs.index(bug)
		ind = str(ind)
		sys.stdout.write(ind + ' ')
		sys.stdout.flush()
	sys.stdout.write('\n')
	sys.stdout.flush()
	
#creates the table
def getGroups():
	n = len(bugProb)

	#initialize table and memory
	for i in range(0,n):
		memory[i][i] = bugs[i]
		table[i][i] = bugProb[i]

	for i in range(1,n):
		for j in range(i-1,-1,-1):
			newVal = table[i-1][j] + table[i][i]
			memSize = len(memory[i-1][j].split(' => '))
			bigEnough = memSize > 2
			oldVal = 0
			oldMem = ''
			if table[i-1][j] > table[i][j+1]:
				oldVal = table[i-1][j]
				oldMem = memory[i-1][j]
			else:
				oldVal = table[i][j+1]
				oldMem = memory[i][j+1]
				
			if newVal*.3 > oldVal: 
				table[i][j] = newVal
				memory[i][j] = memory[i-1][j] + ' => ' + memory[i][i]
			else:
				table[i][j] = oldVal
				memory[i][j] = oldMem

	return table

#gets probability that a bug is performed by a student. put in bugProb
def getProbOfEachBug(numBugs):
	#initialize the size of the table and memory lists
	studentsWithBug = []
	for i in range(0,numBugs):
		if i != numBugs-1:
			table.append([])
			memory.append([])
		for j in range(0,numBugs):
			table[i].append(0.0)
			memory[i].append('')
	
	for i in range(0,len(studentsBugs[0])):
		studentsWithBug.append(0)
	for i in range(0,len(studentsBugs[0])):
		for j in range(0,len(studentsBugs)):
			if studentsBugs[j][i] > 0.0:
				studentsWithBug[i]+=1
				
	numStudents = len(studentsBugs)

	for i in range(0,len(studentsWithBug)):
		if studentsWithBug[i] != 0:
			stud = math.log(float(studentsWithBug[i]))
		else:
			stud = -999999999.9
		logProb = stud - math.log(numStudents)
		logProb = float(logProb)
		bugProb.append(logProb)	
	
def getCombos( input ):
	if (len(combinations) % 1000) == 0:
		print len(combinations)
	if len(input) == 1:
		if input not in combinations:
			combinations.append(input)
		return
	for i in range(0, len(input)):
		newComb = input[0:i]+input[i+1:len(input)]
		if( newComb not in combinations ):
			combinations.append(newComb)
			getCombos(newComb)

#poorly named. this creates the studentsBugs table which has student id's
#as one dimension and the number of times they performed a bug as the second
def makeTable( numStd, numBugs ):
	logs = open("gill3bugs.txt",'r')
	firstLine = logs.readline().split("\t")
	feedbackIndex = 0
	for tok in firstLine :
		if tok == "Feedback Text" :
			break
		feedbackIndex+=1
	logs.close()
	
	logs = open("gill3bugs.txt",'r')
	firstLine = logs.readline().split("\t")
	studentIndex = 0
	for tok in firstLine :
		if tok == "Anon Student Id":
			break
		studentIndex+=1
	logs.close()
	
	for i in range(0,numStd):
		if i < numStd -1:
			studentsBugs.append([])
		for j in range(0,numBugs):
			studentsBugs[i].append(0.0)
	
	
	c = 0

	for line in open('gill3bugs.txt','r').readlines():
		c+=1
		if c==1: continue
		
		sid = line.split('\t')[studentIndex]
		if sid not in students:
			students.append(sid)
		sidInd = students.index( sid )
		
		feedback = line.split('\t')[feedbackIndex]
		tokens = feedback.split(" ")
		if( tokens[0] != "Bug!!!" ):
			continue
		
		bugName = tokens[2]
		if bugName not in bugs:
			bugs.append(tokens[2])
		
		bugInd = bugs.index( bugName )
		studentsBugs[sidInd][bugInd] += 1
			
def getUniqueNumBugs():
	logs = open("gill3bugs.txt",'r')
	firstLine = logs.readline().split("\t")
	feedbackIndex = 0
	for tok in firstLine :
		if tok == "Feedback Text" :
			break
		feedbackIndex+=1
	logs.close()
	
	count = 0
	firstL = True
	bugss = []
	for line in open('gill3bugs.txt','r').readlines():
		if( firstL ):
			firstL = False
			continue
		feedback = line.split('\t')[feedbackIndex]
		tokens = feedback.split(" ")
		if( tokens[0] != "Bug!!!" ):
			continue
		
		bugName = tokens[2]
		if bugName not in bugss:
			bugss.append(tokens[2])
			count += 1
	return count

def getUniqueNumStudents():
	logs = open("gill3bugs.txt",'r')
	firstLine = logs.readline().split("\t")
	studentIndex = 0
	for tok in firstLine :
		if tok == "Anon Student Id":
			break
		studentIndex+=1
	logs.close()
		
	count = 0
	firstL = True
	bugss = []
	for line in open('gill3bugs.txt','r').readlines():
		if( firstL ):
			firstL = False
			continue
		sid = line.split('\t')[studentIndex]
		if sid not in bugss:
			bugss.append(sid)
			count += 1
	return count

def chainRule( listOfBugs ):
	n = len(listOfBugs)
	if n == 1:
		return bugProb[bugs.index(listOfBugs[0])]
	cond = listOfBugs[0]
	given = []
	for i in range(1,n):
		given.append(listOfBugs[i])
	condInd = bugs.index(cond)
	conditionalProb = 0.0
	numWithGivens = 0
	numWithGivensAndCond = 0
	for i in range(0,len(studentsBugs)):
		hasAllGivens = True
		for j in range(0,len(given)):
			givenInd = bugs.index(given[j])
			if studentsBugs[i][givenInd] <= 0:
				hasAllGivens = False
		if hasAllGivens:
			numWithGivens += 1
		if studentsBugs[i][condInd] > 0 and hasAllGivens:
			numWithGivensAndCond += 1
	#print numWithGivensAndCond
	#print numWithGivens
	#print
	#conditionalProb = float(numWithGivensAndCond) / float(numWithGivens)
	logConditionalProb = -999999.9
	if numWithGivens > 0 and numWithGivensAndCond > 0:
		logConditionalProb = math.log(float(numWithGivensAndCond))-math.log(float(numWithGivens))

	#print logConditionalProb
	#print conditionalProb
	return logConditionalProb + chainRule(given)
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

class Group (object):
	def __init__(self, logProb, memory):
		self.logProb = logProb
		self.memory = memory
class Groups (object):
	def __init__(self, groups):
		self.groups = groups
	def __init__(self):
		self.groups = []
	def addGroup(self, logProb, memory):
		if self.contains(logProb, memory):
			#don't want duplicates
			return False
		newGroup = Group(logProb,memory)
		self.groups.append(newGroup)
		return True
	def contains( self, logProb, memory):
		for i in self.groups:
			lp = i.logProb
			mem = i.memory
			allMatch = True
			for m in mem:
				if m not in memory:
					allMatch = False
					break
			if allMatch and lp == logProb:
				return True
		return False
	def removeGroup(self, logProb, memory):
		removeInd = -1
		c = 0
		for i in self.groups:
			lp = i.logProb
			mem = i.memory
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
		#print 'deleted'
if __name__ == "__main__": main()