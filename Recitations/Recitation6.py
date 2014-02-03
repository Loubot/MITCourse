import math
import random
import pylab
def flipPlot(minExp, maxExp, numTrials):
    meanRatios = []
    meandDiffs = []
    ratiosSDs =[]
    diffsSDs = []
    xAxis = []

    for exp in range (minExp, maxExp+1):
        xAxis.append(2**exp)
##    print xAxis,'xax'
    for numFlips in xAxis:
        ratios = []
        diffs = []
        for t in range(numTrials):
            numHeads = 0
            for n in range(numFlips):
                if random.random() < .5:
                    numHeads += 1
##            print numHeads,'heads'
##            print numFlips,'fliops'
            numTails = numFlips - numHeads
##            print numTails,'tails'
            if numTails != 0:
                ratios.append(numHeads/ float(numTails))
            else:ratios.append(0)
            diffs.append(abs(numHeads - numTails))
        meanRatios.append(sum(ratios)/ numTrials)
        meandDiffs.append(sum(diffs)/numTrials)
        ratiosSDs.append(stdDev(ratios))
        diffsSDs.append(stdDev(diffs))
    pylab.plot(xAxis, meanRatios, 'bo')
    pylab.title('Mean Heads/Tails ratios'+str(numTrials)+' trials')
    pylab.xlabel('Number of flips')
    pylab.ylabel('Mean Heads/Tails')
    pylab.semilogx()
    pylab.show()

def stdDev(X):
    mean = sum(X)/float(len(X))
    tot = 0.0
    for x in X:
        tot += (x - mean)**2
    return (tot/len(X))**0.5
