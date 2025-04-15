import logging
import DummyProgram
import PhysicalMemory

def simulateCPU(loggerObject, programsSchedule : dict, physicalMemory : PhysicalMemory.PhysicalMemory):
    blockedQueue = []
    runningProgramsQueue = []
    clockCycle = 0

    while not isSimulationFinished(physicalMemory, programsSchedule, blockedQueue, runningProgramsQueue):
        
        # Try to place program from blocked queue into memory
        if len(blockedQueue) > 0:
            blockedProgram : DummyProgram.DummyProgram = blockedQueue[0]

            if physicalMemory.canAllocateMemoryAmt(blockedProgram.memoryRequirement):
                #Update page table
                coordinateProgramAllocation(blockedProgram, runningProgramsQueue, physicalMemory)
                blockedQueue.pop(0)
            
        # Try to allocate program from program entry
        if (clockCycle in programsSchedule):
            nextProgram : DummyProgram.DummyProgram = programsSchedule.pop(clockCycle)

            if physicalMemory.canAllocateMemoryAmt(nextProgram.memoryRequirement):
                #Update page table
                coordinateProgramAllocation(nextProgram, runningProgramsQueue, physicalMemory)
            else:
                # If not place on blocked queue
                blockedQueue.append(nextProgram)
            
        # Run program current program (if any)
        if (len(runningProgramsQueue) > 0): 
            currentProgram : DummyProgram.DummyProgram = runningProgramsQueue[0]
            isProgramFinished = DummyProgram.runProgramCycle(currentProgram, physicalMemory)

            # if finished deallocate
            if (isProgramFinished):
                coordinateProgramDeallocation(currentProgram, runningProgramsQueue, physicalMemory)

        logCPU(loggerObject, clockCycle, runningProgramsQueue, blockedQueue, physicalMemory)

        clockCycle += 1

def coordinateProgramAllocation(process : DummyProgram.DummyProgram, runningProgramsQueue : list, physicalMemory : PhysicalMemory.PhysicalMemory):
    #Update page table and allocate program
    process.pageTable = physicalMemory.allocateProgram(process.name, process.memoryRequirement)

    # Add to current program list
    runningProgramsQueue.append(process)

def coordinateProgramDeallocation(process : DummyProgram.DummyProgram, runningProgramsQueue : list, physicalMemory : PhysicalMemory.PhysicalMemory):
    physicalMemory.deallocateProgram(process.pageTable, process.name)
    runningProgramsQueue.pop(0)


def isSimulationFinished(physicalMemory : PhysicalMemory.PhysicalMemory, programsSchedule : dict, blockedQueue : list, runningProgramsQueue : list):
    isScheduleEmpty = programsSchedule.__len__() == 0
    isMemoryEmpty = len(physicalMemory.unallocatedFramesIndices) == physicalMemory.frameAmt
    isQueuesEmpty = len(blockedQueue) == 0 and len(runningProgramsQueue) == 0

    return isScheduleEmpty and isMemoryEmpty and isQueuesEmpty

def logCPU(logger : logging.Logger, clockCycle : int, runningProgramsQueue : list, blockedQueue : list, physicalMemory : PhysicalMemory.PhysicalMemory):
    logger.debug(f"Clock Cycle {clockCycle}")
    logger.debug(f"Running Processes Amt: {len(runningProgramsQueue)} ")
    logger.debug(f"Blocked Processes Amt: {len(blockedQueue)} ")
    usage = round((physicalMemory.frameAmt - len(physicalMemory.unallocatedFramesIndices)) / physicalMemory.frameAmt * 100)
    if (usage > 90):
        print("!")
    
    logger.debug(f"Memory Usage: {usage}%")
