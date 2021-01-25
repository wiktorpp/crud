import mysql.connector
import signal
import sys
from getpass import getpass
debug = True

cnx = mysql.connector.connect(
    user='root',
    #password=getpass("hasło: "),
    password="wikipass",
    host='localhost',
    database='test'
)

def exitWrapper(sig=None, frame=None):
    cnx.commit()
    cnx.close()
    print('exited')
    exit()

def validateInput(string, dataType=None):
    if string == "":
        if dataType == "str":
            return ""
        else:
            return True
    else:
        if dataType == "float":
            string = string.replace(",", ".")
            try: return float(string)
            except:
                return None
        elif dataType == "id":
            if isIdValid(string) == True:
                return string
            else:
                return None
        else:
            if string == None:
                return None
            else:
                return string

def inputWrapper(
    prompt="", 
    default=None, 
    dataType=None, 
    force=False
):
    if default == None:
        prompt = "{}?".format(prompt)
    else:
        prompt = "{}({})?".format(prompt, default)

    while True:
        if default == None:
            force = True
        if dataType == "id":
            string = input(prompt).upper()
        else:
            string = input(prompt)
        string = validateInput(
            string = string,
            dataType = dataType
        )

        if string == True and not force:
            return default
        elif string == None or string == True:
            sys.stdout.write(chr(0x07))
            continue
        else:
            return string

def isIdValid(id):
    return len(id) == 3 and id.isalpha() and id.isupper()

def fetchProduct(id):
    cursor = cnx.cursor(buffered=True)
    cursor.execute("""
        select *
        from produkt
        where kod = "{}"
    """.format(id))
    try:
        return {
            "id" : cursor._rows[0][0], 
            "price" : float(cursor._rows[0][1])
        }
    except:
        return {
            "id" : id,
            "price" : None
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

def printProduct(product):
    print(
        (
            "Kod: {}\n"
            "Cena: {}"
        ).format(product["id"], product["price"])
    )

#import pdb; pdb.set_trace()

signal.signal(signal.SIGINT, exitWrapper)

def editProductAction():
    id = inputWrapper(
        prompt = "kod",
        dataType = "id",
        force = True
    )
    product = fetchProduct(id)
    product["price"] = inputWrapper(
        prompt = "cena",
        default = product["price"],
        dataType = "float"
    )
    if debug: print(product)
    updateProduct(product)
    print("Zaaktualizowano!")

def printProductAction():
    id = inputWrapper(
        prompt = "kod",
        dataType = "id",
        force = True
    )
    product = fetchProduct(id)
    print(product)
    printProduct(product)

def mainAction():
    print(
        "1 - Edytuj produkt\n"
        "2 - Znajdź produkt\n"
        "3 - Sprzedaj produkt\n"
        "9 - Debug\n"
        "0 - Wyjdź"
    )
    while True:
        action = input("?")

        if action == "1":
            while True:
                editProductAction()

        if action == "2":
            printProductAction()

        elif action == "9":
            import pdb; pdb.set_trace()
            break

        elif action == "0":
            exitWrapper(None, None)
            
        else:
            print("\aNiepoprawne polecenie!")

if __name__ == '__main__':
    mainAction()
    exitWrapper(None, None)