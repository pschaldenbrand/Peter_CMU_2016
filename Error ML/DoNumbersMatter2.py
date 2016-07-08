import math
import sys
import os

model = {}
realEqToCorrectInput = {}
realEqToWrongInput = {}

def main():
	#for fn in os.listdir('./processedLogs'):
		#allLines = open('processedLogs/'+fn,'r').readlines()
	allLines = open('megaOutput.txt','r').readlines()
	for line in allLines:
		tokens = line.split('\t')
		
		realEq = tokens[0].replace(" ","")# + " => " + tokens[1]
		canonEq = convertConstants(realEq).replace(" ","")
	
		if canonEq not in model.keys():
			model[canonEq] = {}
		if realEq not in model[canonEq].keys():
			model[canonEq][realEq] = [0,0]
		
	
		if tokens[2].lower() == 'correct':
			model[canonEq][realEq][0] += 1
			if realEq not in realEqToCorrectInput.keys():
				realEqToCorrectInput[realEq] = []
			if tokens[1] not in realEqToCorrectInput[realEq]:
				realEqToCorrectInput[realEq].append(tokens[1])
		else:
			if realEq not in realEqToWrongInput.keys():
				realEqToWrongInput[realEq] = []
			if tokens[1] not in realEqToWrongInput[realEq]:
				realEqToWrongInput[realEq].append(tokens[1])
		model[canonEq][realEq][1] += 1
	
	sumStdDev = 0.0
	zeroStdDev = 0
	eqToDev = {}
	allStdDev =[]
	for can in model.keys():
		if len(model[can].keys()) > 1:
			print can
			values = []
			for real in model[can].keys():
				times = model[can][real][0]
				outOf = model[can][real][1]
				values.append(float(times)/float(outOf))
				#sys.stdout.write(str(float(times)/float(outOf)) + '\t')
				#sys.stdout.write(str(times)+"/"+str(outOf) + '\t')
				sys.stdout.write( '\t\t'+str((float(times)/float(outOf))*100.0)[0:4]+'%\t')
				sys.stdout.write(str(times)+'/'+str(outOf)+' \t'+real+'\n')
				if real in realEqToCorrectInput.keys():
					sys.stdout.write('\t\t\tCorrect Input:   ')
					for input in realEqToCorrectInput[real]:
						sys.stdout.write('{'+input+'}  ')
					print
				
				if real in realEqToWrongInput.keys():
					sys.stdout.write('\t\t\tIncorrect Input: ')
					for input in realEqToWrongInput[real]:
						sys.stdout.write('{'+input+'}  ')
					print
			stdDeviation = stdDev(values)
			allStdDev.append(stdDeviation)
			sumStdDev += stdDeviation
			eqToDev[can] = stdDeviation
			if stdDeviation == 0.0:
				zeroStdDev+=1
			print '\tStandard Deviation:\t'+str(stdDeviation)
			print 
	print 'Number of Std Deviations == 0:\t'+str(zeroStdDev)+ ' out of '+ str(len(allStdDev))+'\n'
	print 'Average Standard Deviation:\t'+str(sumStdDev/float(len(allStdDev)))
	print
	printLargestStdDev( 10, eqToDev )
	devBins = [0,0,0,0,0,0,0,0,0,0,0]
	for v in allStdDev:
		v = int(v*20)
		devBins[v] += 1
	i = 0.0
	j = 0.05
	print
	for v in devBins:
		print "# of standard deviations between "+str(i)+'\t-  '+str(j)+': \t'+str(v)
		i += .05
		j+= .05
		
		
def stdDev( vals ):
	mean = 0
	sum = 0
	for i in range(0, len(vals)):
		sum += float(vals[i])
	mean = float(sum) / float(len(vals))
	
	sqDistSum = 0.0
	for num in vals:
		sqDistSum += (float(num) - mean)**2
	
	stdDeviation = (sqDistSum/float(len(vals))) ** (1.0/2.0)
	return stdDeviation

def printLargestStdDev( count, dict ):
	'''top = []
	for eq in dict.keys():
		if len(top) < count-1:
			top.append(eq)
			continue
		currDev = dict[eq]
		for topEq in top:
			if dict[topEq]'''
	#print 'These steps have standard deviations of 1:'
	maxEq = 0
	maxDev = 0.0
	for eq in dict.keys():
		if dict[eq] > maxDev:
			maxDev = dict[eq]
			maxEq  = 1
		if dict[eq] == maxDev:
			maxEq += 1
	print 'Largest Std Deviation:\t'+str(maxDev)+'\n\t'+str(maxEq)+' equations with this value'
		

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