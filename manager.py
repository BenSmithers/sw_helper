#!/usr/bin/python3.6
import pickle
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
    for key in creatures:
        print("    {}".format(key))
    for key in items:
        print("    {}".format(key))
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

    TODO: allow the removal of skills, edges, hindrances
    """
    global creatures
    global items

    if key not in creatures:
        print("{} not in creatures".format(key))
        return()
    user_input = ""
    error_line = ""
    accepted = ['improve', 'reduce','give','skill', 'edge', 'hindrance', 'special', 'force', 'remove', 'wild_card', 'animal']
    while user_input != "done":
        os.system('cls' if os.name=='nt' else 'clear')
        print("Editing '{}'. Type 'done' when done modifying".format(key))
        if error_line!="":
            print("")
            print(error_line)
        print("")
        print(creatures[key])
        print("")
        user_input = input("sw helper ... C$ ")
        if user_input=="done":
            break

        user_input = user_input.split()
        error_line = ""

        # raise/lower/give/add_skill/

        if user_input[0] in accepted:
            if user_input[0]=='improve':
                try:
                    if user_input[1] in creatures[key].skills:
                        # if it's a skill snag the entry in the skill list and improve it
                        creatures[key].skills[user_input[1]].improve()
                    else:
                        # othersise try grabbing the attribute of that name and improve it
                        getattr(creatures[key], user_input[1]).improve() 
                    creatures[key].refresh()
                except AttributeError:
                    error_line = "{} has no attribute {}".format(key, user_input[1])
            elif user_input[0]=='reduce':
                try:
                    if user_input[1] in creatures[key].skills:
                        creatures[key].skills[user_input[1]].reduce()
                    else:
                        getattr(creatures[key], user_input[1]).reduce()
                    creatures[key].refresh()
                except AttributeError:
                    error_line="{} has no attribute {}".format(key, user_input[1])

            elif user_input[0]=='skill':
                if len(user_input)==3:
                    try:
                        creatures[key].add_skill( user_input[1], int(user_input[2]))
                        creatures[key].refresh()
                    except ValueError:
                        error_line="Cannot cast {} as an integer".format(user_input[2])
                elif len(user_input)==2:
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
                    description = " ".join(user_input[2:]) # take all the args after the edge name
                    creatures[key].add_hindrance(user_input[1], description)
                else:
                    error_line="'hindrance' requires args like 'hindrance <name> <desc>'"
            elif user_input[0]=='special':
                if len(user_input)>=3:
                    description = " ".join(user_input[2:]) # take all the args after the edge name
                    creatures[key].add_special(user_input[1], description)
                else:
                    error_line="'special' requires args like 'hindrance <name> <desc>'"
            elif user_input[0]=='force':
                if len(user_input)!=3:
                    print("ya fucked up.")
                else:
                    try:
                        if isinstance( getattr(creatures[key], user_input[1]), int) or isinstance( getattr(creatures[key], user_input[1]), float):
                            setattr(creatures[key], user_input[1], float(user_input[2]))
                        else:
                            error_line="{} is type {}, not int or float".format(getattr(creatures[key],user_input[1]), type(getattr(creatures[key], user_input[1])))
                    except ValueError:
                        error_line="{} is not a number".format(user_input[2])
                    except AttributeError:
                        error_line="{} is not an attribute of {}".format(user_input[1], key)
            elif user_input[0]=='remove':
                if len(user_input)!=3:
                    error_line = "Syntax error: 'remove <skill/edge/hindrance/special> <name>'"
                else:
                    try:
                        del getattr(creatures[key], user_input[1])[user_input[2]]
                    except AttributeError:
                        error_line="{} is not an attribute of {}".format(user_input[1], key)
                    except TypeError:
                        error_line="This only works on skills, edges, hindrances, and special abilities!"
            elif user_input[0]=='animal':
                if creatures[key].animal:
                    creatures[key].animal = False
                else:
                    creatures[key].animal = True
            elif user_input[0]=='wild_card':
                if creatures[key].wild_card:
                    creatures[key].wild_card = False
                else:
                    creatures[key].wild_card = True
            else:
                if len(user_input)==2:
                    if key in items:
                        creatures[key].give( items[user_input[1]] )
                    else:
                        error_line = "{} is not in the item database".format(user_input[1])
                else:
                    error_line = "give requires only 2 arguments, you entered {}".format(len(user_input))
        else:
            error_line="{} not recognized. Try '<improve/reduce/give/skill/edge/hindrance'> <arg>".format(user_input[0])

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
            creatures[args[2]] = sw.Creature()
            edit_creature(args[2])
    elif args[1] in ['item', 'Item', 'Items', 'items']:
        if args[2] in items:
            print("That item already exists!")
            return()

        desc = input("Item description: ")
        while True:
            try:
                weight = float(input("Item weight: "))
                break
            except ValueError:
                print("that's not an acceptable weight")
        items[args[2]] = sw.gear( args[2], weight, desc )

def list_grp():
    global creatures
    global items
    print("Currently, saved creatures are:")
    for key in creatures:
        print("    {}".format(key))
    print("and saved items are:")
    for key in items:
        print("    {}".format(key))

def help_me():
    print("You've using the Savage Worlds helper")
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


# only use this when I need to update things with new class definitions 
def update():
    return()
    global creatures
    for key in creatures:
        setattr(creatures[key], 'wild_card', False)
        setattr(creatures[key], 'animal', True)

def main():
    user_input = ""
    out_words = ['q', 'Q', 'quit', 'Quit', 'exit', 'Exit', 'fuck you']
    while user_input not in out_words:
        user_input = input("sw helper ... $  ")
        user_input = user_input.split() # split by spaces to get individual arguments
        if user_input[0] in out_words:
            break
        if user_input[0] in ['help', 'h', 'Help']:
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

    print("Saving...")
    save()
    print("Goodbye!")

load()
main()
