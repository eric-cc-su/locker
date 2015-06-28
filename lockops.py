# Look into pywin32 for win32security
try:
    from cryptography.fernet import Fernet
except:
    raise Exception("The system is not properly initialized")
import json
import os, os.path
import time

from tempfile import mkstemp

ukey = ""   # user's input combo
klg = 0     # length of file key to look for

def dir_search(suf, bool=False, kfind=False):
    global klg
    global ukey
    if suf == None:
        suf = ukey
    fd, tpath = mkstemp()
    directory = os.path.dirname(tpath)
    os.close(fd)
    os.remove(tpath)

    for fname in os.listdir(directory):
        if fname.endswith(suf) and fname[:2] != "+~":
            if kfind:
                klg = int(fname[-(len(suf)+1)])  # klg placed right before ukey
            apath = os.path.join(directory, fname)

            if ukey == "":
                ukey = suf

            if bool:
                return True
            return apath
    return False


def add_entry(directory, label, pwd):
    key = bin_dec(load_key().decode())
    f = Fernet(key)
    directory[label.lower()] = f.encrypt(bytes(pwd, "UTF-8")).decode("UTF-8")
    return directory


def decrypt_entry(directory, label):
    key = bin_dec(load_key().decode())
    f = Fernet(key)

    try:
        retrieve = directory[label.lower()]
        recieved = f.decrypt(retrieve.encode()).decode()
        print(recieved)
    except KeyError:
        print("No matching entry in repository")


def import_file(filepath, lineformat, sray):
    global ukey
    key = genkey()
    if not dir_search(bin_enc(ukey[:klg]) + str(klg), True):
        save_key(key)
    else:
        key = bin_dec(load_key().decode())
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

            sray[label.lower()] = f.encrypt(bytes(passwd, "UTF-8")).decode("UTF-8")

    write_secure_tfile(sray)
    return read_secure_tfile()


# https://www.logilab.org/blogentry/17873
# https://docs.python.org/3/library/tempfile.html#tempfile.mkstemp
def init_secure_tfile(cusuffix):  # Create secure tmp file
    global ukey
    ukey = cusuffix
    save_key(genkey())


def read_secure_tfile(blocksize=5000):  # Read tmp file
    global ukey
    repo_path = dir_search(ukey)
    rfile = os.open(repo_path, os.O_RDONLY)
    obj = os.read(rfile, blocksize)  # Retrieve object
    os.close(rfile)
    os.remove(repo_path)  # Destroy file
    return json.loads(obj.decode("UTF-8"))


def write_secure_tfile(data):  # Write tmp file
    global ukey
    obj = json.dumps(data).replace('\\"', '"')
    bobj = bytes(obj, "utf-8")
    try:
        repo_path = dir_search(ukey)
        os.remove(repo_path)
    except TypeError:
        pass
    fd, repo_path = mkstemp(suffix=str(klg) + ukey)  # Create file
    os.write(fd, bobj)
    os.close(fd)


def bin_enc(data, datatype="str"):  # Simple cipher using binary, and hex translations
    trial = ""
    tdata = data
    if type(data) == bytes:
        tdata = tdata.decode()

    for letter in tdata:  # analyze data
        trial += hex(int(bin(ord(letter)), 2))[2:]
    return trial


def bin_dec(data):  # decoding
    trial = ""
    item = ""
    for letter in data:
        item += str(bin(int("0x" + letter, 16)))[2:].zfill(4)
        if len(item) == 8:
            numitem = int(item, 2)
            trial += chr(numitem)
            item = ""
    return trial


def genkey():  # Generate F key
    key = Fernet.generate_key()
    return key


def load_key():
    global ukey
    global klg

    apath = dir_search(bin_enc(ukey[:klg]) + str(klg))
    fd = os.open(apath, os.O_RDONLY)
    obj = os.read(fd, 100)
    os.close(fd)

    return obj


def save_key(key):  # Save F key
    global klg
    global ukey

    tk = bin_enc(key).encode()
    klg = round( ord(os.urandom(1))/(ord(os.urandom(1))+1) ) + 1
    fd, repo_path = mkstemp(suffix=( bin_enc(ukey[:klg]) + str(klg)) )  # Create file
    os.write(fd, tk)
    os.close(fd)
