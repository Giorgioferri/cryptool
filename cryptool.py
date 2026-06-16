import argparse
from cryptography.fernet import Fernet,InvalidToken
import os
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from getpass import getpass
import base64
import time
from cryptography.fernet import InvalidToken
KEY_FILE = "key.key"
SALT_FILE= "salt.salt"

def deriva_chiave(password,salt):
    kdf = PBKDF2HMAC(
        algorithm = hashes.SHA256(),
        length = 32,
        salt=salt,
        iterations=100000
    )
    raw = kdf.derive(password.encode())
    return base64.urlsafe_b64encode(raw)

def read_file(path):
    with open(path, "rb") as kf:
        return kf.read()

def write_file(path,data):
    with open(path, "wb") as kf:
        kf.write(data)
        
def delete_file(file1):
    os.remove(file1)
        
def generate_key(key):
    write_file(KEY_FILE,key)
def load_key():
    return read_file(KEY_FILE)
    
def encrypt(file1,file2):
    try:
        password = getpass("passowrd: ")
        salt = os.urandom(16)
        key = deriva_chiave(password,salt)
        f = Fernet(key)
        write_file(SALT_FILE, salt)
        read = read_file(file1)
        write_file(file2,f.encrypt(read))
    except FileNotFoundError:
        print("file to encrypt not found")

def decrypt(file1, file2):
    i = 0                             
    while True:                            
        try:
            password = getpass("password: ")
            salt = read_file(SALT_FILE)
            key = deriva_chiave(password, salt)
            f = Fernet(key)
            content = read_file(file2)
            testo = f.decrypt(content)
            print(testo.decode())
            break                   
        except FileNotFoundError:
            print("file to decrypt not found")
            break                        
        except InvalidToken:
            print("password sbagliata")
            i += 1                          
            if i == 5:
                for rimasti in range(300, 0, -1):
                    minuti = rimasti // 60
                    secondi = rimasti % 60
                    print(f"\rTempo rimasto: {minuti:02d}:{secondi:02d}", end="", flush=True)
                    time.sleep(1)
                print("\rTempo scaduto!          ")
                i = 0  

def main(): 
    Parser = argparse.ArgumentParser(description="exercise")
    Parser.add_argument("action", choices=["encrypt", "decrypt"])
    Parser.add_argument("--delete",action="store_true")
    Parser.add_argument("file1")
    Parser.add_argument("file2")
    args = Parser.parse_args()
    
    if args.action == "encrypt":
        encrypt(args.file1,args.file2)
        if args.delete:
            delete_file(args.file1)

    else:
        
        decrypt(args.file1,args.file2)
           
if __name__ == "__main__":
    main()