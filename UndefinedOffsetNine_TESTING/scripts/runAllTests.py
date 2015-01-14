#!/usr/bin/env python
import os, sys, getopt
import webbrowser

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR +"/../")
TEST_CASE_DIRECTORY = os.path.dirname(PROJECT_DIR + "/testCases/")
DRIVER_DIRECTORY = os.path.dirname(PROJECT_DIR + "/fuzzTestCasesExecutables/")
OUTPUT_DIRECTORY = os.path.dirname(PROJECT_DIR + "/reports/")
sys.path.append(PROJECT_DIR)

def clearFiles():
	name = 'testReport.html'
	#print name
	for root, dirs, files in os.walk(OUTPUT_DIRECTORY):
	 	#print ('clearFiles')
	 	if name in files:
	 		print ('file found, clearing...')
	 		os.remove(OUTPUT_DIRECTORY+'/'+name)
	 	else:
	 		print('File not found')
	
def parseTestCase(txtFile):
	#here for testing purposes
	#print('parseTestCase')

	def lineStripper(lineString):
		returnValue = lineString.split(':', 1)[1]
		returnValue = returnValue.strip()
		return returnValue
		
	returnValue = {}
	testNum = None
	with open(TEST_CASE_DIRECTORY+"/"+txtFile, 'r') as scanner:
		for line in scanner:
			if('testNumber' in line):
				returnValue['testNumber'] = lineStripper(line)
			elif ('requirement' in line):
				returnValue['requirement'] = lineStripper(line)
			elif ('component' in line):
				returnValue['component'] = lineStripper(line)
			elif ('method' in line):
				returnValue['method'] = lineStripper(line)
			elif('inputs' in line):
				returnValue['inputs'] = lineStripper(line)
			elif('driver' in line):
				returnValue['driver'] = lineStripper(line)
			elif('expectedOutput' in line):
				returnValue['expectedOutput'] = lineStripper(line)
	return returnValue
	
def runDriver(testCase):
	driver = testCase['driver']
	exec('from testCasesExecutables.' + driver+ ' import main')
	return main(testCase['inputs'])
	
def compareExpectedToActual(actualOutput, expectedOutput):

	#having to check the types...
	# print (isinstance(actualOutput, int))
	# print(isinstance(expectedOutput, int))

	#type casting because expectedOutput is a string
	if actualOutput == int(expectedOutput):
		compare = "Pass"
	else:
		compare = "Fail"
	return compare

def setUpHTML(outputFile):
	#here for testing purposes
	#print ('setUpHTML')

	outputFile.write("<!DOCTYPE html>\n")
	outputFile.write("<html>\n")
	outputFile.write("\t<head>\n")
	outputFile.write("\t\t<title>FuzzyWuzzy.py Test Report</title>\n")
	outputFile.write("\t</head>\n")
	outputFile.write("\t<body>\n")
	outputFile.write("\t\t<table border=\"1\" style=\"width:100%\">\n")
	outputFile.write("\t\t\t<tr>\n")
	outputFile.write('\t\t\t\t<td>Test Number</td>\n')
	outputFile.write('\t\t\t\t<td>Requirement</td>\n')
	outputFile.write('\t\t\t\t<td>Component</td>\n')
	outputFile.write('\t\t\t\t<td>Method</td>\n')
	outputFile.write('\t\t\t\t<td>Inputs</td>\n')
	outputFile.write('\t\t\t\t<td>Driver</td>\n')
	outputFile.write('\t\t\t\t<td>Expected Output</td>\n')
	outputFile.write('\t\t\t\t<td>Actual Output</td>\n')
	outputFile.write('\t\t\t\t<td>Pass/Fail</td>\n')
	outputFile.write('\t\t\t</tr>\n')

def createFormattedHTML(testCase, actualOutput, compareResult):
	#here for testing purposes
	#print ('createFormattedHTML')
	if compareResult == "Pass":
		color = "green"
	else:
		color = "red"

	returnString = ('\t\t\t<tr>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['testNumber']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['requirement']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['component']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['method']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['inputs']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['driver']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+testCase['expectedOutput']+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td>'+str(actualOutput)+'</td>\n')
	returnString = returnString + ('\t\t\t\t<td><font color ='+color+'>'+compareResult+'</font></td>\n')
	returnString = returnString + ('\t\t\t</tr>\n')
	return returnString

def finishHTML(outputFile):
	#here for testing purposes
	#print ('finishHTML')

	outputFile.write("\t\t</table>\n")
	outputFile.write("\t</body>\n")
	outputFile.write("</html>")

def run():
	clearFiles()
	with open(OUTPUT_DIRECTORY + "/testReport.html", 'w') as outputFile:
		setUpHTML(outputFile)
		for file in os.listdir(TEST_CASE_DIRECTORY):
			testCase = parseTestCase(file)
			actualOutput = runDriver(testCase)
			compareResult = compareExpectedToActual(actualOutput, testCase['expectedOutput'])
			outputFile.write(createFormattedHTML(testCase, actualOutput, compareResult))
		finishHTML(outputFile)
	webbrowser.open(OUTPUT_DIRECTORY + "/testReport.html")

run()
