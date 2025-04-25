lazyConfig = {
    "NumberOfPrograms":100,
    "AverageArrivalTime":500,
    "ProgramMemorySizes": {
        "Small" : {"Max":1e4, "Min":1e3},
        "Medium" : {"Max":1e6, "Min":1e5},
        "Large" : {"Max":50e7, "Min":1e7}
    },
    "ProgramInstructionSizes": {
        "Small" : {"Max":100, "Min":10},
        "Medium" : {"Max":500, "Min":100},
        "Large" : {"Max":1000, "Min":500}
    },
    "PageSizes":[1e3, 1e4, 1e5, 1e6, 1e7, 1e8, 1e9], # In Bytes ranging from 1 KB to 1 GB
    "PageSizeColors":{1e3:'blue', 1e4:'green', 1e5:'red', 1e6:'cyan', 1e7:'magenta', 1e8:'orange', 1e9:'purple'},
    #"PageSizeColors":{1e3:'blue', 1e4:'green', 1e5:'red', 1e6:'cyan', 1e7:'magenta'},
    "PhysicalMemorySize":16e9,
    "testRandomSamplesAmt" : 20,
    "MaxFrameSize" : 10
}