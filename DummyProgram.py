import random
import PhysicalMemory

# Object for "cpu" to iterate over, contains memory size and number of instructions
class DummyProgram:
    def __init__ (self, name, numberInstructions, memorySize):
        self.name = name
        self.numberInstructions = numberInstructions
        self.memorySize = memorySize
        self.lastMemoryAccess = (0, 0)
        self.pageTable = {}

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
    instructionLocation = determineNextMemoryAccessLocation(program.lastMemoryAccess, physicalMemory.pageSizeBytes, program.memorySize)

    physicalMemory.accessMemory(program.pageTable[instructionLocation[0]], instructionLocation[1], program.name)

    program.lastMemoryAccess = instructionLocation
    program.numberInstructions -= 1

    return program.numberInstructions == 0

# Bell curve function for "realistic memory access"
def determineNextMemoryAccessLocation(lastMemoryAccess, pageSize, programMemorySize):
    x = random.random()

    if (x > 0.9):
        return (random.randint(0, programMemorySize - 1), random.randint(0, pageSize - 1))
    else:
        return (lastMemoryAccess[0], (lastMemoryAccess[1] + 1 ) % pageSize)
    