try:
	from cryptography.fernet import Fernet
except:
	raise Exception("The system is not properly initialized")
import json
import os, os.path
import time

from tempfile import mkstemp

def authenticate(initkey):
	fd, tpath = mkstemp()
	directory = os.path.dirname(tpath)
	os.close(fd)
	os.remove(tpath)
	for fname in os.listdir(directory):
		if fname.endswith(initkey):
			return True
	return False

def decrypt_entry():
	print("decrypt")

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

	if not load_fp():
		raise Exception("No existing repository file")
	scw(sray)
 
def load_fp():  # Retrieve JSON file
	with open("sc/dump.json","r") as dfile:
		fp = json.load(dfile)
		if len(fp) > 0:
			return fp
	return False

# https://www.logilab.org/blogentry/17873
# https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp
def ics(cusuffix):  # Create secure tmp file
	fd, tpath = mkstemp(suffix = cusuffix)
	os.close(fd)
	with open("sc/dump.json","w") as dfile:
		json.dump(tpath, dfile)

def rsc(blocksize=5000):  # Read secure tmp file
	fp = load_fp()
	rscf = os.open(fp, os.O_RDONLY)
	obj = os.read(rscf, blocksize)
	os.close(rscf)
	return obj

def scw(data):  # Write secure tmp file
	obj = bytes(json.dumps(data),"utf-8")
	fp = load_fp()
	scwf = os.open(fp, os.O_WRONLY)
	os.write(scwf, obj)
	os.close(scwf)