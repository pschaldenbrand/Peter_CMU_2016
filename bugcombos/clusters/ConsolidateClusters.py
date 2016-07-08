import math
import sys
import os
import datetime

filenames = ['gill3_canon_clusters.txt','legters1_canon_clusters.txt','muller2_canon_clusters.txt']

def main():
	errorToProb = {}
	for fn in filenames:
		f = open(fn, 'r')
		for line in f.readlines():
			tokens = line.split('\t')
			if len(tokens) < 2:
				continue
			probability = tokens[0]
			errorList = tokens[1:]
			errorList.sort()
			error = ''
			for i in range(0,len(errorList)):
				error = error + errorList[i]
				if i < len(errorList)-1:
					error = error + ","
			if error not in errorToProb.keys():
				errorToProb[error] = []
			errorToProb[error].append(probability)
	
	for er in errorToProb.keys():
		probList = errorToProb[er]
		avgProb = 0.0
		for prob in probList:
			avgProb = avgProb+float(prob)
		avgProb = avgProb/float(len(probList))
		
		errorList = er.split(',')
		sys.stdout.write(str(avgProb).replace("\n",""))
		sys.stdout.write('\t')
		for i in range(1, len(errorList)):
			sys.stdout.write(errorList[i].replace("\n",""))
			if i < len(errorList)-1:
				sys.stdout.write('\t')
		sys.stdout.write('\n')
		sys.stdout.flush()

if __name__ == "__main__": main()