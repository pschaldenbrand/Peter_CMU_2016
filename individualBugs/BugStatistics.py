#Peter Schaldenbrand
#Compare a file with one bug to a log with all bugs

import math
import sys
import os

allTransToBugs = {}
allBugsToTrans = {}
transToLog = {}
bugsInTrans = {}

def main():
	initAllBugs()
	#print allTransToBugs
	#print allBugsToTrans
	
	for fn in os.listdir('./individualBugs/datasets'):
		compareIndividualBugsToAllBugs('individualBugs/datasets/'+fn)
	
	transToEq = {}
	for line in open('individualBugs/TransIDtoEquation.txt','r'):
		tokens = line.split('\t')
		if len(tokens) < 2:
			continue
		transToEq[tokens[0]] = tokens[1]
		
	
	for t in transToLog.keys():
		if len(bugsInTrans[t]) < 2:
			continue
	
		#print transToLog[t].replace("\n","")
		if t in transToEq.keys():
			print transToEq[t].replace('\n','')
		print 'bugs fired in this transaction:'
		for bug in bugsInTrans[t]:
			print '\t'+bug
		print
	
'''	
	filename is the name to a log file that was run with just one bug rule.
	the occorences of the bug rule in this file are compared to the file when
	all the bug rules were run
'''
def compareIndividualBugsToAllBugs(filename):
	logs = open(filename,'r')
	firstLine = logs.readline().split("\t")

	#the transactions of the bugs of this file
	individualTransWithBug = []
	
	feedbackIndex = 0
	transactionIndex = 0
	
	thisBug = ''	#the particular bug that was tested in this replay log
	
	c = 0
	for tok in firstLine :
		if tok == "Feedback Text":
			feedbackIndex = c
		if tok == "CF (orig_trans_id)":
			transactionIndex = c
		c+=1
	
	noFirstLine = True
	for line in open(filename,'r').readlines():
		if noFirstLine:
			noFirstLine = False
			continue
		tokens = line.split('\t')
		bug = tokens[feedbackIndex]
		trans = tokens[transactionIndex]
		if len(bug) < 15:
			continue
		if bug[0:13] != 'Bug!!! Name: ':
			continue
		thisBug = bug[13:len(bug)]
		
		if trans not in transToLog.keys():
			transToLog[trans] = line
		if trans not in bugsInTrans.keys():
			bugsInTrans[trans] = []
		bugsInTrans[trans].append(thisBug)
		
		individualTransWithBug.append(trans)
	
	if len(individualTransWithBug) == 0:
		return
	'''
	if thisBug not in allBugsToTrans.keys():
		print thisBug
		print '\toccurrences when using all bugs versus occurrences with just the one bug'
		print '\t\t'+'0'+ '/'+str(len(individualTransWithBug))+ '\t'
		print '\t\t'+'0'+'%'
		print 
		return
		
	allBugsTransWithThisBug = allBugsToTrans[thisBug]
	
	#for trans in individualTransWithBugs:
	print thisBug 
	print '\toccurrences when using all bugs versus occurrences with just the one bug'
	print '\t\t'+str(len(allBugsTransWithThisBug))+ '/'+str(len(individualTransWithBug))+ '\t'
	print '\t\t'+str((float(len(allBugsTransWithThisBug))/len(individualTransWithBug))*100)+'%'
	print 
	
	bugsThatReplacedIt = []

	for trans in individualTransWithBug:
		if trans not in allBugsTransWithThisBug:
			if trans in allTransToBugs.keys():
				bugsThatReplacedIt.append(allTransToBugs[trans] )
			
	sys.stdout.write('\tBugs that replaced it:\n')
	for bug in bugsThatReplacedIt:
		sys.stdout.write('\t\t'+bug+'\n')
	print '\n'
	'''
	
'''
	Go through the log where all bug rules were performed.  
	allBugsToTrans = dictionary relating the bugs found in this file to the transactionID
		on which they were fired
	allTransToBugs = dictionary relating each transaction to a bug that might have been fired
		on it
'''
def initAllBugs():
	filename = 'gill3bugs.txt'
	logs = open(filename,'r')
	firstLine = logs.readline().split("\t")

	feedbackIndex = 0
	transactionIndex = 0
	
	c = 0
	for tok in firstLine :
		if tok == "Feedback Text":
			feedbackIndex = c
		if tok == "CF (orig_trans_id)":
			transactionIndex = c
		c+=1
	
	noFirstLine = True
	for line in open(filename,'r').readlines():
		if noFirstLine:
			noFirstLine = False
			continue
		tokens = line.split('\t')
		bug = tokens[feedbackIndex]
		trans = tokens[transactionIndex]
		if len(bug) < 15:
			continue
		if bug[0:13] != 'Bug!!! Name: ':
			continue
		bug = bug[13:len(bug)]
		
		allTransToBugs[trans] = bug
		if bug not in allBugsToTrans.keys():
			allBugsToTrans[bug] =[trans]
		else:
			allBugsToTrans[bug].append(trans)
		

if __name__ == "__main__": main()