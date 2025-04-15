import logging
import math
import random
from CPUSimulation import simulateCPU
import Config
import DummyProgram
import PhysicalMemory

def administerAllTests(config):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='output.txt', level=logging.DEBUG)

    for i in range(config["testRandomSamplesAmt"]):
        administerTest(generateProgramEntries(config), logger, config)

# Administers tests (from files)
def administerTest(programEntries, logger : logging.Logger, config):
    logger.debug(programEntries)

    pageSizeTests = config["PageSizes"]

    for pageSize in pageSizeTests:
        logger.info(f"Starting {pageSize}.")
        simulateCPU(logger, deepCopyOfProgramEntry(programEntries), PhysicalMemory.PhysicalMemory(config["PhysicalMemorySize"], pageSize))
        logger.info(f"Finished {pageSize}.")
    
    logger.info("Program Finished")

# Generates test cases (output to files)
def generateProgramEntries(config):
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

def deepCopyOfProgramEntry(programEntries):
    temp = {}

    for key, value in programEntries.items():
        temp[key] = DummyProgram.DummyProgram(value.name, value.numberInstructions, value.memoryRequirement)

    return temp

administerAllTests(Config.lazyConfig)