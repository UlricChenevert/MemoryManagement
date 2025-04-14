import math
import random
import Config
import DummyProgram

# Generates test cases (output to files)
def generateTests(config):
    numberOfPrograms = config["NumberOfPrograms"]

    nextTime = 0
    programsSchedule = {}

    for i in range(numberOfPrograms):
        programsSchedule[nextTime] = DummyProgram.generateRandomProgram(createNameFromIndex(i), config)

        nextTime += nextArrivalTime()

    return programsSchedule
    
# Random equation of internet :)
def nextArrivalTime(averageTimeInterval = Config.lazyConfig["AverageArrivalTime"]):
    return round(-1 * math.log(1 - random.random()) * averageTimeInterval) # * λ = 1/T so T

def createNameFromIndex(index):
    return hex(index)[2:]

# Administers tests (from files)
def administerTest():
    pass

# Records statistics

# Outputs statistics to files

# Blocked Queue
# FIFO Queue