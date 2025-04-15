lazyConfig = {
    "NumberOfPrograms":10,
    "AverageArrivalTime":100,
    "ProgramMemorySizes": {
        "Small" : {"Max":10000, "Min":1000},
        "Medium" : {"Max":100000, "Min":10000},
        "Large" : {"Max":500000, "Min":100000}
    },
    "ProgramInstructionSizes": {
        "Small" : {"Max":100, "Min":10},
        "Medium" : {"Max":500, "Min":100},
        "Large" : {"Max":1000, "Min":500}
    },
    # "ProgramMemorySizes": {
    #     "Small" : {"Max":10, "Min":1},
    #     "Medium" : {"Max":100, "Min":10},
    #     "Large" : {"Max":500, "Min":100}
    # },
    "PageSizes":[1e3, 1e4, 1e5, 1e6, 1e6, 1e7], # In Bytes ranging from 1 KB to 1 GB
    "PhysicalMemorySize":1.6e8,
    "testRandomSamplesAmt" : 10
}