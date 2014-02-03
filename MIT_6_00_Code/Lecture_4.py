##x = 0.5
##epsilon = 0.01
##low = 0.0 
##high = max(x, 1.0)
##ans = (high + low)/2.0
##while abs(ans**2 - x) >= epsilon:
##    #print 'ans =', ans, 'low =', low, 'high =', high
##    if ans**2 < x: 
##        low = ans 
##    else:
##         high = ans
##    ans = (high + low)/2.0
##print ans, 'is close to square root of', x
##--------------------------------

def withinEpsilon(x, y, epsilon):
    """x, y, epsilon floats. epsilon > 0.0
        returns true if x is within epsilon of y"""
    #return abs(x - y) <= epsilon

##print withinEpsilon(2,3,1)
##val = withinEpsilon(2,3,0.5)
##print val

##def f(x):
##    x = x + 1
##    print 'x =', x
##    return x
##
##
##x = 3
##z = f(x)
##print 'z =', z
##print 'x =', x

def f1(x):
    def g():
        x = 'abc'
    x = x + 1
    print 'x =', x
    
    g()
    
    return x
    assert False
x = 3
z = f1(x)

##def isEven(i):
##    """assumes i a positive int
##        returns True if i is even, otherwise False"""
##    return i%2 == 0
##
##def findRoot(pwr, val, epsilon):
##    """assumes pwr an int; val, epsilon floats
##        pwr and epsilon > 0
##        if it exists,
##            returns a value within epsilon of val**pwr
##            otherwise returns None"""
##    assert type(pwr) == int and type(val) == float\
##        and type(epsilon) == float
##    assert pwr > 0 and epsilon > 0
##    if isEven(pwr) and val < 0:
##        return None
##    low = -abs(val)
##    high = max(abs(val), 1.0)
##    ans = (high + low)/2.0
##while not withinEpsilon(ans**pwr, val, epsilon):
##    #print 'ans =', ans, 'low =', low, 'high =', high
##    if ans**pwr < val:
##        low = ans #
##    else:
##        high = ans
##    ans = (high + low)/2.0
##return ans



sumDigits = 0
for c in str(1952):
    sumDigits += int(c)
print sumDigits
