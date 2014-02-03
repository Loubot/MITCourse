# 6.00 Problem Set 8
#
# Name:Louis
# Collaborators:
# Time:



import numpy
import random
import pylab
from ps7 import *

#
# PROBLEM 1
#
class ResistantVirus(SimpleVirus):

    """
    Representation of a virus which can have drug resistance.
    """

    def __init__(self, maxBirthProb, clearProb, resistances, mutProb):

        """

        Initialize a ResistantVirus instance, saves all parameters as attributes
        of the instance.

        maxBirthProb: Maximum reproduction probability (a float between 0-1)
        clearProb: Maximum clearance probability (a float between 0-1).

        resistances: A dictionary of drug names (strings) mapping to the state
        of this virus particle's resistance (either True or False) to each drug.
        e.g. {'guttagonol':False, 'grimpex',False}, means that this virus
        particle is resistant to neither guttagonol nor grimpex.

        mutProb: Mutation probability for this virus particle (a float). This is
        the probability of the offspring acquiring or losing resistance to a drug.

        """


        SimpleVirus.__init__(self,maxBirthProb, clearProb)
        self.resistances = resistances
        self.mutProb = mutProb



    def isResistantTo(self, drug):

        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.

        drug: The drug (a string)
        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """

        if drug in self.resistances:
            return self.resistances[drug]

        else: return False




    def reproduce(self, popDensity, activeDrugs):

        """
        Stochastically determines whether this virus particle reproduces at a
        time step. Called by the update() method in the Patient class.

        If the virus particle is not resistant to any drug in activeDrugs,
        then it does not reproduce. Otherwise, the virus particle reproduces
        with probability:

        self.maxBirthProb * (1 - popDensity).

        If this virus particle reproduces, then reproduce() creates and returns
        the instance of the offspring ResistantVirus (which has the same
        maxBirthProb and clearProb values as its parent).

        For each drug resistance trait of the virus (i.e. each key of
        self.resistances), the offspring has probability 1-mutProb of
        inheriting that resistance trait from the parent, and probability
        mutProb of switching that resistance trait in the offspring.

        For example, if a virus particle is resistant to guttagonol but not
        grimpex, and `self.mutProb` is 0.1, then there is a 10% chance that
        that the offspring will lose resistance to guttagonol and a 90%
        chance that the offspring will be resistant to guttagonol.
        There is also a 10% chance that the offspring will gain resistance to
        grimpex and a 90% chance that the offspring will not be resistant to
        grimpex.

        popDensity: the population density (a float), defined as the current
        virus population divided by the maximum population

        activeDrugs: a list of the drug names acting on this virus particle
        (a list of strings).

        returns: a new instance of the ResistantVirus class representing the
        offspring of this virus particle. The child should have the same
        maxBirthProb and clearProb values as this virus. Raises a
        NoChildException if this virus particle does not reproduce.
        """

        for drug in activeDrugs:
            if not self.isResistantTo(drug):
                raise NoChildException()

        prob = random.random()
        if prob < self.maxBirthProb * (1 - popDensity):

            childResistances = {}
            for drug in self.resistances.keys():
                resistanceProb = random.random()
                if resistanceProb < self.mutProb:
                    childResistances[drug] = not self.resistances[drug]
                else:
                    childResistances[drug] = self.resistances[drug]

            child = ResistantVirus(self.maxBirthProb, self.clearProb, childResistances,
                                   self.mutProb)
            return child
        else:
            raise NoChildException()



    def __str__(self):
        print self.resistances


class Patient(SimplePatient):

    """
    Representation of a patient. The patient is able to take drugs and his/her
    virus population can acquire resistance to the drugs he/she takes.
    """

    def __init__(self, viruses, maxPop):
        """
        Initialization function, saves the viruses and maxPop parameters as
        attributes. Also initializes the list of drugs being administered
        (which should initially include no drugs).

        viruses: the list representing the virus population (a list of
        SimpleVirus instances)

        maxPop: the  maximum virus population for this patient (an integer)
        """
        self.drugs = []
        self.viruses = viruses
        self.maxPop = maxPop


    def addPrescription(self, newDrug):

        """
        Administer a drug to this patient. After a prescription is added, the
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.drugs:
            self.drugs.append(newDrug)


    def getPrescriptions(self):

        """
        Returns the drugs that are being administered to this patient.
        returns: The list of drug names (strings) being administered to this
        patient.
        """

        return self.drugs


    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in
        drugResist.

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistPop = 0

        for virus in self.viruses:
            virusCheck = True
            for drug in drugResist:
                if not virus.isResistantTo(drug):
                    virusCheck = False
            if virusCheck == True:
                resistPop += 1

        return resistPop




    def update(self):

        """
        Update the state of the virus population in this patient for a single
        time step. update() should execute these actions in order:

        - Determine whether each virus particle survives and update the list of
          virus particles accordingly
        - The current population density is calculated. This population density
          value is used until the next call to update().
        - Determine whether each virus particle should reproduce and add
          offspring virus particles to the list of viruses in this patient.
          The listof drugs being administered should be accounted for in the
          determination of whether each virus particle reproduces.

        returns: the total virus population at the end of the update (an
        integer)
        """
        health = []
        # the list of viruses isn't cleared
        offsprings = []
        for v in self.viruses:
        # append the virus which is able to reproduce to health
            if not v.doesClear():
                health.append(v)
        popDensity = float(len(health))/self.maxPop
        assert 0 <= popDensity <=1,'wrong popDensity'
        for v in health:
        # append the offsprings the viruses reproduce to a list
            try:
                offsprings.append(v.reproduce(popDensity, self.drugs))
            except NoChildException: pass
        self.viruses = health + offsprings
        # the new viruses list is both list health and list offspring
        return len(self.viruses)
#
# PROBLEM 2
#

def simulationWithDrug():

    """

    Runs simulations and plots graphs for problem 4.
    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.
    total virus population vs. time and guttagonol-resistant virus population
    vs. time are plotted
    """
    virusList = []
    resulList = []
    timeRange = range(0, 300)
    for i in range(0, 100):
        virusList.append(ResistantVirus(.1,.05,{'guttagonol':False},0.005))
    patient = Patient(virusList, 1000)
    for hour in timeRange:
        if hour == 150:
            patient.addPrescription('guttagonol')
        resulList.append(patient.update())
    pylab.plot(resulList)
    pylab.show()


##simulationWithDrug()
#
# PROBLEM 3
#

def simulationDelayedTreatment():

    """
    Runs simulations and make histograms for problem 5.
    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.
    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).
    """
    viruses = 100
    maxPop = 1000
    maxBirthProb = .1
    clearProb = .05
    resistances = {'guttagonol':False}
    presciptions = 'guttagonol'
    mutProb = .005
    numTrials = 30
    delayList = [300, 150, 75, 0]
    plotNum = 1
    for delay in delayList:
        histList = []

        for x in range(0, numTrials):
            virusList = []
            for i in range(0, viruses):
                virusList.append(ResistantVirus(maxBirthProb, clearProb, resistances, mutProb))

            patient = Patient(virusList, maxPop)
            timeRange = range(0, delay + 150)
            for hour in timeRange:
                if hour == delay:
                    patient.addPrescription(presciptions)
                patient.update()

            histList.append(patient.getTotalPop())
        pylab.subplot(2,2,plotNum)
        pylab.title('Delay: '+ str(delay))
        pylab.xlabel('Level of virus present')
        pylab.ylabel('Number of trials')
        pylab.hist(histList, bins = 12, range = (0, 600))
        plotNum += 1
    pylab.show()
#
# PROBLEM 4
#

def simulationTwoDrugsDelayedTreatment():

    """
    Runs simulations and make histograms for problem 6.
    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.

    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    numTrials = range(0, 30)
    delayList = [300, 150, 75, 0]
    numPlot = 1
    for delay in delayList:
        histList = []
        for trial in numTrials:
            virusList = []
            for i in range(0, 100):
                virusList.append(ResistantVirus(.1, .05,{'guttagonol':False, 'grimpex':False}, .005))

            patient = Patient(virusList, 1000)

            for hour in range(0, delay + 300):
                if hour == 150:
                    patient.addPrescription('guttagonol')
                if hour == 150 + delay:
                    patient.addPrescription('grimpex')
                patient.update()
            histList.append(patient.getTotalPop())


        pylab.subplot(2,2, numPlot)

        pylab.hist(histList, bins = 12)
        numPlot += 1
    pylab.show()
#
# PROBLEM 5
#

def simulationTwoDrugsVirusPopulations():

    """

    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.
    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.

    """
    numTrials = range (0, 30)
    timeRange = range(0, 600)
    avgTotal = None
    avgGuttResist = None
    avgGrimpResist = None
    avgBothResist =None
    for trial in numTrials:
        sim1Total = []
        sim1GuttResist =[]
        sim1GrimpResist = []
        sim1BothResist = []
        virusList = []
        for i in range(0, 100):
            virusList.append(ResistantVirus(.1, .05,{'guttagonol':False, 'grimpex':False}, .005))
        patient = Patient(virusList, 1000)

        for hour in timeRange:
            if hour == 150:
                patient.addPrescription('guttagonol')
            if hour == 450:
                patient.addPrescription('grimpex')

            patient.update()
            sim1Total.append(patient.getTotalPop())
            sim1GuttResist.append(patient.getResistPop(['guttagonol']))
            sim1GrimpResist.append(patient.getResistPop(['grimpex']))
            sim1BothResist.append(patient.getResistPop(['guttagonol','grimpex']))
        for hour in timeRange:
            if avgTotal == None:
                avgTotal = sim1Total
            else:
                avgTotal[hour] += sim1Total[hour]
            if avgGuttResist == None:
                avgGuttResist = sim1GuttResist
            else:
                avgGuttResist[hour] += sim1GuttResist[hour]
            if avgGrimpResist == None:
                avgGrimpResist = sim1GrimpResist
            else:
                avgGrimpResist[hour] += sim1GrimpResist[hour]
            if avgBothResist ==None:
                avgBothResist = sim1BothResist
            else:
                avgBothResist[hour] += sim1BothResist[hour]


    for hour in timeRange:
        avgBothResist[hour] /= float(len(numTrials))
        avgGrimpResist[hour]/= float(len(numTrials))
        avgGuttResist[hour]/= float(len(numTrials))
        avgTotal[hour]/= float(len(numTrials))
    pylab.figure()
    pylab.title('Guttagonol added at 150 and Grimpex at 450')
    pylab.plot(avgTotal, label='Total')
    pylab.plot(avgGuttResist, label='Guttagonol resistant')
    pylab.plot(avgGrimpResist, label='Grimpex resistant')
    pylab.plot(avgBothResist, label='Resistant to both drugs')
    pylab.legend(loc=0)

# sim 2
    timeRange = range(0, 300)
    for trial in numTrials:
        sim1Total = []
        sim1GuttResist =[]
        sim1GrimpResist = []
        sim1BothResist = []
        virusList = []
        for i in range(0, 100):
            virusList.append(ResistantVirus(.1, .05,{'guttagonol':False, 'grimpex':False}, .005))
        patient = Patient(virusList, 1000)
        for hour in timeRange:
            if hour == 150:
                patient.addPrescription('guttagonol')
                patient.addPrescription('grimpex')
            patient.update()
            sim1Total.append(patient.getTotalPop())
            sim1GuttResist.append(patient.getResistPop(['guttagonol']))
            sim1GrimpResist.append(patient.getResistPop(['grimpex']))
            sim1BothResist.append(patient.getResistPop(['guttagonol','grimpex']))
        for hour in timeRange:
            if avgTotal == None:
                avgTotal = sim1Total
            else:
                avgTotal[hour] += sim1Total[hour]
            if avgGuttResist == None:
                avgGuttResist = sim1GuttResist
            else:
                avgGuttResist[hour] += sim1GuttResist[hour]
            if avgGrimpResist == None:
                avgGrimpResist = sim1GrimpResist
            else:
                avgGrimpResist[hour] += sim1GrimpResist[hour]
            if avgBothResist ==None:
                avgBothResist = sim1BothResist
            else:
                avgBothResist[hour] += sim1BothResist[hour]



        for hour in timeRange:
            avgBothResist[hour] /= float(len(numTrials))
            avgGrimpResist[hour]/= float(len(numTrials))
            avgGuttResist[hour]/= float(len(numTrials))
            avgTotal[hour]/= float(len(numTrials))



    pylab.figure()
    pylab.title('Guttagonol and Grimpex added at 150')
    pylab.plot(sim1Total, label='Total')
    pylab.plot(sim1GuttResist, label='Guttagonol resistant')
    pylab.plot(sim1GrimpResist, label='Grimpex resistant')
    pylab.plot(sim1BothResist, label='Resistant to both drugs')
    pylab.legend(loc=0)
    pylab.show()


