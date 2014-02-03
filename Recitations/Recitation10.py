#######Example 1 Recursive fibonacci
import pylab, math
runs =0
def fib(n):
    global runs
    runs += 1

    if n == 0 or n ==1:
        return n
    else: return fib(n-1)+fib(n-2)

##x = range(30)
##steps = []
##
##for n in x:
##    runs = 0
##    print "fib (", n, ") is ", fib(n), " takes ", runs, " steps"
##    steps.append(runs)

##pylab.plot(x, [2**i for i in x],label = 'Exponential function')
##pylab.plot(x, [i**2 for i in x], label = 'Quadratic function')
##pylab.plot(x, [((1+math.sqrt(5))/2)**i for i in x], label = 'Tight bound')
##pylab.plot(x, steps, 'bo', label = 'Steps')
##pylab.semilogy()
##pylab.legend()
##pylab.show()

def dpFib(n,memo = None):
    if memo == None:
        memo = {0:0, 1:1}

    global runs
    runs +=1

    if n not in memo:
        memo[n] = dpFib(n-1, memo) + dpFib(n-2, memo)

    return memo[n]

##x = range(30)
##steps = []
##for n in x:
##    runs =0
##    print "Fib (", n, ") is ", dpFib(n), " takes ", runs, " steps"
##    steps.append(runs)
    
##pylab.plot(x, [2**i for i in x], label = "Exponential function")
##pylab.plot(x, [i**2 for i in x], label = "Quadratice Function")
##pylab.plot(x, [2*i -1 for i in x], label = "2*x-1")
##pylab.plot(x, steps, 'bo', label = "Steps")
##pylab.semilogy()
##pylab.legend()
##pylab.show()
##pylab.show


def numRobotPaths(n,m):
    ##Robot is on n xm grid, Can only move right or down
    ##It starts in square (0,0). How many paths are there
    ##from (0,0) to (n,m)?

    global runs
    runs +=1

    if n ==1 or m ==1:
        return 1
    return numRobotPaths(n-1, m) + numRobotPaths(n, m-1)
##runs = 0
##rows = 14
##cols = 14
##print numRobotPaths(rows, cols), runs


def dpNumRobotPaths(n,m,memo = None):
    global runs

    if memo is None:
        memo = {}

    if (n,m) not in memo:
        runs += 1
        if n == 1 or m ==1:
            memo[(n,m)] = 1
        else:
            memo[(n,m)] = dpNumRobotPaths(n-1,m,memo)+dpNumRobotPaths(n,m-1,memo)

        memo[(m,n)] = memo[(n,m)]
    return memo[(n,m)]

##rows =14
##cols =14
##print dpNumRobotPaths(rows, cols), runs
                                           
def dpNumRobotPathsIter(n,m):
    global runs

    paths = [[1] *m] #top row of matrix
    for row in xrange(n):
        paths.append([1] + [0] * (m-1))

    for row in xrange(1,n):
        for col in xrange(1,m):
            paths[row][col] = paths[row-1][col] + paths[row][col-1]
            runs +=1

    return paths[n-1][m-1]

rows = 1400
cols = 1400

runs = 0
##print dpNumRobotPathsIter(rows, cols),runs

s = (1,5,10,25,27)

def countChange(total, coins):
    global runs
    runs +=1

    if total == 0: #base case, total has reached so we have found
                   #one way to make this total using coins
        return 1
    if total <0:    #base case, total is less than 0, the last coin we
                    #tried was too big, so this is a dead end
        return 0
    if len(coins) == 0 and total >= 1:#if we have no more coins to use and there
                                      #is still total amount left, then we're
                                      #hit a dead end
        return 0

    num_ways_without_last_coin = countChange(total, coins[:-1])
    num_ways_using_last_coin = countChange(total - coins[-1], coins)

    return num_ways_without_last_coin+ num_ways_using_last_coin

##print "Using coins ", s
##for tot in [5,10,15,20,25,27,100]:
##    runs = 0
##    print "We have ", countChange(tot, s), " ways to get total " , tot, \
##          " and takes ", runs, "steps"

s = [1,5,10,25,27] 

def dpCountChange(total, coins, memo = None):
    if memo == None:
        memo = {}

    global runs
    runs +=1

    if total == 0:
        return 1
    if total < 0:
        return 0
    if len(coins) == 0 and total >=1:
        return 0

    if (total, coins[-1]) not in memo:
        num_ways_without_last_coin = dpCountChange(total, coins[:-1], memo)
        num_ways_using_last_coin = dpCountChange(total - coins[-1], coins, memo)
        memo[(total, coins[-1])] = num_ways_without_last_coin+num_ways_using_last_coin

    return memo[(total, coins[-1])]

print 'Using coins ',s
for tot in [5,10,15,20,25,27,100]:
    runs = 0
    print "We have ", dpCountChange(tot, s), " ways to get total ", tot,\
          " and takes ", runs , " steps"
