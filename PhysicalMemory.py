import numpy

class PhysicalMemory:
    def __init__(self, totalSizeBytes, pageSizeBytes):
        self.frameAmt: int = int(totalSizeBytes // pageSizeBytes) 
        self.pageSizeBytes : int = int(pageSizeBytes)

        self.pageFrames = numpy.resize(numpy.array([], dtype='<U10'), self.frameAmt)

        self.unallocatedFramesIndices = []
        for i in range(0, self.frameAmt):
            self.unallocatedFramesIndices.append(i)

        # self.blockedQueue = [] should be blocked at higher process

    # Returns page table mapping
    def allocateProgram(self, identifier, pageAmt):
        # Make sure that pageAmt doesn't exceed the amount of pages left
        if (not self.canAllocate(pageAmt)):
            raise Exception(f"Memory overflow! Unable to allocate {identifier}")

        programPageTable = {}

        # Allocate pages
        for pageIndex in range(pageAmt):
            allocatedFrameIndex = self.pAllocateFrame(f"{identifier}{pageIndex}")

            programPageTable[pageIndex] = allocatedFrameIndex

        return programPageTable
    
    def pAllocateFrame(self, referenceName):
        # Making private method to eliminate double checking (one made at parent call)
        # Make sure that pageAmt doesn't exceed the amount of pages left
        # if (not self.canAllocate(1)):
        #     raise Exception(f"Memory overflow! Unable to allocate {referenceName}")
        
        # place page into first available memory
        availableIndex = self.unallocatedFramesIndices[0]

        self.pageFrames[availableIndex] = referenceName
        self.unallocatedFramesIndices.pop(0) # Maintain list

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
    
    def canAllocate(self, pageAmt):
        return pageAmt <= len(self.unallocatedFramesIndices)

    def debugOutput(self):
        print(f"Page Frames Size: {self.frameAmt}, Page Size: {self.pageSizeBytes} Bytes")
        print(self.pageFrames)
        print(self.unallocatedFramesIndices)