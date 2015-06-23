try:
	from cryptography.fernet import Fernet
except:
	raise Exception("The system is not properly initialized")
import json
import os, os.path
import time

def import_file(filepath, lineformat, sray):
	key = Fernet.generate_key()
	f = Fernet(key)

	lidx = lineformat.index('LABEL')
	hidx =lineformat.index('PWD')
	lblevel = 0
	if lidx > hidx:
		lblevel = 1
		lidx = hidx
		hidx = lineformat.index('LABEL')

	pre = lineformat[:lidx].strip('LABEL').strip('PWD')
	mid = lineformat[lidx:hidx].strip('LABEL').strip('PWD')
	suf = lineformat[hidx:].strip('LABEL').strip('PWD')

	label = ""
	passwd = ""

	with open(filepath, "r") as ifile:
		for line in ifile:
			loval = line[line.index(pre):line.index(mid)]
			hival = line[line.index(mid)+len(mid):line.index(suf)]
			if suf == "":
				hival = line[line.index(mid)+len(mid):]

			label = loval
			passwd = hival
			if lblevel == 1:
				label = hival
				passwd = loval

			sray[label] = f.encrypt(bytes(passwd, "UTF-8")).decode("UTF-8")

	try:
		os.mkdir("sc")
	except:
		pass

	with open("sc/dump.json","w") as dfile:
		json.dump(sray,dfile)