import Config
import DummyProgram
import PhysicalMemory
from TestSuite import generateTests

def simulate(programsSchedule : dict, physicalMemory : PhysicalMemory.PhysicalMemory):
    blockedQueue = []
    runningProgramsQueue = []
    clockCycle = 0

    while (not isFinished(physicalMemory, programsSchedule, blockedQueue, runningProgramsQueue)):
        
        # Try to allocate program
        if (clockCycle in programsSchedule):
            nextProgram : DummyProgram.DummyProgram = programsSchedule[clockCycle]
            programsSchedule.pop(clockCycle)

            if physicalMemory.canAllocate(nextProgram.memorySize):
                nextProgram.pageTable = physicalMemory.allocateProgram(nextProgram.name, nextProgram.memorySize)

                # Add to current program list
                runningProgramsQueue.append(nextProgram)
            else:
                # If not place on blocked queue
                blockedQueue.append(nextProgram)

        # Run program current program (if any)
        if (len(runningProgramsQueue) == 0): continue
        currentProgram : DummyProgram.DummyProgram = runningProgramsQueue[0]
        isFinished = DummyProgram.runProgramCycle(currentProgram, physicalMemory)

        # if finished deallocate
        if (isFinished):
            physicalMemory.deallocateProgram(currentProgram.pageTable, currentProgram.name)
            runningProgramsQueue.pop(0)

            # Try to place program from blocked queue into place
            if len(blockedQueue) > 0:
                blockedProgram = blockedQueue[0]

                if physicalMemory.canAllocate(blockedProgram.memorySize):
                    # Add to current program list
                    runningProgramsQueue.append(blockedProgram)
                    blockedQueue.pop(0)
                else:
                    # If not place on blocked queue
                    blockedQueue.append(blockedProgram)

        print(physicalMemory.pageFrames)

        clockCycle += 1

def isFinished(physicalMemory, programsSchedule, blockedQueue, runningProgramsQueue):
    isScheduleEmpty = programsSchedule.__len__() == 0
    isMemoryEmpty = len(physicalMemory.unallocatedFramesIndices) == physicalMemory.frameAmt
    isQueuesEmpty = len(blockedQueue) > 0 or len(runningProgramsQueue) > 0

    return isScheduleEmpty and isMemoryEmpty and isQueuesEmpty

tests = generateTests(Config.lazyConfig)
print(tests)

simulate(tests, PhysicalMemory.PhysicalMemory(600, 1))