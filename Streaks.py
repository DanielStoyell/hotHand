"""Meant for the examination of streak shooting of basketball players,
based on input data of a file containing a line of 0s and 1s, 1 being a
score and 0 being a miss. For a given player, the program analyses the
conditional probabilities of each shot individually to reveal overall
trends on whether an individual shot is impacted by the success of
previous shots"""

#TODO:
#1: Add complements to output
#2: Test

import sys
import time

class Shooter(object):
	"""A single shooter, filled with data from input file.
	INSTANCE ATTRIBUTES:
		_name [String]: The name of the shooter
		_shots [String]: Raw data for the specific shooter
		_totalShots [int>0]: Number of shots taken
		_hitAfterMiss [List of ints]: Number of hits after a streak of misses
		equal to index
		_missStreak [List of ints]: Corresponds to _hitAfterMiss, total number of
		times a streak of misses happened of length index
		_hitAfterHit [list of ints]: Number of hits after a streak of hits equal
		to index
		_hitStreak [List of ints]: Corresponds to _hitAfterHit, total number of
		times a streak of hits happened of length index
		_longestMiss [int>=0]: Longest miss streak
		_longestHit [int>=0]: Longest hit streak
		_hasBreak [Bool]: False if no breaks in shots, True otherwise
		_runs [list of int>0]: Number of runs in the shot input"""
		
	#Initializer, creates attributes and sets their initial positions
	def __init__(self, n):
		self._name = n
		self._shots = ""
		self._totalShots = 0
		self._hitAfterMiss = [0,0,0,0,0,0]
		self._missStreak = [0,0,0,0,0,0]
		self._hitAfterHit = [0,0,0,0,0,0]
		self._hitStreak = [0,0,0,0,0,0]
		self._longestMiss = 0
		self._longestHit = 0
		self._hasBreak = False
		self._runs = [1] #Initialized at 1 because the first index counts as the first run
		
	#For easy data printing, or file output
	def __str__(self):
		info = ""
		info += "SHOOTER: " + self._name + "\n"
		if self._hasBreak:
			info += "*GAPS IN DATA*\n"
		info += "Total Shots: " + str(self._totalShots) + "\n"
		info += "P(H): " + str(self._hitAfterMiss[0]) + "/" + str(self._totalShots)
		info += "  (" + str(round(float(self._hitAfterMiss[0])/float(self._totalShots), 3)) + ")" + "\n\n"
		info += "Conditional Probabilities:\n"
		for streak in range(1,6):
			if self._hitStreak[streak] != 0:
				info += "P(H|" + str(streak) + "H): " + str(self._hitAfterHit[streak]) + "/" + str(self._hitStreak[streak])
				info += "  (" + str(round(float(self._hitAfterHit[streak])/float(self._hitStreak[streak]), 3)) + ")\n"
			else:
				info += "P(H|" + str(streak) + "H): 0/0  (N/A)\n"
			info += "    Complement: " + str(self._hitAfterMiss[0] - self._hitAfterHit[streak]) + "/" + str(self._totalShots - self._hitStreak[streak])
			info += "  (" + str(round(float(self._hitAfterMiss[0] - self._hitAfterHit[streak])/float(self._totalShots - self._hitStreak[streak]), 3)) + ")\n"
		info += "\n"
		for streak in range(1,6):
			if self._missStreak[streak] != 0:
				info += "P(H|" + str(streak) + "M): " + str(self._hitAfterMiss[streak]) + "/" + str(self._missStreak[streak])
				info += "  (" + str(round(float(self._hitAfterMiss[streak])/float(self._missStreak[streak]), 3)) + ")\n"
			else:
				info += "P(H|" + str(streak) + "M): 0/0  (N/A)\n"
			info += "    Complement: " + str(self._hitAfterMiss[0] - self._hitAfterMiss[streak]) + "/" + str(self._totalShots - self._missStreak[streak])
			info += "  (" + str(round(float(self._hitAfterMiss[0] - self._hitAfterMiss[streak])/float(self._totalShots - self._missStreak[streak]), 3)) + ")\n"
		info += "\nLongest Hit Streak: " + str(self._longestHit) + "\n"
		info += "Longest Miss Streak: " + str(self._longestMiss) + "\n"
		info += "Number of Runs: " + str(self._runs)[1:-1] + "\n"
		info += "------------------------\n"
		return info
		

def makeAggregate(people): #CAREFUL USING THIS - PROBABILITIES USED SKEWED BY SPLIT DATA
	"""Precondition: people is a list of Shooters
	Takes all the shooters in the list and makes a new shooter
	which is the aggregate of their probabilities"""
	agg = Shooter("AGGREGATE") #Sum/combination of the probabilities of all the shooters
	agg._shots = "N/A"	
	agg._runs = "N/A"				
	for person in people:
		agg._totalShots += person._totalShots
		for i in range(6):
			agg._missStreak[i] += person._missStreak[i]
			agg._hitStreak[i] += person._hitStreak[i]
			agg._hitAfterHit[i] += person._hitAfterHit[i]
			agg._hitAfterMiss[i] += person._hitAfterMiss[i]
		if person._longestMiss > agg._longestMiss:
			agg._longestMiss = person._longestMiss
		if person._longestHit > agg._longestHit:
			agg._longestHit = person._longestHit
	return agg

def hasProperFormat(f):
	onLine = 1
	for line in f:
		if line[-1] == "\n":
			line = line[:-1]
		if onLine%2 == 0:
			for i in range(len(line)):
				if line[i] != "1" and line[i] != "0" and line[i] != " ":
					return False
		elif line[-1] != ":":
			return False
		onLine += 1	
	return True
	
toTest = open(sys.argv[1], 'r')
assert hasProperFormat(toTest), "Improper formatting! Check your file."
toTest.close()

shotData = open(sys.argv[1], 'r')
Shooters = []
for test in shotData:
	if test[-1] == "\n":
		test = test[:-1] #Gets rid of newlines
	if test != "":
		if test[0] != "0" and test[0] != "1": #Not a shot line
			Shooters.append(Shooter(test[:-1])) #Adds the new shooter
		else: #Must be a scoring line
			Shooters[-1]._shots = test
			hitStreak = 0 #Reset appropriate counter variables
			missStreak = 0
			spaces = 0
			onStreak = 0
			for i in range(len(test)):
				if test[i] == " ":
					spaces += 1
			Shooters[-1]._totalShots = len(test)-spaces #Set the values of the latest shooter added to those that can
			Shooters[-1]._missStreak[0] = len(test) #Be grabbed immediately
			Shooters[-1]._hitStreak[0] = len(test)
			for i in range(len(test)):
				if test[i] != " ":
					if i>0 and test[i] != test[i-1]:
						Shooters[-1]._runs[onStreak] += 1
					#Find out if this value corresponds to a streak and increment appropriately
					try:
						for streak in range(1,6):
							if test[i-streak:i] == "1"*streak:
								Shooters[-1]._hitStreak[streak] += 1
							if test[i-streak:i] == "0"*streak:
								Shooters[-1]._missStreak[streak] += 1
					except: #Triggered if there aren't enough shots before the current one to check (string out of bounds)
						pass
				else:
					onStreak += 1
					Shooters[-1]._hasBreak = True
					Shooters[-1]._runs += [0]
				
				#Handling miss or hit specific cases
				if test[i] == "0": #Miss code
					hitStreak = 0
					missStreak += 1
					if missStreak > Shooters[-1]._longestMiss:
						Shooters[-1]._longestMiss = missStreak
				elif test[i] == "1": #Hit code
					missStreak = 0
					hitStreak += 1
					if hitStreak > Shooters[-1]._longestHit:
						Shooters[-1]._longestHit = hitStreak
					try:
						for streak in range(6): #Add hit/miss streaks as appropriate, from P(H), P(H|1H), P(H|1M), P(H|2H), ... P(H|5H), P(H|5M)
							if test[i-streak:i] == "1"*streak:
								Shooters[-1]._hitAfterHit[streak] += 1
							if test[i-streak:i] == "0"*streak:
								Shooters[-1]._hitAfterMiss[streak] += 1
					except: #Triggered if there aren't enough shots before the current one to check (string out of bounds)
						pass
								
outputFile = open("StreaksAnalysis.txt", 'w')
for person in Shooters:
	outputFile.write(str(person))
	if not person._hasBreak:
		outputFile.write("\n")
	outputFile.write("")
#aggregate = makeAggregate(Shooters) #Sum/combination of the probabilities of all the shooters
#outputFile.write(str(aggregate))
	
shotData.close()
outputFile.close()