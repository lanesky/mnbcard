import hashlib

def sha256sum(filename):
    h  = hashlib.sha256()
    b  = bytearray(128*1024)
    mv = memoryview(b)
    with open(filename, 'rb', buffering=0) as f:
        while n := f.readinto(mv):
            h.update(mv[:n])
    return h.hexdigest()

def sha256_str_to_int_array(sha256_str):
    int_array = []
    for i in range(0, 32):
        int_array.append(int((sha256_str[i * 2] + sha256_str[i * 2 + 1]), 16))
    return int_array

def get_file_hash(filename):
    sha256 = sha256sum(filename)
    hash = sha256_str_to_int_array(sha256)
    return hash

def save_to_file(filename, data):
    newFile = open(filename, "wb")
    newFileByteArray = bytearray(data)
    newFile.write(newFileByteArray)