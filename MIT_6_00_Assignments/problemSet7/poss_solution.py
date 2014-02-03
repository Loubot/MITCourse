

# 6.00 Problem Set 12
#
# Name: Joe Li
# Collaborators:
# Time: 7:00

import numpy
import random
import pylab

class NoChildException(Exception):
    """
    NoChildException is raised by the reproduce() method in the SimpleVirus
    and ResistantVirus classes to indicate that a virus particle does not
    reproduce. You can use NoChildException as is, you do not need to
    modify/add any code.
    """    

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
        """
        Stochastically determines whether this virus is cleared from the
        patient's body at a time step. 

        returns: Using a random number generator (random.random()), this method
        returns True with probability self.clearProb and otherwise returns
        False.
        """
        prob = random.random()
        if prob < self.clearProb:
            return True
        else:
            return False
    
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
        chance = self.maxBirthProb * (1 - popDensity)
        prob = random.random()
        if prob < chance:
            offspring = SimpleVirus(self.maxBirthProb, self.clearProb)
            return offspring
        raise NoChildException

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
        popDensity = float(len(health))/float(self.maxPop)
        assert 0 <= popDensity <=1,'wrong popDensity'
        for v in health:
        # append the offsprings the viruses reproduce to a list
            try:
                offsprings.append(v.reproduce(popDensity))
            except NoChildException: pass
        self.viruses = health + offsprings
        # the new viruses list is both list health and list offspring
        return len(self.viruses)

#
# PROBLEM 2
#

def problem2():
    """
    Run the simulation and plot the graph for problem 2 (no drugs are used,
    viruses do not have any drug resistance).    

    Instantiates a patient, runs a simulation for 300 timesteps, and plots the
    total virus population as a function of time.    
    """
    v = []
    pop = []
    for i in range(100):
        v.append(SimpleVirus(0.1, 0.05))
    poorguy = SimplePatient(v, 1000)
    for i in range(300):
        pop.append(poorguy.update())
    pylab.plot(pop)
    pylab.xlabel('Time')
    pylab.ylabel('Total virus population')
    pylab.title('Simulation of viruses reproduction without drug')
    pylab.show()
        
    
#
# PROBLEM 3
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
        assert type(maxBirthProb) == type(clearProb) == type(mutProb) == float, 'wrong input type'
        assert 0 <= maxBirthProb <= 1, 'maxBirthProb should be in [0,1]'
        assert 0 <= clearProb <= 1, 'clearProb should be in [0,1]'
        assert 0 <= mutProb <= 1, 'mutProb should be in [0,1]'
        self.maxBirthProb = maxBirthProb
        self.clearProb = clearProb
        self.resistances = resistances
        self.mutProb = mutProb
        
    def getResistance(self, drug):
        """
        Get the state of this virus particle's resistance to a drug. This method
        is called by getResistPop() in Patient to determine how many virus
        particles have resistance to a drug.        

        drug: the drug (a string).

        returns: True if this virus instance is resistant to the drug, False
        otherwise.
        """
        return self.resistances[drug]
        
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
            if not self.resistances[drug]:
                raise NoChildException
        chance = self.maxBirthProb * (1 - popDensity)
        prob = random.random()
        if prob < chance:
        # reproduce
            child_resistances = {}
            for drug in self.resistances:
                switch = random.random()
                if switch < self.mutProb:
                # mutate
                    child_resistances[drug] = not self.resistances[drug]
                else:
                # inherit
                    child_resistances[drug] = self.resistances[drug]
                offspring = ResistantVirus(self.maxBirthProb, self.clearProb, child_resistances, self.mutProb)
            return offspring
        raise NoChildException
            
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
        self.viruses = viruses
        self.maxPop = maxPop
        self.prescription = []
        
    def addPrescription(self, newDrug):
        """
        Administer a drug to this patient. After a prescription is added, the 
        drug acts on the virus population for all subsequent time steps. If the
        newDrug is already prescribed to this patient, the method has no effect.

        newDrug: The name of the drug to administer to the patient (a string).

        postcondition: list of drugs being administered to a patient is updated
        """
        if newDrug not in self.prescription:
            self.prescription.append(newDrug)

    def getPrescriptions(self):
        """
        Returns the drugs that are being administered to this patient.

        returns: The list of drug names (strings) being administered to this
        patient.
        """
        return self.prescription
        
    def getResistPop(self, drugResist):
        """
        Get the population of virus particles resistant to the drugs listed in 
        drugResist.        

        drugResist: Which drug resistances to include in the population (a list
        of strings - e.g. ['guttagonol'] or ['guttagonol', 'grimpex'])

        returns: the population of viruses (an integer) with resistances to all
        drugs in the drugResist list.
        """
        resistpop = 0
        for v in self.viruses:
            resist_all = True
            for drug in drugResist:
                if not v.resistances[drug]:
                    resist_all = False
            if resist_all == True:
                resistpop += 1
        return resistpop

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
          The list of drugs being administered should be accounted for in the
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
        popDensity = float(len(health))/float(self.maxPop)
        assert 0 <= popDensity <=1,'wrong popDensity'
        for v in health:
        # append the offsprings the viruses reproduce to a list
            try:
                offsprings.append(v.reproduce(popDensity, self.prescription))
            except NoChildException: pass
        self.viruses = health + offsprings
        # the new viruses list is both list health and list offspring
        return len(self.viruses)

#
# PROBLEM 4
#

def problem4():
    """
    Runs simulations and plots graphs for problem 4.

    Instantiates a patient, runs a simulation for 150 timesteps, adds
    guttagonol, and runs the simulation for an additional 150 timesteps.

    total virus population vs. time  and guttagonol-resistant virus population
    vs. time are plotted
    """
    v = []
    pop = []
    for i in range(100):
        v.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
    poorguy = Patient(v, 1000)
    poorguy.addPrescription('guttagonol')
    for i in range(150):
        pop.append(poorguy.update())
    pylab.plot(pop)
    pylab.xlabel('Time')
    pylab.ylabel('Total virus population')
    pylab.title('Simulation of viruses reproduction with drug')
    pylab.show()

#
# PROBLEM 5
#
        
def problem5():
    """
    Runs simulations and make histograms for problem 5.

    Runs multiple simulations to show the relationship between delayed treatment
    and patient outcome.

    Histograms of final total virus populations are displayed for delays of 300,
    150, 75, 0 timesteps (followed by an additional 150 timesteps of
    simulation).    
    """
    tot_trial = 100
    delay = [300, 150, 75, 0]
    for s in delay:
        trial = 0
        record = []
        for test in range(tot_trial):
            trial += 1
            v = []
            pop = []
            for i in range(100):
                v.append(ResistantVirus(0.1, 0.05, {'guttagonol':False}, 0.005))
            poorguy = Patient(v, 1000)
            # instiate patient
            for i in range(s):
                poorguy.update()
            poorguy.addPrescription('guttagonol')
            # take meds
            for i in range(150):
                poorguy.update()
            record.append(poorguy.getTotalPop())
            # record the final virus population
            print 'delay: '+str(s)+' timesteps, Trial: '+str(trial)
        cured = 0
        for result in record:
            if result <= 50:
                cured +=1
        curerate = str(float(cured) / len(record) * 100.0) + '%'
        pylab.figure()
        pylab.hist(record, bins=20, label='Cure rate: '+curerate, facecolor='g')
        pylab.legend()
        pylab.title('Simulation of viruses reproduction with drug delay '+str(s)+' timesteps')
        pylab.xlabel('Total virus population')
        pylab.ylabel('Number of patients')
    pylab.show()
    
#
# PROBLEM 6
#

def problem6():
    """
    Runs simulations and make histograms for problem 6.

    Runs multiple simulations to show the relationship between administration
    of multiple drugs and patient outcome.
    
    Histograms of final total virus populations are displayed for lag times of
    150, 75, 0 timesteps between adding drugs (followed by an additional 150
    timesteps of simulation).
    """
    delay = [300, 150, 75, 0]
    for s in delay:
        trial = 0
        record = []
        for test in range(30):
            trial += 1
            v = []
            pop = []
            for i in range(100):
                v.append(ResistantVirus(0.1, 0.05, {'guttagonol':False,'grimpex':False}, 0.005))
            poorguy = Patient(v, 1000)
            # initiate patient
            for i in range(150):
                poorguy.update()
            poorguy.addPrescription('guttagonol')
            # take meds 1
            for i in range(s):
                poorguy.update()
            poorguy.addPrescription('grimpex')
            # take meds 2
            for i in range(150):
                poorguy.update()
            record.append(poorguy.getTotalPop())
            # record the final virus population
            print 'delay: '+str(s)+' timesteps, Tiral: '+str(trial)
        cured = 0
        for result in record:
            if result <= 50:
                cured +=1
        curerate = str(float(cured) / len(record) * 100.0) + '%'
        pylab.figure()
        pylab.hist(record, bins=20, label='Cure rate: '+curerate, facecolor='g')
        pylab.legend()
        pylab.title('Simulation of viruses reproduction with delay '+str(s)+' timesteps between 2 drugs')
        pylab.xlabel('Total virus population')
        pylab.ylabel('Number of patients')
    pylab.show()

#
# PROBLEM 7
#
     
def problem7():
    """
    Run simulations and plot graphs examining the relationship between
    administration of multiple drugs and patient outcome.

    Plots of total and drug-resistant viruses vs. time are made for a
    simulation with a 300 time step delay between administering the 2 drugs and
    a simulations for which drugs are administered simultaneously.        
    """
    delay = [300, 0]
    t = {300:'Simulation of viruses population agianst time \n with a 300 time step delay between administering the 2 drugs',0:'Simulation of viruses population agianst time \n with drugs administered simultaneously'}
    for s in delay:
        v = []
        pop = []    # total virus population
        pop1 = []   # the population of guttagonol-resistant virus
        pop2 = []   # the population of grimpex- resistant virus
        popb = []   # the population of viruses that are resistant to both drugs
        for i in range(100):
            v.append(ResistantVirus(0.1, 0.05, {'guttagonol':False,'grimpex':False}, 0.005))
        poorguy = Patient(v, 1000)
        # initiate patient
        for i in range(150):
            pop.append(poorguy.update())
            p1 = 0
            p2 = 0
            pb = 0
            for v in poorguy.viruses:
                if v.resistances['guttagonol']: p1 += 1
                if v.resistances['grimpex']: p2 += 1
                if v.resistances['guttagonol'] and v.resistances['grimpex']: pb += 1
            pop1.append(p1)
            pop2.append(p2)
            popb.append(pb)
        poorguy.addPrescription('guttagonol')
        # take meds 1
        for i in range(s):
            pop.append(poorguy.update())
            p1 = 0
            p2 = 0
            pb = 0
            for v in poorguy.viruses:
                if v.resistances['guttagonol']: p1 += 1
                if v.resistances['grimpex']: p2 += 1
                if v.resistances['guttagonol'] and v.resistances['grimpex']: pb += 1
            pop1.append(p1)
            pop2.append(p2)
            popb.append(pb)
        poorguy.addPrescription('grimpex')
        # take meds 2
        for i in range(150):
            pop.append(poorguy.update())
            p1 = 0
            p2 = 0
            pb = 0
            for v in poorguy.viruses:
                if v.resistances['guttagonol']: p1 += 1
                if v.resistances['grimpex']: p2 += 1
                if v.resistances['guttagonol'] and v.resistances['grimpex']: pb += 1
            pop1.append(p1)
            pop2.append(p2)
            popb.append(pb)
        pylab.figure()
        pylab.plot(pop, label='total')
        pylab.plot(pop1, label='guttagonol-resistant virus')
        pylab.plot(pop2, label='grimpex- resistant virus')
        pylab.plot(popb, label='resistant to both drugs')
        pylab.legend(loc=0)
        pylab.xlabel('Time')
        pylab.ylabel('Virus population')
        pylab.title(t[s])
    pylab.show()
