import sys
import random
random.seed()

target = open("C:\\Users\\Daniel\\Desktop\\Gilovich Shooting\\Generated.txt", 'w')

streak = ""
SHOOTING_AVG = .3
for i in range(int(sys.argv[1])):
	if random.random() < SHOOTING_AVG:
		streak += "1"
	else:
		streak += "0"
	
target.truncate()
target.write(streak)