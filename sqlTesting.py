from venv import create
import pymysql
import password
import requests
from datetime import datetime
import pandas as pd
from pandas.io import sql
from sqlalchemy import create_engine

def data():
    with open("BTC-USD.csv", 'r') as file:
        content = file.readlines()
    header = content[:1]
    rows = content[1:]
    data= pd.read_csv("BTC-USD.csv")
    df = data
    engine = create_engine("mysql+pymysql://root:"+password.myPassword+"@localhost/btc")
    df.to_sql(name = 'btcPrice', con=engine, if_exists='append', index=False)
   

def trackBitcoin():
    url = "https://min-api.cryptocompare.com/data/price?fsym=BTC&tsyms=USD,JPY,EUR"
    response = requests.get(url).json()
    price = response["USD"]
    time = datetime.now().strftime("%H:%M:%S")
    date = datetime.now().date()
    return price



def sql_connect():
    connection = pymysql.connect(host='localhost',
                                user='root',
                                password=password.myPassword,
                                db="test"
                                )
    cursor = connection.cursor()
    
    choice = ""
    
    print("Type: \n1 for creating a new account\n2 to access your account\n3 to see the value of your Bitcoin\n4 ADMIN ONLY")
    choice = int(input("How would you like to proceed: "))
    if (choice == 1):
        insert(cursor, connection)
    elif(choice == 2):
        update(cursor, connection)
    elif(choice == 3):
        value(cursor, connection)
    elif(choice == 4):
        admin(cursor, connection)
    connection.close()

def admin(cursor, connection):
    index = 1
    pswCheck=psw(cursor, index)
    if(pswCheck == False):
        pass
    else:
        sql = "SELECT * FROM account;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for r in result:
            print(r)
        rid = input("Type the index of which account you want to delete: ")
        while(rid == "1"):
            print("Can not delete Admin")
            rid = input("Type the index of which account you want to delete: ")
        checkID(cursor, rid)
        sql = "DELETE FROM psw WHERE accountID = {};".format(rid)
        cursor.execute(sql)
        connection.commit()
        sql = "DELETE FROM account WHERE ID = {};".format(rid)
        cursor.execute(sql)
        connection.commit()
    
    
    
        sql = "SELECT * FROM account;"
        cursor.execute(sql)
        result = cursor.fetchall()
        for r in result:
            print(r)
    

    
    

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

def insert(cursor, connection):
    sql = "SELECT * FROM account;"
    cursor.execute(sql)
    number = cursor.fetchall()
    j=1
    for i in number:
        j+=1 
    if(j>1):
        sql = "SELECT MAX(ID) FROM account;"
        cursor.execute(sql)
        print("2")
        number = cursor.fetchall()
        number = cleanTxt(number)
        #print(number)
        j = int(number)
        j+=1
    index = j
    fname = input("Enter first name: ")
    lname = input("Enter last name: ")
    btcAmount = input("Enter the amount of bitcoins do you own: ")
    tdate =  datetime.now().date()
    pword = input("create a password for this account: ")
    cursor.execute("INSERT INTO account VALUES({}, '{}', '{}', {}, '{}');".format(index, fname, lname, btcAmount, tdate))
    connection.commit()
    cursor.execute(sql)
    print("The index for your account is {}, make sure you remember this so you can sign in later.".format(index))

    #result = cursor.fetchall()
    #for i in result:
    #    print(i)

    cursor.execute("INSERT INTO psw VALUES({}, '{}');".format(index, pword))
    connection.commit()
    cursor.execute(sql)

def select(cursor, connection, index):
    sql = "SELECT * FROM account WHERE ID = {};".format(index)
    cursor.execute(sql)
    result = cursor.fetchall()
    print(result)


def update(cursor, connection):
    index = input("What is your account ID? ")
    IDcheck = checkID(cursor, index)
    #print(IDcheck)
    if(IDcheck == False):
        pass
    elif(IDcheck == True):
        #PASSWORD
        check=psw(cursor, index)
        #print(check)
        if(check == False):
            pass
        else:
            deposit = input("How much bitcoin do you now own? ")
            sql = "UPDATE account SET btcAmount='{}' WHERE ID={};".format(deposit, index) 
            cursor.execute(sql)
            connection.commit()
            select(cursor, connection, index)

def value(cursor, connection):
    index = input("What is your account ID? ")
    IDcheck = checkID(cursor, index)
    #print(check)
    if(IDcheck == False):
        pass
    elif(IDcheck == True):
        check=psw(cursor, index)
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


def cleanTxt(tuple):
    string = str(tuple)
    string = string.replace('"','')
    string = string.replace('(','')
    string = string.replace(')','')
    string = string.replace(',','')
    string = string.replace("'",'')
    return string

def psw(cursor, index):
    check = False
    pwordAttempt = input("What is the password for this account? ")
    sql = "SELECT pword AS String FROM psw WHERE accountID =({});".format(index)
    cursor.execute(sql)
    result = cursor.fetchall()
    result = cleanTxt(result)
    #print(result)
    if(pwordAttempt != result):
        print("Incorrect Password")
        
    if(pwordAttempt == result):
        check = True
    
    return check

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


data()
#sql_connect()