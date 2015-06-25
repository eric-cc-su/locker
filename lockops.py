try:
    from cryptography.fernet import Fernet
except:
    raise Exception("The system is not properly initialized")
import json
import os, os.path
import time

from tempfile import mkstemp

ukey = ""

def dir_search(initkey, bool=False):
    global ukey
    if initkey == None:
        initkey = ukey
    fd, tpath = mkstemp()
    directory = os.path.dirname(tpath)
    os.close(fd)
    os.remove(tpath)

    for fname in os.listdir(directory):
        if fname.endswith(initkey) and fname[:2] != "+~":
            apath = os.path.join(directory, fname)
            if ukey == "":
                ukey = initkey

            if bool:
                return True
            return apath
    return False


def decrypt_entry():
    print("decrypt")


def import_file(filepath, lineformat, sray):
    global ukey
    key = Fernet.generate_key()
    f = Fernet(key)

    lidx = lineformat.index('LABEL')
    hidx = lineformat.index('PWD')
    lblevel = 0
    if lidx > hidx:
        lblevel = 1
        lidx = hidx
        hidx = lineformat.index('LABEL')

    pre = lineformat[:lidx].strip('LABEL').strip('PWD')
    mid = lineformat[lidx:hidx].strip('LABEL').strip('PWD')
    suf = lineformat[hidx:].strip('LABEL').strip('PWD')

    with open(filepath, "r") as ifile:
        for line in ifile:
            loval = line[line.index(pre):line.index(mid)]
            hival = line[line.index(mid) + len(mid):line.index(suf)]
            if suf == "":
                hival = line[line.index(mid) + len(mid):]

            label = loval
            passwd = hival
            if lblevel == 1:
                label = hival
                passwd = loval

            sray[label] = f.encrypt(bytes(passwd, "UTF-8")).decode("UTF-8")

    write_secure_tfile(sray)
    return read_secure_tfile()

# Deprecated check to JSON file, may be reinstated later
"""
def load_fp():  # Retrieve JSON file
    global repo_path
    with open("sc/dump.json", "r") as dfile:
        fp = json.load(dfile)
        if len(fp) > 0:
            return fp
    return False
"""

# https://www.logilab.org/blogentry/17873
# https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp
def init_secure_tfile(cusuffix):  # Create secure tmp file
    global ukey
    ukey = cusuffix


def read_secure_tfile(blocksize=5000):          # Read secure tmp file
    global ukey
    repo_path = dir_search(ukey)
    rfile = os.open(repo_path, os.O_RDONLY)
    obj = os.read(rfile, blocksize)             # Retrieve object
    os.close(rfile)
    os.remove(repo_path)                        # Destroy file
    return json.loads(obj.decode("UTF-8"))


def write_secure_tfile(data):  # Write secure tmp file
    global ukey
    obj = json.dumps(data).replace('\\"','"')
    bobj = bytes(obj, "utf-8")
    try:
        repo_path = dir_search(ukey)
        os.remove(repo_path)
    except TypeError:
        pass
    fd, repo_path = mkstemp(suffix=ukey)        #Create file
    os.write(fd, bobj)
    os.close(fd)