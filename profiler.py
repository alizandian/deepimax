"""
This is a profiling class for check time or space complexities. It enables us to check 
performance of the project in various ways we want.

Written by Ali Zandian (alizandian@outlook.com) for University project, researching a better way to gauge unlimited trees.
A project at the university of Ashrafi Esfahani.
"""

import cProfile as Profiler
import pstats
import sys
import os

RESULTPATH = 'results'


class ProfilerData():
    def __init__(self, title, totalTime, totalCalls, algorithmCalls, algorithmTotalTime, algorithmRecursiveCalls, algorithmCumulativeTime,
                 neighborsCount, copyCounts, queueCounts, evaluatedCount, evaluatedTime):
        self.Title = title
        self.TotalTime = totalTime
        self.TotalCalls = totalCalls
        self.AlgorithmCalls = algorithmCalls
        self.AlgorithmTime = algorithmTotalTime
        self.AlgorithmRecursice = algorithmRecursiveCalls
        self.AlgorithmCum = algorithmCumulativeTime
        self.NeibursCount = neighborsCount
        self.CopyCount = copyCounts
        self.QueueCount = queueCounts
        self.EvaluatedCount = evaluatedCount
        self.EvaluatedTime = evaluatedTime

previousProfileData = None
MyProfiler = Profiler.Profile()

def Start():
    MyProfiler.enable(subcalls = True)

def Run(func):
    MyProfiler.runcall(func)

def End(diagrams = None, options = None):
    MyProfiler.disable()

def Print(onlyReturn, controllerTitle):
    global MyProfiler
    global previousProfileData

    # Printing to the file
    os.makedirs(RESULTPATH, exist_ok=True)
    file = open(RESULTPATH + "/Complete Log.txt","w+")
    stats = pstats.Stats(MyProfiler, stream = file)

    items = stats.stats.items()

    # Get the important data and calculate on them
    totalCalls = stats.total_calls
    totalTime = stats.total_tt

    # bot.py -> MiniMaxValue
    # bot.py -> Minimax
    algorithmCalls = 0
    algorithmRecursiveCalls = 0
    algorithmTotalTime = 0
    algorithmCumulativeTime = 0
    
    # entities.py -> EvaluationFunction
    evaluatedCounts = 0
    evaluatedTime = 0

    # entities.py -> Neighbors
    neighborsCount = 0

    # entities.py -> Copy
    copyCounts = 0

    # queue.py -> __init__
    queueCounts = 0

    for key, value in items: 
        keyString = str(key)
        if (('Minimax' in keyString and 'bot.py' in keyString) or
            ('MiniMaxValue' in keyString and 'bot.py' in keyString)):
                algorithmCalls += GetCallTime(value)
                algorithmRecursiveCalls += GetRecursiveTime(value)
                algorithmTotalTime += GetTotalTime(value)
                algorithmCumulativeTime += GetCumTime(value)

        if ('MinimaxAlphaBeta' in keyString and 'bot.py' in keyString):
                algorithmCalls += GetCallTime(value)
                algorithmRecursiveCalls += GetRecursiveTime(value)
                algorithmTotalTime += GetTotalTime(value)
                algorithmCumulativeTime += GetCumTime(value)

        if ('Expectimax' in keyString and 'bot.py' in keyString):
                algorithmCalls += GetCallTime(value)
                algorithmRecursiveCalls += GetRecursiveTime(value)
                algorithmTotalTime += GetTotalTime(value)
                algorithmCumulativeTime += GetCumTime(value)

        if('EvaluationFunction' in keyString and 'entities.py' in keyString):
            evaluatedCounts += GetCallTime(value)
            evaluatedTime += GetCumTime(value)

        if('Neighbors' in keyString and 'entities.py' in keyString):
            neighborsCount += GetCallTime(value)

        if('Copy' in keyString and 'entities.py' in keyString):
            queueCounts += GetCallTime(value)

        if('__init__' in keyString and 'queue.py' in keyString):
            copyCounts += GetCallTime(value)
    
    
    stats.sort_stats('cumulative').print_stats()
    file.close()

    profilerData = ProfilerData(controllerTitle, totalTime, totalCalls, algorithmCalls, algorithmTotalTime, algorithmRecursiveCalls, 
                                algorithmCumulativeTime, neighborsCount, copyCounts, queueCounts, evaluatedCounts, evaluatedTime)

    if(onlyReturn == False):
        PrintProfilerData(profilerData)
        # Printing to the console
        MyProfiler.print_stats('cumulative')

    previousProfileData = profilerData
    return profilerData

def PrintProfilerData(profilerData):
    print ("\nA bit more about the algorithm that just executed: ")
    print ("Total Time: " + str(profilerData.TotalTime))
    print ("Total Calls: " + str(profilerData.TotalCalls))
    print ("algorithm Time: " + str(profilerData.AlgorithmTime))
    print ("algorithm Calls: " + str(profilerData.AlgorithmCalls))
    print ("algorithm Cumulative Time: " + str(profilerData.AlgorithmCum))
    print ("algorithm Recursive Calls: " + str(profilerData.AlgorithmRecursice))
    print ("Evaluated Counts: " + str(profilerData.EvaluatedCount))
    print ("Evaluated Time: " + str(profilerData.EvaluatedTime))
    print ("Get Neighbors Calls: " + str(profilerData.NeibursCount))
    print ("Entities Created: " + str(profilerData.CopyCount))
    print ("Queues Created: " + str(profilerData.QueueCount))
    print ("")

def DumpProfilerInfo():
    global MyProfiler
    MyProfiler.clear()
    MyProfiler.disable()
    MyProfiler.enable()

def GetCallTime(value):
    return value[0]

def GetRecursiveTime(value):
    return value[1]
   
def GetTotalTime(value):
    return value[2]

def GetCumTime(value):
    return value[3]