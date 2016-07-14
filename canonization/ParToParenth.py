import math
import sys
import os

def main():
	for line in open('megaOutputTime.txt','r').readlines():
		line = line.replace('eq','=')
		firstPar = True
		increment = 0
		for i in range(0,len(line)):
			if increment > 0:
				increment += -1
				continue
			if i < len(line)-3:
				if line[i:i+3] == 'par':
					if firstPar:
						sys.stdout.write('(')
						firstPar = False
					else:
						sys.stdout.write(')')
					increment = 2
				else:
					sys.stdout.write(line[i])
			else:
				sys.stdout.write(line[i])
		#sys.stdout.write('\n')

if __name__ == "__main__": main()