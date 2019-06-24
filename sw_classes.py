import warnings
from numpy import random

def rolldie(die):
    """
    takes an integer number, rolls a die with that number of sides
        if the highest number is rolled, roll another time and add the results together (exploding mechanic, can happend multiple times)
    """
    total = 0
    droll = die
    while droll == die:
        droll  =  int(die*random.rand(1)[0]) + 1
        total += droll

    return(total)

class gear():
    """
    represents generic kind of item. I was gonna user the __id__ attribute but decided against it! 
    """
    def __init__(self, name, weight, description=""):
        self.name           = name
        self.description    = weight
        self.weight         = description
        self.__id__         = 0
    def __str__(self):
        return(self.name)

class Trait():
    """
    Savage worlds trait. Both for skills and attributes
        + die is which die it is
        + past_d12 represents legendary levels of the trait
        + bonus is used to hold bonuses and detriments from edges and hindrances 

        * want to implement some distinguishing characteristic between attributes and skills! 
    """
    def __init__(self, value=0):
        self.past_d12 = 0 
        self.bonus = 0
        if int(value) not in [0, 4, 6, 8, 10, 12]: # these are the only polyhedral dice, SW doesn't use d20
            warnings.warn("Warning: {} is not an allowed die value. Setting to 0".format(value)) # if user is naughty, they deserve to be punished
            self.die = 4
        else:
            self.die = value
    
    # function used to force a trait to some value without using the 'improve / reduce' options. 
    # not supposed to be used really
    # added the assignment restriction 'cause otherwise it breaks the improve / reduce functions
    def __force__(self, value):
        if value not in [0,4,6,8,10,12]:
            raise Exception("Error: {} is not an allowed die value.".format(value))
        else:
            self.die = value 

    # python thingy that gives the result of print( Trait )
    def __str__(self):
        if self.die==0:
            return("d4+{}".format(self.bonus - 2))
        else:
            if self.past_d12!=0:
                return("d{}+{}".format(self.die, self.past_d12 + self.bonus) )
            else:
                return("d{}".format(self.die))

    # just rolls the die
    def roll(self):
        if self.die==0: # should no longer come up...
            return(rolldie(4) -2 + self.bonus )
        else:
            return(rolldie( self.die ) + self.bonus + self.past_d12)

    # move die up a step
    def improve(self):
        if self.die == 0:
            self.die    = 4
        elif self.die== 4:
            if self.bonus==0:
                self.die    = 6 # step up the die if the bonus is 0
            elif bonus<0:
                self.bonus+=1   # bring the onus closer to zero
            else: #wtf????
                warnings.warn("{} bonus at impossible value {}".format(self,self.bonus))
                self.bonus = 0
                self.die = 6 
        elif self.die== 6:
            self.die    = 8
        elif self.die== 8:
            self.die    = 10
        elif self.die==10:
            self.die    = 12
        elif self.die==12:
            self.past_d12 += 1
        else:
            warnings.warn("Unsure how to operate on die value {}".format(self.die))
        print("Trait improved to {}".format(self.__str__()))
    
    # move die down a step
    def reduce(self):
        if self.die==0:
            self.die = 4 # break away from the deprecated value
        elif self.die ==4: # removing support for die=0. Should never need that...
            self.bonus -= 1 # instead I'll reduce the bonus value by 1    
        elif self.die ==6:
            self.die = 4
        elif self.die ==8:
            self.die = 6
        elif self.die ==10:
            self.die = 8
        elif self.die==12: #improving from d12 increases legendary level (past_d12)
            if self.past_d12>0:
                self.past_d12 -= 1
            else:
                self.die = 10
                self.past_d12 = 0
        print("Trait reduced to {}".format(self.__str__()))


class Creature():
    '''
    implements a class that covers all creatures, humanoids, et cetera. Should cover all extras and wildcards
    '''
    def __init__(self, context={}):
        self.agility    = Trait(6) # implementation of Trait class above
        self.smarts     = Trait(6)
        self.spirit     = Trait(6)
        self.strength   = Trait(6)
        self.vigor      = Trait(6)
        self.pace       = 6. # floats! 
        self.toughness  = 0.
        self.parry      = 0.
        self.edges      = {} # dict of strings
        self.hindrances = {} # dict of strings
        self.gear       = [] # gear is a list so creature can have duplicates
        self.skills     = {} # dictionary of Traits
        self.special    = {} # dict of strings
        self.wild_card  = False
        self.animal     = True

        if not isinstance(context, dict):
            # the context object can be used to create a creature. Just pass keys for each of the objects
            #   if it's not a dictionary, just nullify it and move on
            warnings.warn("Warning: context object is not type {}, ignoring".format(context))
            context = None
        if context is not None:
            for key in context:
                if hasattr(self, key): # if that's a main attribute set it
                    # before grabbing the item from the dictionary, make sure it's the right data type! 
                    #   otherwise this could lead to everything breaking. 
                    if isinstance( context[key], type( getattr(self, key) )):      
                        setattr(self, key, Trait(context[key]))
                else:
                    # add it as a skill, I guess
                    #   but make sure that thing is a number! 
                    if isinstance(context[key], int) or isinstance(context[key], float):
                        self.skills[key] = Trait( context[key] )  #otherwise it's a skill?
        
        # if toughness and parry are not explicitly set
        # these formulas come from the SWADE core rulebook
        if self.toughness==0:
            self.toughness  = 2 + self.vigor.die/2 + self.vigor.past_d12
        if self.parry == 0:
            if 'fighting' in self.skills:
                self.parry  = 2 + self.skills['fighting'].die/2 + self.skills['fighting'].past_d12
            else:
                self.parry = 2 + 1
   
    def refresh(self):
        '''
        recalculates the parry and toughness
        '''
        if 'fighting' in self.skills:
            self.parry  = 2 + self.skills['fighting'].die/2 + self.skills['fighting'].past_d12
        else:
            self.parry = 2 + 1
        self.toughness = 2 + self.vigor.die/2 + self.vigor.past_d12

    # need to be careful with the next few of these
    #   can overwrite entries if not careful
    #   should raise error or warning if overwriting something

    def add_edge(self, key, description):
        self.edges[key] = description

    def add_hindrance(self, key, description):
        self.hindrances[key] = description

    def add_special(self, key, description):
        self.special[key] = description

    def add_skill(self, key, value):
        self.skills[key]= Trait(value)

    def give(self, thing):
        if isinstance(thing, gear):
            self.gear.append( gear )
    

    # just rolls the trait. never really uses this
    def roll(self, trait):
        if isinstance(trait, str):
            getattr(self, str).roll()
        elif isinstance(trait, Trait):
            trait.roll()
        else:
            print("I don't recognize {}, use a string or a trait type".format(type(trait)))
    
    # just prits out a list of what the creature has
    def has(self):
        for thing in self.gear:
            print(thing)

    def __str__(self):
        if self.wild_card:
            print("Is WILDCARD!")
        print("Attributes: ", end='')
        print("Agility {}, ".format(self.agility), end='')
        if self.animal:
            print("Smarts {} (A), ".format(self.smarts), end='')
        else:
            print("Smarts {}, ".format(self.smarts), end='')
        print("Spirit {}, ".format(self.spirit), end='')
        print("Strength {}, ".format(self.strength), end='')
        print("Vigor {}, ".format(self.vigor), end='')
        print("\nSkills: ",end='')
        for key in self.skills:
            print("{} {}, ".format(key, self.skills[key] ), end='')
        print("\nDerived: ", end='')
        print("Toughness {}, ".format(self.toughness), end='')
        print("Pace {}, ".format(self.pace), end='')
        print("Parry {}, ".format(self.parry), end='')
        if len(self.edges)>0:
            print("\nEdges: ")
            for key in self.edges:
                print("    -{}: {}".format(key, self.edges[key]))
        if len(self.hindrances)>0:
            print("\nHindrances: ")
            for key in self.hindrances:
                print("    -{}: {}".format(key, self.hindrances[key]))
        if len(self.special)>0:
            print("\nSpecial Abilities: ")
            for key in self.special:
                print("    -{}: {}".format(key, self.special[key]))
        return("")


