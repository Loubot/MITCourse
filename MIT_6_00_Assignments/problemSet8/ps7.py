#-------------------------------------------------------------------------------
# Name:        ps7
# Purpose:
#
# Author:      angell
#
# Created:     24/03/2013
# Copyright:   (c) angell 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

# Problem Set 7: Simulating the Spread of Disease and Virus Population Dynamics
# Name:
# Collaborators:
# Time:

import numpy
import random
import pylab

'''
Begin helper code
'''

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """

'''
End helper code
'''

#
# PROBLEM 1
#
class SimpleVirus(object):

    """
    Representation of a simple virus (does not model drug effects/resistance).
    """
    def __init__(self, maxBirthProb, clearProb):

        """
        Initialize a SimpleVirus instance, saves all parameters as attributes
        of the instance.
        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).
        """

        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb

    def doesClear(self):

        """ Stochastically determines whether this virus particle is cleared from the
        patient's body at a time step.
        returns: True with probability self.clearProb and otherwise returns
        False.
        """

        rand = random.random()
        return rand < self.clearProb


    def reproduce(self, popDensity):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the SimplePatient and
        Patient classes. The virus particle reproduces with probability
        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring SimpleVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population.

        returns: a new instance of the SimpleVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        rand = random.random()

        if rand < self.maxBirthProb* (1 - popDensity):
            newVirus = SimpleVirus(self.maxBirthProb, self.clearProb)
            return newVirus
        else:
            raise NoChildException

    def __str__(self):
        return ('This is a virus with %0.2f birth probability clear probabilty of %0.2f')%(self.maxBirthProb, self.clearProb)


class SimplePatient(object):

    """
    Representation of a simplified patient. The patient does not take any drugs
    and his/her virus populations have no drug resistance.
    """

    def __init__(self, viruses, maxPop):

        """

        Initialization function, saves the viruses and maxPop parameters as
        attributes.

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """

        self.viruses = viruses
        self.maxPop = maxPop


    def getTotalPop(self):

        """
        Gets the current total virus population.
        returns: The total virus population (an integer)
        """

        return len(self.viruses)


    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute the following steps in this order:

        - Determine whether each virus particle survives and updates the list
        of virus particles accordingly.
        - The current population density is calculated. This population density
          value is used until the next call to update()
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.

        returns: The total virus population at the end of the update (an
        integer)
        """

        virusList = []
        for virus in self.viruses:
            if not virus.doesClear():
                virusList.append(virus)

        popDensity = float(len(virusList)) / float(self.maxPop)
##        print popDensity,'popdense'
        self.viruses = virusList
        childList = []
        for parent in self.viruses:
            childList.append(parent)
            try:
                child = parent.reproduce(popDensity)
                childList.append(child)
            except NoChildException:
                continue

        self.viruses = childList
        return len(self.viruses)

    def __str__(self):
        return ('This patient has %d virus instanses and a maxpop of %d')%(len(self.viruses), self.maxPop)
#
# PROBLEM 2
#
def simulationWithoutDrug(numViruses, maxPop, maxBirthProb, clearProb, numTrials):

    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).
    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.
    """
    sumResults = None
    timeRange = range(0,300)
    for i in range(0, numTrials):
        resultList = (runSimulation(numViruses,maxBirthProb,clearProb,maxPop,timeRange))

        if sumResults == None:
            sumResults = resultList
        else:
            for j in range (0, len(resultList)):
                sumResults[j] += resultList[j]

    for i in range(0, len(sumResults)):
        sumResults[i] /= numTrials

    pylab.plot(timeRange, sumResults, label = 'SimpleVirus')
    pylab.xlabel('Time step')
    pylab.ylabel('# viruses')
    pylab.title('Simple virus simulation')
    pylab.legend(loc = 'best')
    pylab.show()

def runSimulation(numViruses, maxBirthProb,clearProb,maxPop,timeRange):
    virusList = []
    virusRange = range(0, numViruses)
    for i in virusRange:
        virus = SimpleVirus(maxBirthProb, clearProb)
        virusList.append(virus)
    patient = SimplePatient(virusList, maxPop)
    resultList = []

    for hour in timeRange:
        resultList.append(patient.update())


    return resultList
