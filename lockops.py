# Look into pywin32 for win32security
try:
    from cryptography.fernet import Fernet
except:
    raise Exception("The system is not properly initialized")
import json
import os, os.path
import sys
import time

from tempfile import mkstemp

ukey = ""   # user's input combo
klg = 0     # length of file key to look for

#file interactions
def create_file(sfx=None):
    if sys.platform != "darwin":
        fd, filepath = mkstemp(suffix=sfx)
    else:
        fn_prefix = ""
        for num in range(ord(os.urandom(1)) % 100):
            trial = os.urandom(1)
            while ord(trial) < 33 or ord(trial) > 126 or ord(trial) in [47, 92]:  #writeable characters
                trial = os.urandom(1)
            fn_prefix += trial.decode()
        filepath = os.path.join("store", fn_prefix + sfx)
        with open(filepath, "w+b") as fd:
            pass
        fd = os.open(filepath, os.O_RDWR)
    return fd, filepath

def close_file(fd, fpath):
    os.close(fd)
    if sys.platform == "darwin":
        os.chmod(fpath, 256)

def open_file(fpath, mode):
    os.chmod(fpath, 448)
    fd = os.open(fpath, mode)
    return fd

def secure_directory():
    if sys.platform == "darwin":
        os.chmod("store", 256)

#end file interactions

def dir_search(suf, bool=False, kfind=False):
    global klg
    global ukey
    if suf == None:
        suf = ukey
    if sys.platform != "darwin":  # Not OS X
        fd, tpath = mkstemp()
        directory = os.path.dirname(tpath)
        os.close(fd)
        os.remove(tpath)
    else:
        if not os.path.isdir("store"):
            os.mkdir("store", 448)
        directory = "store"
    os.chmod("store", 448)

    for fname in os.listdir(directory):
        if fname.endswith(suf) and fname[:2] != "+~":
            if kfind:
                klg = int(fname[-(len(suf)+1)])  # klg placed right before ukey
            apath = os.path.join(directory, fname)

            if ukey == "":
                ukey = suf

            if bool:
                return True
            os.chmod(apath, 493)
            return apath
    return False


def add_entry(directory_obj, label, pwd):
    key = bin_dec(load_key().decode())
    f = Fernet(key)
    directory_obj[label.lower()] = f.encrypt(bytes(pwd, "UTF-8")).decode("UTF-8")
    return directory_obj


def decrypt(directory_obj, label):
    key = bin_dec(load_key().decode())
    f = Fernet(key)

    if os.path.isfile(label):
        with open(label, 'r') as efile:
            blockdata = efile.read()

        with open(label,'w') as wfile:
            wfile.write(f.decrypt(bytes(blockdata, 'UTF-8')).decode())
        print("FILE DECRYPTED")
    else:
        try:
            retrieve = directory_obj[label.lower()]
            received = f.decrypt(retrieve.encode()).decode()
            print(received)
        except KeyError:
            print("No matching entry in repository")


def delete_entry(directory_obj, label):
    del directory_obj[label.lower()]
    return directory_obj


def encrypt_file(filepath):
    key = bin_dec(load_key().decode())
    f = Fernet(key)

    if os.path.isfile(filepath):
        with open(filepath, 'r') as efile:
            blockdata = efile.read()
        with open(filepath,'w') as wfile:
            wfile.write(f.encrypt(bytes(blockdata, 'UTF-8')).decode())
        print("FILE ENCRYPTED")

    else:
        print("File not found!")
        time.sleep(1.5)


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
            if suf == "":
                hival = line[line.index(mid) + len(mid):]
            else:
                hival = line[line.index(mid) + len(mid):line.index(suf)]

            label = loval
            passwd = hival
            if lblevel == 1:
                label = hival
                passwd = loval

            sray[label.lower().strip()] = f.encrypt(bytes(passwd.strip(), "UTF-8")).decode("UTF-8")

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
    fd, repo_path = create_file(str(klg) + ukey)  # Create file
    os.write(fd, bobj)
    close_file(fd, repo_path)


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

def enc2(data, datatype="str"):
    trial = ""
    binconvert = ""
    if type(data) == bytes:
        data = data.decode()
    for letter in data:
        testch = os.urandom(1)
        while ord(testch) < 33 and ord(testch) > 126:
            testch = os.urandom(1)
        trial += format(ord(testch), "#010b")[2:]
        #32(space) - 126

def genkey():  # Generate F key
    key = Fernet.generate_key()
    return key


def load_key():
    global ukey
    global klg

    apath = dir_search(bin_enc(ukey[:klg]) + str(klg))
    if type(apath) == bool and not apath:
        apath = dir_search(bin_enc(ukey[:klg]))
        if apath == False:
            raise Exception("DIR_SEARCH COULD NOT FIND KEY FILE")
    fd = os.open(apath, os.O_RDONLY)
    obj = os.read(fd, 100)
    close_file(fd, apath)

    return obj


def save_key(key):  # Save F key
    global klg
    global ukey

    tk = bin_enc(key).encode()
    klg = round( ord(os.urandom(1))/(ord(os.urandom(1))+1) ) + 1
    fd, repo_path = create_file(bin_enc(ukey[:klg]) + str(klg))
    time.sleep(2)
    os.write(fd, tk)
    close_file(fd, repo_path)
