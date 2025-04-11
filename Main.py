import PhysicalMemory
from TestSuite import generateTests

physicalMemory = PhysicalMemory.PhysicalMemory(10, 1)

def attemptAllocate(blocked):
    if (physicalMemory.canAllocate())


a = physicalMemory.allocateProgram("aa", 3)
b = physicalMemory.allocateProgram("bb", 4)
c = physicalMemory.allocateProgram("cc", 2)
physicalMemory.deallocateProgram(c, "cc")
physicalMemory.deallocateProgram(b, "bb")
d = physicalMemory.allocateProgram("dd", 4)
physicalMemory.debugOutput()