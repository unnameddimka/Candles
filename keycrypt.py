import json
import getpass
from Crypto.Cipher import AES
from Crypto.Hash import SHA256
from Crypto import Random
import base64


def read(name):
    f = open(name)
    data = json.load(f)
    print("data loaded")
    return data


def write(name, data):
    f = open(name, "w")
    json.dump(data, f)
    print("data saved")


def encrypt_value(value, aeskey):
    IV = Random.new().read(AES.block_size)
    padding = AES.block_size - len(value) % AES.block_size
    encryptor = AES.new(aeskey, AES.MODE_CBC, IV)
    source = value.encode('UTF-8') + bytes([padding]) * padding
    return base64.b64encode(IV + encryptor.encrypt(source)).decode('utf-8')


def input_and_encrypt(name):
    apikey = input("input API key:")
    secretkey = input("input secret key:")
    paswd = input ("input password:")
    aeskey = SHA256.new(paswd.encode('UTF-8')).digest()
    enc_apikey = encrypt_value(apikey, aeskey)
    hash_apikey = base64.b64encode(SHA256.new(apikey.encode('UTF-8')).digest()).decode('utf-8')
    enc_secretkey = encrypt_value(secretkey, aeskey)
    hash_secretkey = base64.b64encode(SHA256.new(secretkey.encode('UTF-8')).digest()).decode('utf-8')

    result = {
        "apikey":{
            "value":enc_apikey,
            "hash":hash_apikey
        },
        "secretkey":{
            "value":enc_secretkey,
            "hash":hash_secretkey
        }
    }
    write(name, result)



def decrypt_value(source, aeskey):
    IV = source[:AES.block_size]
    decryptor = AES.new(aeskey, AES.MODE_CBC, IV)
    value = decryptor.decrypt(source[AES.block_size:])
    padding = value[-1]  # pick the padding value from the end; Python 2.x: ord(data[-1])
    if value[-padding:] != bytes([padding]) * padding:  # Python 2.x: chr(padding) * padding
        raise ValueError("Invalid padding...")
    return value[:-padding]


def check_hash(value, hash):
    if hash == base64.b64encode(SHA256.new(value).digest()).decode("utf-8"):
        print("key check OK")
    else:
        print("key check not OK")
    return value.decode("utf-8")


def read_and_decrypt(name):
    data = read(name)
    paswd = getpass.getpass()
        #input("input password:")
    enc_apikey = base64.b64decode(data["apikey"]["value"])
    hash_apikey = base64.b64decode(data["apikey"]["hash"])
    enc_secretkey = base64.b64decode(data["secretkey"]["value"])
    hash_secretkey = base64.b64decode(data["secretkey"]["hash"])
    aeskey = SHA256.new(paswd.encode('UTF-8')).digest() #getting encryption key from password.

    apikey = decrypt_value(enc_apikey, aeskey)
    check_hash(apikey, hash_apikey)
    secretkey = decrypt_value(enc_secretkey, aeskey)
    check_hash(secretkey, hash_secretkey)
    result = {"apikey": apikey.decode('UTF-8'), "secretkey": secretkey.decode('UTF-8')}
    return result


if __name__ == '__main__':
    #data = read("config/key.js")
    #write("config/key2.js", data)
    #input_and_encrypt("config/enckey.js")
    key = read_and_decrypt('config/enckey.js')
    print("decrypted key "+str(key)+"")
