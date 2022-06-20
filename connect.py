import mysql.connector
import password
from datetime import datetime
import requests


class Database:
    my_db = my_cursor = None

    def __init__(self):
        global my_db, my_cursor
        my_db = mysql.connector.connect(
            host="localhost",
            user="root",
            password=password.myPassword,
            database="btc"
        )
        my_cursor = my_db.cursor()
        #my_cursor.commit()

    """ def __del__(self):
        my_db.commit() """


class account(Database):

    def select(self, id):
        sql = "SELECT * FROM account ORDER BY id {}".format(id)

        try:
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
            
        except Exception as e:
            return e

        #for r in result:
        return result

    def insert(self, data):

        sql = "INSERT INTO account (fname, lname,btcAmount,tdate) VALUES ('{}','{}', {}, '{}')".format(data[0], data[1], data[2], data[3])
        try:
            my_cursor.execute(sql)
            my_db.commit()
        except Exception as e:
            return e

        #return my_cursor.lastrowid

    def delete(self, table, idName, id):
        sql = "DELETE FROM {} WHERE {} = {}".format(table, idName, id)
        print(sql)

        try:
            my_cursor.execute(sql)
            my_db.commit()
        except Exception as e:
            return e

    def update(self, amount, index):

        sql = "UPDATE account SET btcAmount = {} WHERE ID = {}".format(amount, index)

        #val = (data[0])

        try:
            my_cursor.execute(sql)
            my_db.commit()

        except Exception as e:
            return e



db = Database()
ac = account()

def user(cursor, connection):
    choice = ""
    print("Type: \n1 for creating a new account\n2 to access your account\n3 to see the value of your Bitcoin\n4 ADMIN ONLY")
    choice = input("How would you like to proceed: ")
    it_is = checkInt(choice)
    while(it_is != True):
        choice = input("How would you like to proceed: ")
        it_is = checkInt(choice)
    if (choice == '1'):
        inserting()
    elif(choice == '2'):
        updating()
    elif(choice == '3'):
        value(cursor, connection)
    elif(choice == '4'):
        admin(cursor, connection)
    else:
        print("Not an Option")
    #connection.close()

#THIS IS INSERTING
def inserting():
    fname = input("Enter first name: ")
    while(fname == ''):
        fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    while(lname == ''):
        lname = input("Enter last name: ")
    btcAmount = input("Enter the amount of bitcoins do you own: ")
    #btcAmount = int(btcAmount)
    it_is = checkInt(btcAmount)
    while(it_is != True):
        btcAmount = input("Enter the amount of bitcoins do you own: ")
        it_is = checkInt(btcAmount)
    tdate =  datetime.now().date()
    data = [fname, lname, btcAmount, tdate]
    ac.insert(data)

    #Password
    pword = input("create a password for this account: ")
    while(pword == ''):
        pword = input("create a password for this account: ")

    my_cursor.execute("INSERT INTO psw (pword) VALUES('{}');".format(pword))
    my_db.commit()

    userIndex = my_cursor.execute("SELECT MAX(id) FROM account;")
    userIndex = my_cursor.fetchall()
    userIndex = cleanTxt(userIndex)
    print("The index for your account is {}, make sure you remember this so you can sign in later.".format(userIndex))
    #my_db.commit()


#THIS IS UPDATING
def updating():
    index = input("Type in your account ID: ")
    it_is = checkInt(index)
    while(it_is != True):
        index = input("Type in your account ID: ")
        it_is = checkInt(index)
    idCheck = checkID(my_cursor, index)
    if(idCheck == False):
        pass
    else:
        pCheck = checkPsw(my_cursor, index)
        if(pCheck == False):
            pass
        else:
            amount = input("How much bitcoin do you now have? ")
            it_is = checkInt(amount)
            while(it_is != True):
                amount = input("How much bitcoin do you now have? ")
                it_is = checkInt(amount)
            print("yo")
            ac.update(amount, index)

def checkPsw(cursor, index):
    pswcheck = False
    pwordAttempt = input("What is the password for this account? ")
    sql = "SELECT pword AS String FROM psw WHERE accountID =({});".format(index)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = cleanTxt(result)
    #print(result)
    if(pwordAttempt != result):
        print("Incorrect Password")
        
    if(pwordAttempt == result):
        pswcheck = True
    
    return pswcheck

def cleanTxt(tuple):
    string = str(tuple)
    string = string.replace('"','')
    string = string.replace('(','')
    string = string.replace(')','')
    string = string.replace(',','')
    string = string.replace("'",'')
    string = string.replace("]",'')
    string = string.replace("[",'')
    return string


def checkID(cursor, index):
    checkID = False
    
    sql = "SELECT pword AS String FROM psw WHERE accountID =({});".format(index)
    cursor.execute(sql)
    result = cursor.fetchall()
    #print(result)
    result = cleanTxt(result)
    #print(result)
    checkID = True
    #print(result)
    if(result == ''):
        print("index does not exist")
        checkID = False
    
    return checkID

def value(cursor, connection):
    index = input("What is your account ID? ")
    it_is = checkInt(index)
    while(it_is != True):
        index = input("Type in your account ID: ")
        it_is = checkInt(index)
    IDcheck = checkID(cursor, index)
    #print(check)
    if(IDcheck == False):
        pass
    elif(IDcheck == True):
        check=checkPsw(cursor, index)
        if(check == False):
            pass
        else:
            sql = "SELECT btcAmount FROM account WHERE ID = {};".format(index)
            cursor.execute(sql)
            result = cursor.fetchall()
            result = cleanTxt(result)
            result = float(result)
            currentValue = trackBitcoin() * result
            currentValueUSD = '${:,.2f}'.format(currentValue)
            print("You currently have {} worth of Bitcoin".format(currentValueUSD)) 
            #Comparing value from Date##############
            date = input("Enter a date to compare the price to between(04-19-2021 and 04-19-2022):\n")
            #print(checkDate(cursor, connection, date))
            date = str(date)
            thenPrice = priceDate(cursor, connection, date)
            if(thenPrice == False):
                pass
            else:
                thenPrice = float(thenPrice)
                thenPrice = thenPrice*result
                if(thenPrice > currentValue):
                    upDown = thenPrice - currentValue
                    upDown = '${:,.2f}'.format(upDown)
                    print("You are down {} from {}".format(upDown, date))
                elif(thenPrice < currentValue):
                    upDown = currentValue - thenPrice
                    upDown = '${:,.2f}'.format(upDown)
                    print("You are up {} from {}".format(upDown, date))
                else:
                    print("You have neither gained or lost money")

def trackBitcoin():
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    price = response["USD"]
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().date()
    return price

def priceDate(cursor, connection, date):
    #sql = "SELECT open FROM btcprice WHERE;"
    sql = "SELECT open FROM btcPrice WHERE date = '{}';".format(date)
    # WHERE date = {};".format(date)
    connection.commit()
    cursor.execute(sql)
    result = cursor.fetchall()
    #print(result)
    #result = result[0]
    priceAtDate = cleanTxt(result)
    checkDate = True
    #print(result)
    if(priceAtDate == ''):
        print("Date is not in range or was typed incorrectly")
        checkDate = False
    
        return checkDate
    else:
        return (priceAtDate)

def admin(cursor, connection):
    #ac = account()
    index = 1
    pswCheck=checkPsw(cursor, index)
    if(pswCheck == False):
        pass
    else:
        result = ac.select("ASC")
        for r in result:
            print(r)
        rid = input("Type the index of which account you want to delete: ")
        it_is = checkInt(rid)
        while(it_is != True):
            rid = input("Type the index of which account you want to delete: ")
            it_is = checkInt(rid)
        while(rid == "1"):
            print("Can not delete Admin")
            rid = input("Type the index of which account you want to delete: ")
            it_is = checkInt(rid)
            while(it_is != True):
                rid = input("Type the index of which account you want to delete: ")
                it_is = checkInt(rid)
        IDcheck = checkID(cursor, rid)
        if(IDcheck == False):
            pass
        else:
            ac.delete("psw", "accountid", rid)
            ac.delete("account", "ID", rid)
            #sql = "DELETE FROM psw WHERE accountID = {};".format(rid)
            #cursor.execute(sql)
            #connection.commit()
            #sql = "DELETE FROM account WHERE ID = {};".format(rid)
            #cursor.execute(sql)
            #connection.commit()

    
            sql = "SELECT * FROM account;"
            cursor.execute(sql)
            result = cursor.fetchall()
            for r in result:
                print(r)

def checkInt(x):
    try:
        float(x)
        it_is = True
    except ValueError:
        it_is = False
    return it_is
#inserting()
#updating()
#value(my_cursor, my_db)
#user()