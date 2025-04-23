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
        
        self.pageSizeTestLevelStatistics : dict[str, PageSizeTestLevelStatistic] = {}

        for size in config["PageSizes"]:
            self.pageSizeTestLevelStatistics[size] = PageSizeTestLevelStatistic(size)
        
class PageSizeTestLevelStatistic:
    def __init__(self, pageSize):
        self.pageSize = pageSize
        self.memoryUseGraph = ([], [])
        self.pageFaultAmt = 0

        self.internalFragmentation = []
        self.pageTableAmounts = []

        self.averageFragmentation = 0
        self.averagePageTableSize = 0

def updateStatisticsWithProgramEntries(stats : PageSizeTestLevelStatistic, programEntries : dict):
    for values  in programEntries.values():
        updateProcessSize(stats, values.numberInstructions)

def updateProcessSize(statistics : SampleTestLevelStatistics, processSize : int):
    statistics.processSizes.append(processSize)

# process memory demand vs. time. 
def updateMemoryUse(statistics : PageSizeTestLevelStatistic, CPUCycle : int, memoryUse : float):
    statistics.memoryUseGraph[0].append(CPUCycle) # x
    statistics.memoryUseGraph[1].append(memoryUse) # y

def updatePageFaults(statistics : PageSizeTestLevelStatistic):
    statistics.pageFaultAmt += 1

# Page table size vs Memory Size
def updateInternalFragmentation(statistics : PageSizeTestLevelStatistic, usedMemorySize, allocatedAmount):
    internalFragmentation = allocatedAmount - usedMemorySize
    statistics.internalFragmentation.append(internalFragmentation)

# page faults per memory access
def updatePageTableSizeVsProgramSize(pageSizeTestLevelStatistic : PageSizeTestLevelStatistic, pageTableAmount):
    pageSizeTestLevelStatistic.pageTableAmounts.append(pageTableAmount)

def compileAndOutputStats(statistics : Statistics, config):
    internalFragmentationResults, pageFaultsResults, pageTableSizeResults = generatePageScoreAverages(statistics, config)

    pageSizeScore = scorePageSizes(internalFragmentationResults, pageFaultsResults, pageTableSizeResults)

    printStats(pageSizeScore)


def generatePageScoreAverages(statistics : Statistics, config):
    # Assemble data into {pageSize: x, result: y} for three measurements average internal fragmentation, page faults per memory access, and page table size
    internalFragmentationResults = []
    pageFaultsResults = []
    pageTableSizeResults = []

    for pageSize in config["PageSizes"]:
        totalFragmentation = 0
        totalPageFaultAmt = 0
        totalTableSizes = 0
        numberOfProcesses = config["NumberOfPrograms"] * config["testRandomSamplesAmt"]

        for sampleTest in statistics.sampleTestStatistics:
            pageSizeTest = sampleTest.pageSizeTestLevelStatistics[pageSize]

            for fragmentation in pageSizeTest.internalFragmentation:
                totalFragmentation += fragmentation
            
            totalPageFaultAmt += pageSizeTest.pageFaultAmt

            for tableSize in pageSizeTest.pageTableAmounts:
                totalTableSizes += tableSize

        averageFragmentation = totalFragmentation / numberOfProcesses
        averagePageFaultAmt = totalPageFaultAmt / numberOfProcesses
        averageTableSizes = totalTableSizes / numberOfProcesses

        internalFragmentationResults.append({"pageSize": pageSize, "result" : averageFragmentation})
        pageFaultsResults.append({"pageSize": pageSize, "result" : averagePageFaultAmt})
        pageTableSizeResults.append({"pageSize": pageSize, "result" : averageTableSizes})

    internalFragmentationResults = sorted(internalFragmentationResults, key=lambda item: item['result'])
    pageFaultsResults = sorted(pageFaultsResults, key=lambda item: item['result'])
    pageTableSizeResults = sorted(pageTableSizeResults, key=lambda item: item['result'])

    return (internalFragmentationResults, pageFaultsResults, pageTableSizeResults)

def scorePageSizes(internalFragmentationResults : list[dict[str, float]], pageFaultsResults : list[dict[str, float]], pageTableSizeResults : list[dict[str, float]]):
    pageSizeScore = {}

    # Add internal fragmentation score
    for i in range(len(internalFragmentationResults)):
        result = internalFragmentationResults[i]
        
        if (result["pageSize"] in pageSizeScore):
            pageSizeScore[result["pageSize"]] += i
        else:
            pageSizeScore[result["pageSize"]] = i

    # Add page fault score
    for i in range(len(pageFaultsResults)):
        result = pageFaultsResults[i]
        
        pageSizeScore[result["pageSize"]] += i

    # Add page table size score
    for i in range(len(pageTableSizeResults)):
        result = pageTableSizeResults[i]
        
        pageSizeScore[result["pageSize"]] += i

    return pageSizeScore

def printStats(scores: dict):
    print("============ Scores ============")
    for pageSize, score in scores.items():
        print(f"{pageSize} bytes : {score} pts")
    print("================================")

def printGraph(statistics: Statistics, config):
    axis = pyplot.subplots(1, 3)[1]

    graphCPUCycleVsMemoryUse(statistics, axis, config)
    graphGraphFragmentationVsMemorySize(statistics, axis)
    pageFaultRateVsPageSize(statistics, axis)

    # figure.suptitle('CPU Cycle vs Memory Use')
    pyplot.show(block=True)

def graphCPUCycleVsMemoryUse(statistics: Statistics, axis : ndarray, config):
    legend_handles = []

    for size, pageColor in config["PageSizeColors"].items():
        formattedSize = "{:.2e}".format(size)

        legend_handles.append(matplotlib.patches.Patch(color=pageColor, label=f"{formattedSize} Bytes"))

    # Graph CPU Cycle vs Memory Use
    for sampleTest in statistics.sampleTestStatistics:
        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics.values():
            color = config["PageSizeColors"][pageSizeTest.pageSize] # "PageSizeColors":{1e3:'b', 1e4:'g', 1e5:'r', 1e6:'c', 1e7:'m'},
            
            axis[0].plot(pageSizeTest.memoryUseGraph[0], pageSizeTest.memoryUseGraph[1], color = color)

    axis[0].set_xlabel('CPU Cycle')
    axis[0].set_ylabel('Memory Use')        

    # BUG: legend doesn't work
    axis[0].legend(handles=legend_handles)

def graphGraphFragmentationVsMemorySize(statistics: Statistics, axis : ndarray):
    # Graph Fragmentation vs memory size (log scale)
    for sampleTest in statistics.sampleTestStatistics:
        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics.values():
            for fragmentationAmount in pageSizeTest.internalFragmentation:
                axis[1].scatter(pageSizeTest.pageSize, fragmentationAmount)

    axis[1].set_xscale('log')
    axis[1].set_xlabel('Page Size')

    axis[1].set_yscale('log')
    axis[1].set_ylabel('Internal Fragmentation')    

def pageFaultRateVsPageSize(statistics : Statistics, axis : ndarray):
    for sampleTest in statistics.sampleTestStatistics:
        for pageSizeTest in sampleTest.pageSizeTestLevelStatistics.values():

            axis[2].scatter(pageSizeTest.pageSize, pageSizeTest.pageFaultAmt)

    axis[2].set_xscale('log')
    axis[2].set_xlabel('Page Size')

    axis[2].set_ylabel('Page Fault')

def generateRandomMemory(size = 10):
    cycles = []
    memoryUse = []

    for i in range(0, size):
        cycles.append(i)
        memoryUse.append(round(random.random() * 100))

    return (cycles, memoryUse)