from math import ceil
import numpy

from Statistics import PageSizeTestLevelStatistic, updateInternalFragmentation, updatePageTableSizeVsProgramSize

class PhysicalMemory:
    def __init__(self, totalSizeBytes, pageSizeBytes, maxProgramSize):
        self.frameAmt: int = int(totalSizeBytes // pageSizeBytes) 
        self.pageSizeBytes : int = int(pageSizeBytes)

        self.pageFrames = numpy.resize(numpy.array([], dtype='<U10'), self.frameAmt)
        self.maxProgramSize = maxProgramSize

        self.unallocatedFramesIndices = []
        for i in range(0, self.frameAmt):
            self.unallocatedFramesIndices.append(i)


    # Returns page table mapping
    def allocateProgram(self, identifier, memoryRequirement, statistics : PageSizeTestLevelStatistic):
        leftOverMemory = memoryRequirement % self.pageSizeBytes
        updateInternalFragmentation(statistics, leftOverMemory, self.pageSizeBytes)
        
        numberOfFramesNeeded = min(ceil(memoryRequirement / self.pageSizeBytes), self.maxProgramSize) 
        # updateInternalFragmentation(statistics, memoryRequirement, self.pageSizeBytes*numberOfFramesNeeded)

        # Make sure that pageAmt doesn't exceed the amount of pages left
        if (not self.canAllocatePageAmt(numberOfFramesNeeded)):
            raise Exception(f"Memory overflow! Unable to allocate {identifier}")

        programPageTable = {}
        programAllocationQueue = []

        # Allocate pages
        for pageIndex in range(numberOfFramesNeeded):
            allocatedFrameIndex = self.pAllocateFrame(f"{identifier}{pageIndex}")

            programPageTable[pageIndex] = allocatedFrameIndex
            programAllocationQueue.append(pageIndex)

        updatePageTableSizeVsProgramSize(statistics, len(programPageTable))
        return (programPageTable, programAllocationQueue)
    
    def pAllocateFrame(self, referenceName):
        # Making private method to eliminate double checking (one made at parent call)
        # Make sure that pageAmt doesn't exceed the amount of pages left
        # if (not self.canAllocate(1)):
        #     raise Exception(f"Memory overflow! Unable to allocate {referenceName}")
        
        # place page into first available memory
        availableIndex = self.unallocatedFramesIndices.pop(0) # (Maintain list too)

        self.pageFrames[availableIndex] = referenceName
        
        return availableIndex

    def deallocateProgram(self, programPageTable, identifier):
        for allocatedFrameIndex in programPageTable.values():
            if not self.canAccess(identifier, allocatedFrameIndex): 
                raise Exception("Cannot access memory with given identifier!")
            
            self.pageFrames[allocatedFrameIndex] = ""
            self.unallocatedFramesIndices.append(allocatedFrameIndex)

    def accessMemory(self, frameIndex, offset, identifier):
        if (frameIndex >= self.frameAmt or offset >= self.pageSizeBytes):
            return False
            # raise Exception("Memory address does not exist!")
        
        # If virtual memory or physical memory

        if not self.canAccess(identifier, frameIndex):
            return False
            # raise Exception("Incorrect permissions!")

        return True
    
    def canAccess(self, identifier, frameIndex):
        result = True
        
        for characterIndex in range(len(identifier)):
            if (self.pageFrames[frameIndex][characterIndex] != identifier[characterIndex]):
                return False

        return result
    
    def canAllocatePageAmt(self, pageAmt):
        return pageAmt <= len(self.unallocatedFramesIndices)
    
    def canAllocateMemoryAmt(self, memoryRequirement):
        pageAmt = ceil(memoryRequirement / self.pageSizeBytes)
        return pageAmt <= len(self.unallocatedFramesIndices)

    def debugOutput(self):
        print(f"Page Frames Size: {self.frameAmt}, Page Size: {self.pageSizeBytes} Bytes")
        print(self.pageFrames)
        print(self.unallocatedFramesIndices)

