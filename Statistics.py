from math import sqrt
import random

import matplotlib
import matplotlib.pyplot as pyplot
from numpy import ndarray

class Statistics:
    def __init__(self, config):
        self.sampleTestStatistics : list[SampleTestLevelStatistics] = []

        # Identified by sample, then test

        for _ in range(config["testRandomSamplesAmt"]):
            self.sampleTestStatistics.append(SampleTestLevelStatistics(config))

class SampleTestLevelStatistics:
    def __init__(self, config):

        self.processSizes = []
        self.averageProcessSize = 0
        self.processSizeStandardDeviation = 0
        
        self.pageSizeTestLevelStatistics : list[PageSizeTestLevelStatistics] = []

        for size in config["PageSizes"]:
            self.pageSizeTestLevelStatistics.append(PageSizeTestLevelStatistics(size))
        
class PageSizeTestLevelStatistics:
    def __init__(self, pageSize):
        self.pageSize = pageSize
        # self.programTestLevelStatistics : list[ProgramTestLevelStatistics] = []
        self.memoryUseGraph = ([], [])

        self.internalFragmentation = []
        self.pageTableAmounts = []

        self.averageFragmentation = 0
        self.averagePageTableSize = 0

def updateStatisticsWithProgramEntries(stats : SampleTestLevelStatistics, programEntries : dict):
    for values  in programEntries.values():
        updateProcessSize(stats, values.numberInstructions)

def updateProcessSize(statistics : SampleTestLevelStatistics, processSize : int):
    statistics.processSizes.append(processSize)

# process memory demand vs. time. 
def updateMemoryUse(statistics : PageSizeTestLevelStatistics, CPUCycle : int, memoryUse : float):
    statistics.memoryUseGraph[0].append(CPUCycle) # x
    statistics.memoryUseGraph[1].append(memoryUse) # y

# Page table size vs Memory Size
def updateInternalFragmentation(statistics : PageSizeTestLevelStatistics, programMemorySize, totalAllocationAmount):
    internalFragmentation = totalAllocationAmount - programMemorySize
    statistics.internalFragmentation.append(internalFragmentation)

# page faults per memory access
def updatePageTableSizeVsProgramSize(pageSizeTestLevelStatistics : PageSizeTestLevelStatistics, pageTableAmount):
    pageSizeTestLevelStatistics.pageTableAmounts.append(pageTableAmount)

def calculateAllStats(statistics : Statistics):

    for sampleTest in statistics.sampleTestStatistics:
        # Process average size and standard deviation
        if (len(sampleTest.processSizes) > 0):
            sampleTest.averageProcessSize = round(sum(sampleTest.processSizes) / len(sampleTest.processSizes))

            standardDeviationTotal = 0
            for size in sampleTest.processSizes:
                standardDeviationTotal += pow(size - sampleTest.averageProcessSize, 2)
            sampleTest.processSizeStandardDeviation = sqrt(standardDeviationTotal/len(sampleTest.processSizes))

        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics:
            # Internal Fragmentation
            if (len(pageSizeTest.internalFragmentation) > 0):
                pageSizeTest.averageFragmentation = sum(pageSizeTest.internalFragmentation) / len(pageSizeTest.internalFragmentation)

            # Page Table Size
            if (len(pageSizeTest.pageTableAmounts) > 0):
                pageSizeTest.averagePageTableSize = sum(pageSizeTest.pageTableAmounts) / len(pageSizeTest.pageTableAmounts)

# def printStats(statistics: Statistics):
#     for sampleTest in statistics.sampleTestStatistics:
#         print(f"Process Size:")
#         print(f"\tμ: {sampleTest.averageProcessSize}")
#         print(f"\tσ: {sampleTest.processSizeStandardDeviation}") 
#         print()
#         for pageSizeTest in sampleTest.pageSizeTestLevelStatistics:
#             print(f"Memory Efficiency:")
#             print(f"\tPage Table Size: {pageSizeTest.averagePageTableSize}")
#             print(f"\tAverage Fragmentation: {pageSizeTest.averageFragmentation}")

def printGraph(statistics: Statistics, config):
    axis = pyplot.subplots(1, 2)[1]

    graphCPUCycleVsMemoryUse(statistics, axis, config)
    graphGraphFragmentationVsMemorySize(statistics, axis)

    # figure.suptitle('CPU Cycle vs Memory Use')
    pyplot.show(block=True)

def graphCPUCycleVsMemoryUse(statistics: Statistics, axis : ndarray, config):
    legend_handles = []

    for size, pageColor in config["PageSizeColors"].items():
        legend_handles.append(matplotlib.patches.Patch(color=pageColor, label=size))

    # Graph CPU Cycle vs Memory Use
    for sampleTest in statistics.sampleTestStatistics:
        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics:
            color = config["PageSizeColors"][pageSizeTest.pageSize] # "PageSizeColors":{1e3:'b', 1e4:'g', 1e5:'r', 1e6:'c', 1e7:'m'},
            
            axis[0].plot(pageSizeTest.memoryUseGraph[0], pageSizeTest.memoryUseGraph[1], color = color)

    axis[0].set_xlabel('CPU Cycle')
    axis[0].set_ylabel('Memory Use')        

    # BUG: legend doesn't work
    axis[0].legend(handles=legend_handles)

def graphGraphFragmentationVsMemorySize(statistics: Statistics, axis : ndarray):
    # Graph Fragmentation vs memory size (log scale)
    for sampleTest in statistics.sampleTestStatistics:
        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics:
            for fragmentationAmount in pageSizeTest.internalFragmentation:
                axis[1].scatter(pageSizeTest.pageSize, fragmentationAmount)

    axis[1].set_xscale('log')
    axis[1].set_xlabel('Page Size')

    axis[1].set_yscale('log')
    axis[1].set_ylabel('Internal Fragmentation')    

def generateRandomMemory(size = 10):
    cycles = []
    memoryUse = []

    for i in range(0, size):
        cycles.append(i)
        memoryUse.append(round(random.random() * 100))

    return (cycles, memoryUse)