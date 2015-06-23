try:
	from cryptography.fernet import Fernet
except:
	raise Exception("The system is not properly initialized")

import lockops
import os
import time

EXIT = True
IFILE = None
IFORMAT = None
MTB = {}

def screen_import():
	global IFILE
	os.system('cls')
	print("\t*************************************************")
	print("\t***              Locker - Import              ***")
	print("\t***                                           ***")
	print("\t***                                           ***")
	print("\t*** INPUT FILENAME                            ***")
	print("\t***                                           ***")
	print("\t*** :back   - back to main menu               ***")
	print("\t*************************************************")
	ks = input('FILENAME: ').strip().lower()
	if ks == ":back":
		screen_main()
	elif ks == ":q":
		EXIT = False
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
	os.system('cls')
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
	print("\t*** :back   - back to main menu               ***")
	print("\t*************************************************")
	ks = input('FORMAT: ')
	if ks == ":back":
		screen_import()
	elif ks == ":q":
		EXIT = False
	else:
		IFORMAT = ks
		farray = lockops.import_file(IFILE, IFORMAT, MTB)

def screen_list():
	global MTB
	os.system('cls')
	for key, val in MTB.items():
		print(key + ": " + str(val))
		print()
	input("Continue: ")

def screen_main():
	global EXIT
	global MTB
	os.system('cls')
	print("\t*************************************************")
	print("\t***              Locker - Import              ***")
	print("\t***                                           ***")
	print("\t***                                           ***")
	print("\t***                                           ***")
	print("\t*** list   - list entries                     ***")
	print("\t*** import - import from text file            ***")
	print("\t*** new    - create new entry                 ***")
	print("\t*** delete - delete entry                     ***")
	print("\t***                                           ***")
	print("\t*** exit   - close application                ***")
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

while EXIT:
	screen_main()
os.system('cls')