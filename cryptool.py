import argparse
from cryptography.fernet import Fernet
import os

KEY_FILE = "chiave.key"

def leggi_file(path):
    with open(path, "rb") as kf:
        return kf.read()
    
def scrivi_file(path,dati):
    with open(path, "wb") as kf:
        kf.write(dati)
        
def elimina_file(file1):
    os.remove(file1)
        
def generate_key(key):
    scrivi_file(KEY_FILE,key)
def carica_chiave():
    return leggi_file(KEY_FILE)
    
def cifra(file1,file2):
    try:
        key = Fernet.generate_key()
        f = Fernet(key)
        scrivi_file(KEY_FILE,key)
        read = leggi_file(file1)
        scrivi_file(file2, f.encrypt(read))
    except FileNotFoundError:
        print("file da cifrare non trovato")

def decifra(file1,file2):
    try:
        f = Fernet(carica_chiave())
        content = leggi_file(file2)
        encripted = f.decrypt(content)
        print(encripted.decode())
    except FileNotFoundError:
        print("il file non da decifrare non e stato trovato")
    except InvalidToken:
        print("la key non e corretta")
    except ValueError:
        print("non ce la key nel file .key") 
    
    
    
def main():
    Parser = argparse.ArgumentParser(description="esercizio")
    Parser.add_argument("azione", choices=["cripta", "decripta"])
    Parser.add_argument("--elimina",action="store_true")
    Parser.add_argument("file1")
    Parser.add_argument("file2")
    args = Parser.parse_args()
    
    if args.azione == "cripta":
        cifra(args.file1,args.file2)
        if args.elimina:
            elimina_file(args.file1)
    else:
        decifra(args.file1,args.file2)
        
    
if __name__ == "__main__":
    main()