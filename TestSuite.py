import logging
import math
import random
from CPUSimulation import simulateCPU
import Config
import DummyProgram
import PhysicalMemory
import Statistics

def administerAllTests(config):
    logger = logging.getLogger(__name__)
    logging.basicConfig(filename='output.txt', level=logging.DEBUG)

    statistics : Statistics.Statistics = Statistics.Statistics(config)

    for i in range(config["testRandomSamplesAmt"]):
        programEntries = generateProgramEntries(config)
        
        Statistics.updateStatisticsWithProgramEntries(statistics.sampleTestStatistics[i], programEntries)

        administerTest(programEntries, logger, statistics.sampleTestStatistics[i], config)

    Statistics.calculateAllStats(statistics)
    # Statistics.printStats(statistics)
    Statistics.printGraph(statistics, config)

# Administers tests (from files)
def administerTest(programEntries, logger : logging.Logger, sampleTestStatistics : Statistics.SampleTestLevelStatistics, config):
    logger.debug(programEntries)

    pageSizeTests = config["PageSizes"]

    for i in range(len(pageSizeTests)):
        pageSize = pageSizeTests[i]
        
        logger.info(f"Starting {pageSize}.")
        simulateCPU(logger, deepCopyOfProgramEntry(programEntries), PhysicalMemory.PhysicalMemory(config["PhysicalMemorySize"], pageSize, config["MaxFrameSize"]), sampleTestStatistics.pageSizeTestLevelStatistics[i])
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
