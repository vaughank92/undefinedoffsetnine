#FuzzyWuzzyTestDriver.py
import os, sys, getopt, re

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR +"/../")
TEST_CASE_DIRECTORY = os.path.dirname(PROJECT_DIR+"/testCases/")
sys.path.append(PROJECT_DIR)

from project.fuzz import *
from project.process import *


#Parses the arguments, gives one extra chance before stopping the program for bad input
#input: <list>
#output: <String> <int>
def argHandler(args):
	argLength = len(args)
	fileName = None
	testNum = None

	if(argLength > 0):
		try:
			fileName = sys.argv[1]
		except ValueError:
			print("An invalid type for input \"file\" found. Expected type: STRING")
			returnValue = input("Enter valid input: ")

	if(argLength > 1):
		try:
			testNum = sys.argv[2]
		except ValueError:
			print("An invalid type for input \"test number\" found. Expected type: STRING")
			returnValue = input("Enter valid input: ")

	return fileName, testNum

#Lists out all the files in the testCases directory.
#output: <list>
def populateTestFiles():
	returnValue = []

	for file in os.listdir(TEST_CASE_DIRECTORY):
		returnValue.append(file)

	return returnValue

#Returns a dictionary containing the test cases.
#input: <string>
#output: <dictionary={1: 'function' , 'inputValues', 'expectedOutput'}>
def parseTestFile(fileString):
	returnValue = {}
	testNum = None
	with open(TEST_CASE_DIRECTORY+"/"+fileString, 'r') as scanner:
		for line in scanner:
			if('Test' in line):
				testNum = lineStripper(line)
				returnValue[testNum] = {}
			elif ('function' in line):
				tempFunction = lineStripper(line)
				returnValue[testNum]['function'] = tempFunction
			elif ('input' in line):
				tempInputValue  = lineStripper(line)
				returnValue[testNum]['inputValues'] = tempInputValue
			elif ('output' in line):
				tempOutput = lineStripper(line)
				returnValue[testNum]['expectedOutput'] = tempOutput
	return returnValue

#Strips a line of the tags, and outside whitespace.
#input: <string>
#output: <string>
def lineStripper(lineString):
	returnValue = lineString.split(':')[1]
	returnValue = returnValue.strip()
	return returnValue

#Runs the test for specified test and testcase
#input: <string> <string>
def runTests(test, testCase):
	testedOutput = str(eval(test[testCase]['function']+"("+test[testCase]['inputValues']+")"))
	if(testedOutput != test[testCase]['expectedOutput']):
		print("Function: " + test[testCase]['function'] + "\tCase: " + testCase + " Failed")
		print("Input Values: " + test[testCase]['inputValues'])
		print("Current Output: " + testedOutput)
		print("Expected Output: " + test[testCase]['expectedOutput'])
		print()
	else:
		print("Function: " + test[testCase]['function'] + "\tCase: " + testCase + " Passed")
		print()


print("\nBegin Testing\n")

fileName, testNum = argHandler(sys.argv[1:])
testList = populateTestFiles()
toTest = []

if (fileName is None):
	for i in testList:
		toTest.append(parseTestFile(i))
else:
	for i in testList:
		if(fileName in i):
			toTest.append(parseTestFile(i))

for test in toTest:
	if(testNum is None):
		for testCase in test:
			runTests(test, testCase)
	else:
		runTests(test,testNum)

print("End Testing")
