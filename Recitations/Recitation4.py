def rec_mult(m,n):
    if n==0:
        return 0
    elif n >=1:
        return m + rec_mult(m, n-1)
    elif n <= -1:
        return -m + rec_mult(m, n+1)


def rec_fibonacci(n):
    if n ==0 or n ==1:
        return n
    else: return rec_fibonacci(n-1) + rec_fibonacci(n-2)

def iter_fib(n):
    if n ==0 or n ==1 :
        return n

    else:
        previous_fib = 0
        current_fib = 1
        for iteration in xrange(1, n):
            next_fib = current_fib + previous_fib
            previous_fib = current_fib
            current_fib = next_fib

        return current_fib

def rec_bisection_sqrt(x, epsilon=0.01, low = None, high = None):
    if low == None:
        low = 0.0
    if high == None:
        high = x
    midpoint = (low+high)/2.0
    if abs(midpoint**2-x) < epsilon or midpoint > x:
        return midpoint
    else:
        if midpoint**2 < x:
            return rec_bisection_sqrt(x, epsilon, midpoint, high)
        else:
            return rec_bisection_sqrt(x, epsilon, low, midpoint)
        
def close_enough(x, y, epsilon = 0.00001):
    """
        checks to see if 2 floating point numbers
        are equal within an error of epsilon
        """
    return abs(x-y) < epsilon

def find_prime(n):
    if n<= 3:
        if n ==2 or n ==3:
            return True
        else:
            return False
    #Otherwise
    else:
        #check divisors between 2 and sqrt(n)
        for divisor in range(2, int(n**.5)+1):
            #if divisor goes into n evenly, n isn't a prime
            if n%divisor == 0:
                return False
        #if none of the divisors go in evenly, n must be prime
        return True


