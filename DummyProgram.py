import random
import PhysicalMemory

# Object for "cpu" to iterate over, contains memory size and number of instructions
class DummyProgram:
    def __init__ (self, name, numberInstructions, memoryRequirement):
        self.name = name
        self.numberInstructions = numberInstructions
        self.memoryRequirement = memoryRequirement

        self.lastMemoryAccess = 0

        # Updated upon memory allocation
        self.pageTable = {}
        self.replacementQueue = []

def generateRandomProgram(name, config):
    size = random.randint(0, 2)

    configMemorySizeCache = config["ProgramMemorySizes"]
    configProgramInstructionSizeCache = config["ProgramInstructionSizes"]

    if (size == 0):
        memorySize = random.randint(configMemorySizeCache["Small"]["Min"], configMemorySizeCache["Small"]["Max"])
        instructionsSize = random.randint(configProgramInstructionSizeCache["Small"]["Min"], configProgramInstructionSizeCache["Small"]["Max"])

    elif (size == 1):
        memorySize = random.randint(configMemorySizeCache["Medium"]["Min"], configMemorySizeCache["Medium"]["Max"])
        instructionsSize = random.randint(configProgramInstructionSizeCache["Medium"]["Min"], configProgramInstructionSizeCache["Medium"]["Max"])
    
    else:
        memorySize = random.randint(configMemorySizeCache["Large"]["Min"], configMemorySizeCache["Large"]["Max"])
        instructionsSize = random.randint(configProgramInstructionSizeCache["Large"]["Min"], configProgramInstructionSizeCache["Large"]["Max"])

    return DummyProgram(name, instructionsSize, memorySize)

# Run for programs
def runProgramCycle(program : DummyProgram, physicalMemory : PhysicalMemory.PhysicalMemory):
    # Get next instruction location
    nextInstructionLocation = determineNextMemoryAccessLocation(program.lastMemoryAccess, program.memoryRequirement)
    logicalFrameIndex = nextInstructionLocation // physicalMemory.pageSizeBytes
    offset = nextInstructionLocation % physicalMemory.pageSizeBytes

    physicalFrameIndex = program.pageTable[logicalFrameIndex]

    # Get frame index and offset index
    physicalMemory.accessMemory(physicalFrameIndex, offset, program.name)

    # Update member variables
    program.lastMemoryAccess = nextInstructionLocation

    # Decrement instruction amt
    program.numberInstructions -= 1

    # Determine if program is finished
    return program.numberInstructions <= 0

# Bell curve function for "realistic memory access"
def determineNextMemoryAccessLocation(lastMemoryAccess, programMemorySize):
    chance = random.random()

    if (chance > 0.9):
        return random.randint(0, programMemorySize - 1) 
    else:
        return lastMemoryAccess + 1
    