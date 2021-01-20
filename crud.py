import mysql.connector
import signal
import sys
from getpass import getpass

def exitWrapper(sig, frame):
    cnx.commit()
    cnx.close()
    print('exited')
    exit()

def inputWrapper(force=False, default=None, prompt="?", dataType=None):
    while True:
        inputedData = input(prompt)
        if inputedData == "":
            if force:
                sys.stdout.write(chr(0x07))
                continue
            else:
                return default
        else:
            if dataType == "float":
                inputedData = inputedData.replace(",", ".")
                try: float(inputedData)
                except:
                    sys.stdout.write(chr(0x07))
                    continue
                else:
                    return inputedData
            elif dataType == "id":
                if isIdValid(inputedData) == True:
                    return inputedData
                else:
                    sys.stdout.write(chr(0x07))
            else:
                return inputedData

def stringify(string):
    return '"{}"'.format(string)

def isIdValid(id):
    return len(id) == 3 and id.isalpha() and id.isupper()

def fetchProduct(id):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("""
        select *
        from produkt
        where kod = "{}"
    """.format(id))
    return {
        "id" : cursor._rows[0][0], 
        "price" : float(cursor._rows[0][1])
    }

def updateProduct(product):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("""
        INSERT INTO produkt
        VALUES ("{0}", {1})
        ON DUPLICATE KEY UPDATE cena={1}; 
    """.format(product["id"], product["price"]))
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

print(
    "1 - Edytuj produkt\n"
    "2 - Sprzedaj produkt\n"
    "9 - Debug\n"
    "0 - Wyjdź"
)
while True:
    action = input("?")

    if action == "1":
        while True:
            id = inputWrapper(
                force = True, 
                prompt = "kod?",
                dataType = "id",
            )
            product = fetchProduct(id)
            product["price"] = inputWrapper(
                force = True,
                prompt = "cena({})?".format(product["price"]),
                dataType = "float"
            )
            updateProduct(product)
            print("Zaaktualizowano!")

    elif action == "9":
        import pdb; pdb.set_trace()
        break

    elif action == "0":
        exitWrapper(None, None)
        
    else:
        print("\aNiepoprawne polecenie!")

exitWrapper(None, None)