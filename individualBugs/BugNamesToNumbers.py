
import math
import sys
import os


def main():
	bugToNum = []
	for line in open('WhichBugsWereInAllButNotIndi.txt','r'):
		tokens = line.split('\s+')
		
		for t in tokens:
			if t[0:4] == 'bug-':
				if t in bugToNum:
					print bugToNum[bugToNum.index(t)]
				else







if __name__ == "__main__": main()