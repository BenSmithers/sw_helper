#!/usr/bin/python3.6
import pickle
import numpy as np
import sw_classes as sw
import os

creatures   = {}
items       = {}

def load():
    """
    loads in the database pickle
    """

    if os.path.isfile("database"):
        load_file = open('database', 'rb')
    else:
        print("no database file found! Creating new one, I guess")
        return()

    global creatures
    global items
    temp_pickle = pickle.load( load_file )
    creatures   = temp_pickle['creatures']
    items       = temp_pickle['items']
    load_file.close()
    print("Loaded...")
    return()


def save():
    global creatures
    global items
    load_file = open('database','wb')
    pickle.dump( {'creatures': creatures, 'items': items}, load_file, -1)
    load_file.close()


def edit_creature(key):
    """
    Used to edit the creature object at that key.
    Modify traits, add edges and hindrances

    """
    global creatures
    global items

    if key not in creatures:
        print("{} not in creatures".format(key))
        return()
    user_input = ""
    error_line = ""
    accepted = ['improve', 'reduce','give','skill', 'edge', 'hindrance', 'special', 'force', 'remove', 'wild_card', 'animal', 'help'] #check user inputs against this list
    printHelp= False
    while user_input != "done":
        # clear the screen, display any error from last loop, wait for user input
        os.system('cls' if os.name=='nt' else 'clear')
        print("Editing '{}'. Type 'done' when done modifying".format(key))
        if error_line!="":
            print("")
            print(error_line)
        print("")
        print(creatures[key])
        print("")
        if printHelp:
            print("SWADE Helper Creature Editor")
            print("")
            print("To adjust a <trait> by <n_steps> die steps. The number of steps is an optional argument!")
            print("")
            print("    improve <trait> <n_steps>")
            print("    reduce  <trait> <n_steps>")
            print("")
            print("Can be used on attributes and skills!")
            print("")
            print("Adding skills:")
            print("    skill <name> <die>")
            print("")
            print("Removing unwanted things")
            print("'remove <what> <name>'")
            print("    what = 'edges', 'skills', 'hindrances', 'items', 'special'")
            print("    name = the name of the thing above")
            print("")
            print("'edge <name> <desc>'     - give the creature and edge. Provide name and description")
            print("force <what> <number>'   - sets the number value <what> to <number>")
            print("'hindrance <name> <desc>'- same as above, but hindrances")
            print("'special <name> <desc>'  - same as above, but for special abilities")
            print("'animal'                 - toggles whether or not the creature is of animal intelligence")
            print("'wild_card'              - switches between wild card and extra")
            print("'give <item>'            - gives the creature an item from the item list. WIP!")
            print("")
        user_input = input("sw helper ... C$ ")
        printHelp = False
        if user_input=="":
            continue
        # may also want to exit on inputs like 'exit' or 'quit'
        if user_input=="done": # if they want out, END IT!
            break

        user_input = user_input.split()
        error_line = ""

        # raise/lower/give/add_skill/

    
        # only try doing things if we recognize the first word! 
        # go through a list of possible commands, each one has different args and catches!
        if user_input[0]=='improve':
            # couple checks to either a) break out of this command, b) prepare to do multple loops, or c) just do one loop
            if len(user_input)<2:
                error_line = "missing an argument"
                continue
            elif len(user_input)==3:
                try:
                    nLoops = int(user_input[2])
                except ValueError:
                    nLoops = 1
                    error_line = "I couldn't cast {} as an int! Improving one step".format(user_input[2])
            else:
                nLoops = 1
            
            try:
                if user_input[1] in creatures[key].skills:
                    # if it's a skill snag the entry in the skill list and improve it
                    for i in range(nLoops):
                        creatures[key].skills[user_input[1]].improve()
                else:
                    # othersise try grabbing the attribute of that name and improve it
                    for i in range(nLoops):
                        getattr(creatures[key], user_input[1]).improve() 
                creatures[key].refresh() # recalculate toughness and fighting 
            except AttributeError:
                # so if we encountered this error (this _should_ be the only one possible)
                error_line = "{} has no attribute {}".format(key, user_input[1])
        # works exactly like improve, but changed improve() to reduce()
        elif user_input[0]=='reduce':
            if len(user_input)<2:
                error_line = "missing an argument"
                continue
            elif len(user_input)==3:
                try:
                    nLoops = int(user_input[2])
                except ValueError:
                    nLoops = 1
                    error_line = "I couldn't cast {} as an int! Improving one step".format(user_input[2])
            else:
                nLoops = 1
            try:
                if user_input[1] in creatures[key].skills:
                    for i in range(nLoops):
                        creatures[key].skills[user_input[1]].reduce()
                else:
                    for i in range(nLoops):
                        getattr(creatures[key], user_input[1]).reduce()
                creatures[key].refresh()
            except AttributeError:
                error_line="{} has no attribute {}".format(key, user_input[1])
        
        # add skill! 
        elif user_input[0]=='skill':
            # if it's length 3, then hopefully they specified the die value
            if len(user_input)==3:
                try:
                    creatures[key].add_skill( user_input[1], int(user_input[2]))
                    creatures[key].refresh()
                except ValueError:
                    # mainly here incase they write "d6" instead of "6"
                    error_line="Cannot cast {} as an integer".format(user_input[2]) 
            elif len(user_input)==2:
                # in this case they didn't specify the die type, so let's add it as a 4
                creatures[key].add_skill( user_input[1], 4)
            else:
                error_line="'skill' accepts args like 'skill <skill> <die>'."
        elif user_input[0]=='edge':
            if len(user_input)>=3:
                description = " ".join(user_input[2:]) # take all the args after the edge name
                creatures[key].add_edge(user_input[1], description)
            else:
                error_line="'edge' requires args like 'edge <name> <desc>'"
        elif user_input[0]=='hindrance':
            if len(user_input)>=3:
                description = " ".join(user_input[2:]) # take all the args after the hindrance name
                creatures[key].add_hindrance(user_input[1], description)
            else:
                error_line="'hindrance' requires args like 'hindrance <name> <desc>'"
        elif user_input[0]=='special':
            if len(user_input)>=3:
                description = " ".join(user_input[2:]) # take all the args after the special ability name
                creatures[key].add_special(user_input[1], description)
            else:
                error_line="'special' requires args like 'hindrance <name> <desc>'"
        elif user_input[0]=='force':
            # manually set one of the int-like stats to a number
            #       only works on creature attributes that are numbers (not sw.Traits or dicts or lists)
            if len(user_input)!=3:
                print("ya fucked up.")
            else:
                try:
                    # make sure that the attribute the user wants to change is either an int or a float
                    if isinstance( getattr(creatures[key], user_input[1]), int) or isinstance( getattr(creatures[key], user_input[1]), float): 
                        setattr(creatures[key], user_input[1], float(user_input[2]))
                    else:
                        error_line="{} is type {}, not int or float".format(getattr(creatures[key],user_input[1]), type(getattr(creatures[key], user_input[1])))
                except ValueError:
                    # but of course the user's input  might not even be an int or a float...
                    error_line="{} is not a number".format(user_input[2])
                except AttributeError:
                    # and they might not hav eeven specified a valid attribute 
                    error_line="{} is not an attribute of {}".format(user_input[1], key)
        elif user_input[0]=='remove':
            # used to remove  an entry from one of the dicts.
            if len(user_input)!=3:
                error_line = "Syntax error: 'remove <skills/edge/hindrance/special> <name>'"
            else:
                try:
                    del getattr(creatures[key], user_input[1])[user_input[2]]
                except AttributeError:
                    # that thing doesn't exist
                    error_line="{} is not an attribute of {}".format(user_input[1], key)
                except TypeError:
                    # they tried using this on a number, list, or an attribute 
                    error_line="This only works on skills, edges, hindrances, and special abilities!"

        elif user_input[0]=='animal':
            # flip the smarts between animal and humanoid
            if creatures[key].animal:
                creatures[key].animal = False
            else:
                creatures[key].animal = True
        elif user_input[0]=='wild_card':
            # flip the wild card status
            if creatures[key].wild_card:
                creatures[key].wild_card = False
            else:
                creatures[key].wild_card = True
        elif user_input[0]=='give':
            # this is the 'give' option
            #   currently borked afaik
            if len(user_input)==2:
                if user_input[1] in items:
                    creatures[key].give( items[user_input[1]] )
                else:
                    error_line = "{} is not in the item database".format(user_input[1])
            else:
                error_line = "give requires only 2 arguments, you entered {}".format(len(user_input))
        elif user_input[0] in ['help','Help','h']:
            printHelp=True
        else:
            error_line="{} not recognized. Try 'help'".format(user_input[0])

def new(args):
    """
    used to make new creatures and items 
    """
    global creatures
    global items
    nArgs = len(args)
    if nArgs != 3:
        print("function 'new' takes 3 arguments, you provided: {}".format(nArgs))
        print("new <class> <name>")
        print("")
        return()
    
    if args[1] in ['creature', 'Creature', 'Creatures', 'creature']:
        if args[2] in creatures:
            print("creature {} already exists. Try 'edit {}'".format(args[2], args[2]))
            return()
        else:
            # if they are making a unique creature, launch into the editor, above
            creatures[args[2]] = sw.Creature()
            edit_creature(args[2])

    elif args[1] in ['item', 'Item', 'Items', 'items']:
        if args[2] in items:
            print("That item already exists!")
            return()

        # have the user input a string description and a number-like weight
        desc = input("Item description: ")
        while True:
            try:
                weight = float(input("Item weight: "))
                break
            except ValueError:
                print("that's not an acceptable weight")
        items[args[2]] = sw.Gear( args[2], weight, desc )

def list_grp():
    """
    just spits out the known creatures and items
    """
    global creatures
    global items
    print("Currently, saved creatures are:")

    keylist = np.sort([key for key in creatures])
    for key in keylist:
        print("    {}".format(key))
    print("")
    keylist = np.sort([key for key in items])
    print("and saved items are:")
    for key in keylist:
        print("    {}".format(key))

def help_me():
    """
    it helps the user if they don't know what to do
    I just hope people know to type 'help' when they need 'help'
    """
    print("You've using the SWADE helper help function.")
    print("")
    print("Enter 'exit' to exit")
    print("")
    print("'list' - returns a list of creatures and items saved in the database")
    print("'new <creature/item> <name>' - creates a new item or creature with the given name. If creating a creature, enters the creature editor")
    print("'edit <name>' - enters the creature editor for the creature specified")
    print("'stat <name>' - prints stats of creature specified")
    print("")

def stat(key):
    os.system('cls' if os.name=='nt' else 'clear')
    global creatures
    if key in creatures:
        print("{}: ".format(key))
        print(creatures[key])
    elif key in items:
        print(items[key])
    else:
        print("{} isn't in either list.",format(key))

def search(arg):
    """
    Scans over the keys and returns the ones that match a string provided by the user
    """
    if len(arg)<2:
        print("... for what?")
        return()
    elif len(arg)>2:
        search_term =  description = " ".join(arg[2:])  # if user provides a big sentence, make the whole thing (minus 'search ') the search string
    else:
        search_term = arg[1]

    global creatures
    global items
    
    print("Searching for {}".format(search_term))
    for key in creatures:
        if search_term in key:
            print("Creature: {}".format(key))
    for key in items:
        if search_term in key:
            print("Item: {}".format(key))




# only use this when I need to update things with new class definitions 
def update():
    return() # don't do anything, this is deprecated! 
    global creatures
    for key in creatures:
        creatures[key].gear = []


def main():
    """
    master control function

    Just goes in a little loop waiting to hear one of the command words
    """
    user_input = ""
    out_words = ['q', 'Q', 'quit', 'Quit', 'exit', 'Exit', 'fuck you']
    while user_input not in out_words:
        user_input = input("sw helper ... $  ")
        if user_input=="":
            continue
        user_input = user_input.split() # split by spaces to get individual arguments
        if user_input[0] in out_words:
            break
        if user_input[0] in ['help', 'h', 'Help', 'wtf', 'what', 'wat']:
            help_me()
        if user_input[0] == "new":
            new(user_input)
        if user_input[0] =='list':
            list_grp()
        if user_input[0] =='edit':
            if len(user_input)>1:
                edit_creature(user_input[1])
        if user_input[0]=='stat':
            if len(user_input)>1:
                stat(user_input[1])
        if user_input[0]=='update':
            update()
        if user_input[0] in ['search', 'Search', 'find']:
            search(user_input)

    # save any changes to the database to disk
    print("Saving...")
    save()
    print("Goodbye!")

load()
main()
