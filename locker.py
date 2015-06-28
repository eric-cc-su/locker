try:
    from cryptography.fernet import Fernet
except:
    raise Exception("The system is not properly initialized")

import json
import lockops
import os
import platform
import time

EXIT = True
IFILE = None
IFORMAT = None
MTB = {}
UPRF = ""

def clear_screen():
    if platform.system() in ['Darwin', 'Linux']:  # Mac & Linux
        os.system('clear')
    else:
        os.system('cls')

def gen_screen(prompt, input_text="INPUT: ", back=False, menu=None):
    clear_screen()
    print("\t*************************************************")
    if menu is None:
        print("\t***                  Locker                   ***")
    else:
        print(menu)
    print("\t***                                           ***")
    print("\t***                                           ***")
    print(prompt)
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    if back:
        print("\t***           :q   - previous menu            ***")
    else:
        print("\t***         :q     - close application        ***")
    print("\t*************************************************")
    return( input(input_text) )

def screen_decrypt():
    prompt = "\t*** INPUT ENTRY LABEL                         ***"
    menu = "\t***              Locker - Decrypt             ***"
    ks = gen_screen(prompt ,'LABEL: ', True).strip().lower()
    if ks == ":q":
        screen_main()
    else:
        lockops.decrypt_entry(MTB, ks)
        input("PRESS ENTER TO CONTINUE")

def screen_import():
    global IFILE
    clear_screen()
    menu = "\t***              Locker - Import              ***"
    prompt = "\t***               INPUT FILENAME              ***"

    ks = gen_screen(prompt, "FILENAME: ", True, menu).strip().lower()
    if ks == ":q":
        screen_main()
    else:
        try:
            with open(ks, "r") as test:
                pass
            IFILE = ks
            screen_import2()
        except FileNotFoundError:
            print()
            print(ks, " IS NOT A VALID FILE")
            time.sleep(1)
            screen_import()

def screen_import2():
    global IFORMAT
    global MTB
    clear_screen()
    print("\t*************************************************")
    print("\t***              Locker - Import              ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t*** Using labels 'LABEL' and 'PWD':           ***")
    print("\t*** Give format of file lines                 ***")
    print("\t***                                           ***")
    print("\t*** ex:                                       ***")
    print("\t*** `Facebook - password` --> `LABEL - PWD`   ***")
    print("\t***                                           ***")
    print("\t***           :q   - previous menu            ***")
    print("\t*************************************************")
    ks = input('FORMAT: ')
    if ks == ":q":
        screen_import()
    else:
        IFORMAT = ks
        try:
            MTB = lockops.import_file(IFILE, IFORMAT, MTB)
        except ValueError:
            print("FORMAT NOT FOUND - Please input exact format of file lines")
            time.sleep(1)
            screen_import2()

def screen_list():
    global MTB
    clear_screen()
    try:
        for key, val in MTB.items():
            print(key + ": " + str(val))
            print()
    except:
        print(MTB)
    input("Continue: ")

def screen_main():
    global EXIT
    global MTB
    clear_screen()
    print("\t*************************************************")
    print("\t***                  Locker                   ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t***                                           ***")
    print("\t*** list   - list entries                     ***")
    print("\t*** import - import from text file            ***")
    print("\t*** new    - create new entry                 ***")
    print("\t*** delete - delete entry                     ***")
    print("\t*** decrypt- decrypt entry                    ***")
    print("\t***                                           ***")
    print("\t*** :q     - close application                ***")
    print("\t*************************************************")
    ks = input("INPUT: ").strip().lower()
    if ks == 'exit':
        EXIT = False
    elif ks == ":q":
        EXIT = False
    elif ks == "list":
        screen_list()
    elif ks == "import":
        screen_import()
    elif ks == "new":
        pass
    elif ks == "delete":
        pass
    elif ks == "decrypt":
        screen_decrypt()
    return

def cntn_main():
    while EXIT:
        screen_main()
    if not lockops.dir_search(None, True):  # Save file
        lockops.write_secure_tfile(MTB)
    clear_screen()
    return

#*************************************** MAIN ********************************
clear_screen()
apwd = gen_screen("\t***          INPUT LOCKER COMBINATION         ***")
if apwd != ":q":
    if not lockops.dir_search(apwd, True, True):
        prmpt = input("Combination is unrecognized. Create new repository? (y/n)")
        if prmpt == "y":
            lockops.init_secure_tfile(apwd)
            cntn_main()
    else:
        MTB = lockops.read_secure_tfile()
        lockops.load_key()
        cntn_main()
clear_screen()
