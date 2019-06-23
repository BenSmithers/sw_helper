import warnings
from numpy import random

def rolldie(die):
    total = 0
    droll = die
    while droll == die:
        droll  =  int(die*random.rand(1)[0]) + 1
        total += droll

    return(total)

class gear():
    def __init__(self, name, weight, description=""):
        self.name           = name
        self.description    = weight
        self.weight         = description
        self.__id__         = 0
    def __str__(self):
        return(self.name)

class Trait():
    def __init__(self, value=0):
        self.past_d12 = 0
        self.bonus = 0
        if int(value) not in [0, 4, 6, 8, 10, 12]:
            warnings.warn("Warning: {} is not an allowed die value. Setting to 0".format(value))
            self.die = 0
        else:
            self.die = value
    
    def __force__(self, value):
        if value not in [0,4,6,8,10,12]:
            raise Exception("Error: {} is not an allowed die value.".format(value))
        else:
            self.die = value 

    def __str__(self):
        if self.die==0:
            return("d4-2")
        else:
            if self.past_d12!=0:
                return("d{}+{}".format(self.die, self.past_d12) )
            else:
                return("d{}".format(self.die))


    def roll(self):
        if self.die==0:
            return(rolldie(4) -2 + self.bonus )
        else:
            return(rolldie( self.die ) + self.bonus + self.past_d12)
    def improve(self):
        if self.die == 0:
            self.die    = 4
        elif self.die== 4:
            self.die    = 6
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
    def reduce(self):
        if self.die==0:
            self.die = 0
        elif self.die ==4:
            self.die = 0
        elif self.die ==6:
            self.die = 4
        elif self.die ==8:
            self.die = 6
        elif self.die ==10:
            self.die = 8
        elif self.die==12:
            if self.past_d12>0:
                self.past_d12 -= 1
            else:
                self.die = 10
                self.past_d12 = 0
        print("Trait reduced to {}".format(self.__str__()))


class Creature():
    def __init__(self, context={}):
        self.agility    = Trait(6)
        self.smarts     = Trait(6)
        self.spirit     = Trait(6)
        self.strength   = Trait(6)
        self.vigor      = Trait(6)
        self.pace       = 6
        self.toughness  = None
        self.parry      = None
        self.edges      = {}
        self.hindrances = {}
        self.gear       = []
        self.skills     = {}
        self.special    = {}
        self.wild_card  = False
        self.animal     = True

        if not isinstance(context, dict):
            warnings.warn("Warning: context object is not type {}, ignoring".format(context))
            context = None
        if context is not None:
            for key in context:
                if hasattr(self, key): # if that's a main attribute set it
                    setattr(self, key, Trait(context[key]))
                else:
                    self.skills[key] = Trait( context[key] )  #otherwise it's a skill?
        
        # if toughness and parry are not explicitly set
        if self.toughness is None:
            self.toughness  = 2 + self.vigor.die/2 + self.vigor.past_d12
        if self.parry is None:
            if 'fighting' in self.skills:
                self.parry  = 2 + self.skills['fighting'].die/2 + self.skills['fighting'].past_d12
            else:
                self.parry = 2 + 1
    
    def refresh(self):
        if 'fighting' in self.skills:
            self.parry  = 2 + self.skills['fighting'].die/2 + self.skills['fighting'].past_d12
        else:
            self.parry = 2 + 1
        self.toughness = 2 + self.vigor.die/2 + self.vigor.past_d12

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
    

    def roll(self, trait):
        if isinstance(trait, str):
            getattr(self, str).roll()
        elif isinstance(trait, Trait):
            trait.roll()
        else:
            print("I don't recognize {}, use a string or a trait type".format(type(trait)))
    
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


