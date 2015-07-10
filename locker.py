try:
    from cryptography.fernet import Fernet
except:
    raise Exception("The system is not properly initialized")

import json
import lockops
import os
import platform
import sys
import time
import traceback

NULLCLS = False
EXIT = True
IFILE = None
IFORMAT = None
MTB = {}
UPRF = ""

def clear_screen():
    global NULLCLS
    if not NULLCLS:
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
    if type(prompt) == str:
        print(prompt)
    elif type(prompt) == list:
        for line in prompt:
            print(line)
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
    menu = "\t***              Locker - Decrypt             ***"
    prompt = "\t*** Input entry name or file path:            ***"
    ks = gen_screen(prompt ,'ENTRY/FILE: ', True).strip().lower()
    if ks == ":q":
        screen_main()
    else:
        lockops.decrypt(MTB, ks)
        input("PRESS ENTER TO CONTINUE")

def screen_delete():
    prompt = "\t*** INPUT ENTRY LABEL                         ***"
    menu = "\t***              Locker - Delete              ***"
    ks = gen_screen(prompt ,'LABEL: ', True).strip().lower()
    if ks == ":q":
        screen_main()
    else:
        lockops.delete_entry(MTB, ks)
        input("PRESS ENTER TO CONTINUE")

def screen_encrypt():
    prompt = "\t*** INPUT FILE PATH                           ***"
    menu = "\t***              Locker - Encrypt             ***"
    ks = gen_screen(prompt ,'FILE: ', True).strip().lower()
    if ks == ":q":
        screen_main()
    else:
        lockops.encrypt_file(ks)
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

    menu = "\t***              Locker - Import              ***"

    prompt = ["\t*** Using labels 'LABEL' and 'PWD':           ***",
        "\t*** Give format of file lines                 ***",
        "\t***                                           ***",
        "\t*** ex:                                       ***",
        "\t*** `Facebook - password` --> `LABEL - PWD`   ***"]

    ks = gen_screen(prompt, 'FORMAT: ', True, menu)
    if ks == ":q":
        screen_import()
    else:
        IFORMAT = ks
        MTB = lockops.import_file(IFILE, IFORMAT, MTB)
        """
        try:
            MTB = lockops.import_file(IFILE, IFORMAT, MTB)
        except ValueError as ex:
            print("FORMAT NOT FOUND - Please input exact format of file lines")
            traceback.print_tb(sys.exc_info()[2])
            time.sleep(1)
            screen_import2()
        """

def screen_list():
    global MTB
    clear_screen()
    try:
        for key, val in MTB.items():
            print(key)
            print()
    except:
        print(MTB)
    input("Continue: ")

def screen_new():
    label_prompt = "\t***                Input Label                ***"
    label_input_label = "LABEL: "
    menu = "\t***               Locker - New                ***"
    new_label = gen_screen(label_prompt, label_input_label, True, menu)

    pwd_prompt = "\t***              Input Password               ***"
    pwd_input_label = "PASSWORD: "
    new_pwd = gen_screen(pwd_prompt, pwd_input_label, True, menu)

    lockops.add_entry(MTB, new_label, new_pwd)

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
    print("\t*** encrypt - encrypt file                    ***")
    print("\t*** decrypt - decrypt entry                   ***")
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
        screen_new()
    elif ks == "delete":
        screen_delete()
    elif ks == "encrypt":
        screen_encrypt()
    elif ks == "decrypt":
        screen_decrypt()
    return

def cntn_main():
    global NULLCLS
    while EXIT:
        screen_main()
    if not lockops.dir_search(None, True):  # Save file
        lockops.write_secure_tfile(MTB)
        lockops.secure_directory()
        clear_screen()
    return

#*************************************** MAIN ********************************
clear_screen()
apwd = gen_screen("\t***          INPUT LOCKER COMBINATION         ***")
if apwd != ":q":
    try:
        if not lockops.dir_search(apwd, True, True):
            prmpt = input("Combination is unrecognized. Create new repository? (y/n)")
            if prmpt == "y":
                lockops.init_secure_tfile(apwd)
                cntn_main()
        else:
            MTB = lockops.read_secure_tfile()
            lockops.load_key()
            cntn_main()
    except Exception as ex:
        lockops.write_secure_tfile(MTB)
        NULLCLS = True
        exceptn = sys.exc_info()
        print()
        print(str(ex).upper())
        print()
        traceback.print_tb(exceptn[2])
clear_screen()
