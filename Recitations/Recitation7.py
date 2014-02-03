import math
import pylab
import random
def frange(start, stop, step):
    l = []
    for i in range(int((stop-start)/step)):
        l.append(start+step*i)
    return l

def show_discrete_uniform(a,b, num_points):
    points = []
    for n in range(num_points):
        points.append(random.randint(a,b))

    pylab.figure()
    pylab.hist(points, 100, normed = True)
##    pylab.title('Discrete uniform distribution with ' +str(num_points)
    pylab.show()

##show(discrete_unifrom(1,100,1000000)
def show_continuous_uniform(a,b,num_points):
    points = []
    for n in range(num_points):
        points.append(random.uniform(a,b))

    pylab.figure()
    pylab.hist(points, 100)
    pylab.show()

##show_continuous_uniform(0,1.0,100000)

##def make_gaussian_plot(mu, sigma, num_points, show_ideal = True):
##    points = []
##    for n in range(num_points):
##        points.append(random.gauss(mu, sigma))
##
##    ideal_points_x = frange(mu-(sigma*3), mu+(sigma+3), 0.0001)
##    ideal_points_y = ()
##    for x in ideal_points_x:
##        y = 1.0 / math.sqrt(2.0 * math.pi * sigma **2) * math.exp(-(x-mu)**2/


def make_exponential_plot(lmbda, num_points):
    points = []
    for n in range(num_points):
        points.append(random.expovariate(lmbda))

    ideal_points_x = frange(0,10,0.0001)
    ideal_points_y = []
    for x in ideal_points_x:
        y = lmbda * math.exp(-lmbda * x)
        ideal_points_y.append(y)
    pylab.figure()
    pylab.hist(points, 100, normed=True)
    pylab.plot(ideal_points_x, ideal_points_y, c = 'r', lw=5)
    pylab.legend(['ideal curve', 'Random points'])
    

##make_exponential_plot(0.5, 10000)
##pylab.axis([0,10,0,1])
##
##make_exponential_plot(1,10000)
##pylab.axis([0,10,0,1])
##
##make_exponential_plot(1.5, 10000)
##pylab.axis([0,10,0,1])
##pylab.show()

def choose_door():
    return random.choice([1,2,3])

def play_monty_hall(num_trials = 1000):
    stay_wins = 0
    switch_wins = 0
    for trial in range(num_trials):
        prize_door = choose_door()
        player_door = choose_door()
        if prize_door == player_door:
            stay_wins += 1
        elif prize_door!= player_door:
            switch_wins += 1

    print 'Stay wins: ', stay_wins / float(num_trials)
    print 'Switch wins ', switch_wins/ float(num_trials)

##play_monty_hall()
def random_point(r):
    x = random.uniform(-r, r)
    y = random.uniform(-r, r)
    return(x,y)

def make_points(r, n):
    points = []
    for i in range(n):
        points.append(random_point(r))
    return points

def in_circle(r, point):
    x = point[0]
    y = point[1]
    return x**2 + y**2 <= r**2
def num_in_circle(r, points):
    count = 0
    for point in points:
        if in_circle(r, point):
            count += 1
    return count
def compute_pi(num_points, points = None):
    if points is None:
        points = make_points(1.0, num_points)
    in_circle = num_in_circle(1.0, points)
    return float(in_circle) / float(num_points) * 4.0

def run_trials(num_trials_per_point, num_points_list):
    results = []
    for num_points in num_points_list:
        print num_points
        for trial in range(num_trials_per_point):
            results.append((num_points, compute_pi(num_points)))
    return results
def plot_pi(trials, trials_results):
    num_points = []
    results = []
    for result in trials_results:
        num_points.append(result[0])
        results.append(result[1])

    pylab.figure()
    pylab.clf()
    pylab.scatter(num_points, results, c = 'r')
    pylab.plot(trials, [math.pi for trial in trials], c = 'b')
    pylab.xlabel('Number of points')
    pylab.ylabel('PI')
    pylab.title('PI vs the number of points')
    pylab.show()

##num_trials_per_point = 50
##num_points_list = range(10, 10000, 1000)
##trials_results = run_trials(num_trials_per_point, num_points_list)
##plot_pi(num_points_list, trials_results)

def plot_pi_scatter(r, n):
    points = make_points(1.0,n)
    pi_est = compute_pi(n, points)

    square_points_x = []
    square_points_y = []

    circle_points_x = []
    circle_points_y = []

    for point in points:
        if in_circle(r,point):
            circle_points_x.append(point[0])
            circle_points_y.append(point[1])
        else:
            square_points_x.append(point[0])
            square_points_y.append(point[1])

    pylab.figure()
    pylab.clf()
    pylab.scatter(square_points_x, square_points_y, c='r')
    pylab.scatter(circle_points_x, circle_points_y, c='b')
    pylab.axis([-1.5, 1.5,-1.5,1.5])
    pylab.text(-1.4,-1.4,'Pi is estimated to be '+ str(pi_est))
    pylab.show()

plot_pi_scatter(1,10)
plot_pi_scatter(1,100)
plot_pi_scatter(1,1000)
plot_pi_scatter(1,10000)


