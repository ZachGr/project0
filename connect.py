import mysql.connector
import password
from datetime import datetime
import requests
import pandas as pd
from sqlalchemy import create_engine

#creating a class to connect to the database
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


class account(Database):
    #runs select command in sequal with the user inputs
    def select(self, id):
        sql = "SELECT * FROM account ORDER BY id {}".format(id)

        try:
            my_cursor.execute(sql)
            result = my_cursor.fetchall()
            
        except Exception as e:
            return e

        return result

    #Allows user to create an account with the values they inputed
    def insert(self, data):
        sql = "INSERT INTO account (fname, lname,btcAmount,tdate) VALUES ('{}','{}', {}, '{}')".format(data[0], data[1], data[2], data[3])
        try:
            my_cursor.execute(sql)
            my_db.commit()
        except Exception as e:
            return e

    #Allows ADMIN to be able to delete from sql
    def delete(self, table, idName, id):
        sql = "DELETE FROM {} WHERE {} = {}".format(table, idName, id)
        #print(sql)

        try:
            my_cursor.execute(sql)
            my_db.commit()
        except Exception as e:
            return e

#Allows user to update the amount of Bitcoin they have
    def update(self, amount, index):

        sql = "UPDATE account SET btcAmount = {} WHERE ID = {}".format(amount, index)

        #val = (data[0])

        try:
            my_cursor.execute(sql)
            my_db.commit()
            print("Account {} has been updated to have {} bitcoin".format(index, amount))

        except Exception as e:
            return e



db = Database()
ac = account()

#Allows user to choose how they want to continue
def user(cursor, connection):
    choice = ""
    print("Type: \n1 Create a new account\n2 Edit the amount of Bitcoin in your account\n3 See the value of your Bitcoin\n4 See all accounts and Remove accounts (ADMIN ONLY)\n5 To exit")
    choice = input("How would you like to proceed: ")
    #Checks to make sure that the input is an int and a correct option
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
    elif(choice == '5'):
        again = 'n'
        pass
    else:
        print("Not an Option")
        user(cursor, connection)
    #connection.close()

#This asks for user input and then calls the insert class to run the sql code
def inserting():
    fname = input("Enter first name: ")
    #Checking that user input is correct and usable
    while(fname == ''):
        fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    while(lname == ''):
        lname = input("Enter last name: ")
    btcAmount = input("Enter the amount of Bitcoin you own: ")
    it_is = checkInt(btcAmount)
    while(it_is != True):
        btcAmount = input("Enter the amount of Bitcoin you own: ")
        it_is = checkInt(btcAmount)
    tdate =  datetime.now().date()
    #Example of a collection
    data = [fname, lname, btcAmount, tdate]
    ac.insert(data)

    #Allows user to input a password for their account and checks to make sure one has been added
    pword = input("create a password for this account: ")
    while(pword == ''):
        pword = input("create a password for this account: ")

    my_cursor.execute("INSERT INTO psw (pword) VALUES('{}');".format(pword))
    my_db.commit()

    userIndex = my_cursor.execute("SELECT MAX(id) FROM account;")
    userIndex = my_cursor.fetchall()
    userIndex = cleanTxt(userIndex)
    print("Your account ID is {}, make sure you remember this so you can sign in later.".format(userIndex))
    #my_db.commit()


#This asks for user input and then calls the update class to run the sql code
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
            ac.update(amount, index)

#a function that checks the input for passwords when called
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

#A function that removes unwanted characters from strings to be used later in the code
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

#a function to check that the ID enter is an int and exists within a table
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
        print("Account ID entered is not an option")
        checkID = False
    
    return checkID

#Uses an api to get the current price of bitcoin and calculates the users value based off of that
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
            #Compares price of bitcoin from a specific date and compares it to users amount
            print("The amount of bitcoin you have, {}, is worth {}".format(result, currentValueUSD)) 
            #Comparing value from Date#
            date = input("Enter a date to compare the price to between(04-19-2021 and 04-19-2022):\n")
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
                    thenPrice = '${:,.2f}'.format(thenPrice)
                    print("You are down {} from the {} price of {}".format(upDown, date, thenPrice))
                elif(thenPrice < currentValue):
                    upDown = currentValue - thenPrice
                    upDown = '${:,.2f}'.format(upDown)
                    print("You are up {} from the {} price of {}".format(upDown, date, thenPrice))
                else:
                    print("You have neither gained or lost money")

#An API that gets the current price of Bitcoin
def trackBitcoin():
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    price = response["USD"]
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().date()
    return price

#Gets the price for the user inputed date
def priceDate(cursor, connection, date):
    sql = "SELECT open FROM btcPrice WHERE date = '{}';".format(date)
    connection.commit()
    cursor.execute(sql)
    result = cursor.fetchall()
    priceAtDate = cleanTxt(result)
    checkDate = True
    if(priceAtDate == ''):
        print("Date is not in range or was typed incorrectly")
        checkDate = False
    
        return checkDate
    else:
        return (priceAtDate)

def admin(cursor, connection):
    index = 1
    pswCheck=checkPsw(cursor, index)
    if(pswCheck == False):
        pass
    else:
        result = ac.select("ASC")
        for r in result:
            print(r)
        rid = input("Type the account ID of the account you would like to delete: ")
        it_is = checkInt(rid)
        while(it_is != True):
            rid = input("Type the account ID of the account you would like to delete: ")
            it_is = checkInt(rid)
        while(rid == "1"):
            print("Can not delete Admin")
            rid = input("Type the account ID of the account you would like to delete: ")
            it_is = checkInt(rid)
            while(it_is != True):
                rid = input("Type the account ID of the account you would like to delete: ")
                it_is = checkInt(rid)
        IDcheck = checkID(cursor, rid)
        if(IDcheck == False):
            pass
        else:
            ac.delete("psw", "accountid", rid)
            ac.delete("account", "ID", rid)

    
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

#only run if need to fill btcPrice database with data from csv file
def btcdatabase():
    with open("BTC-USD.csv", 'r') as file:
        content = file.readlines()
    header = content[:1]
    rows = content[1:]
    data= pd.read_csv("BTC-USD.csv")
    df = data
    engine = create_engine("mysql+pymysql://root:"+password.myPassword+"@localhost/btc")
    df.to_sql(name = 'btcPrice', con=engine, if_exists='append', index=False)
