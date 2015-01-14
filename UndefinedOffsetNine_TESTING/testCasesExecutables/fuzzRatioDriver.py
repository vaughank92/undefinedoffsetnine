import os, sys

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_DIR = os.path.dirname(CURRENT_DIR +"/../")
sys.path.append(PROJECT_DIR)

from project.fuzz import ratio

def main(arguments):
	actualOutput = eval ("ratio(" + arguments + ")")
	return actualOutput

