#TODO:
#   -code input

import mysql.connector
import signal
#from sys import *
from getpass import getpass

def exitWrapper(sig, frame):
    cnx.commit()
    cursor.close()
    cnx.close()
    print('exited')
    exit()

def inputWrapper(force=False, default=None, prompt="?", type=None):
    while True:
        try:
            inputedData = input(prompt)
        except:
            if force:
                stdout.write(chr(0x07))
            else:
                return default
        else:
            if type == "float":
                pass
            else:
                return inputedData

def stringify(string):
    return '"{}"'.format(string)

def fetchProduct(code):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("""
        select *
        from produkt
        where kod = "{}"
    """.format(code))
    return {
        "code" : cursor._rows[0][0], 
        "price" : float(cursor._rows[0][1])
    }

def updateProduct(product):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("""
        INSERT INTO produkt
        VALUES ("{0}", {1})
        ON DUPLICATE KEY UPDATE cena={1}; 
    """.format(product["code"], product["price"]))
    cnx.commit()
    cursor.close()
    return



#import pdb; pdb.set_trace()

signal.signal(signal.SIGINT, exitWrapper)

cnx = mysql.connector.connect(
    user='root',
    #password=getpass("hasło: "),
    password="wikipass",
    host='localhost',
    database='test'
)

cursor = cnx.cursor(buffered=True)

#kod = input("Kod: ")
#cena = input("Cena: ")

# select = """
# select *
# from produkt
# """

# insert = """
# INSERT INTO produkt
# VALUES ("{0}", {1})
# ON DUPLICATE KEY UPDATE cena={1}; 
# """.format(kod, cena)

#cursor.execute(insert)

cnx.commit()

# cursor.execute(select)
# print(cursor._rows)
print(
    "1 - Edytuj produkt\n"
    "2 - Sprzedaj produkt\n"
    "9 - Debug\n"
    "0 - Wyjdź"
)
while True:
    action = input("?")
    if action == "1":
        inputWrapper(True, None, "kod poduktu?", "code")
    if action == "9":
        import pdb; pdb.set_trace()
        break
    elif action == "0":
        exitWrapper(None, None)
    else:
        print("\aNiepoprawne polecenie!")

exitWrapper(None, None)