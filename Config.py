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
    "PageSizes":[1e3, 1e4, 1e5, 1e6, 1e7], # In Bytes ranging from 1 KB to 1 GB
    "PageSizeColors":{1e3:'blue', 1e4:'green', 1e5:'red', 1e6:'cyan', 1e7:'magenta'},
    "PhysicalMemorySize":1.6e8,
    "testRandomSamplesAmt" : 1,
    "MaxFrameSize" : 10
}