#import sqlTesting as sqlT
from matplotlib.pyplot import connect
import connect as sqlT
import os


#Runs through connect.py until the user is done
again = 'y'
while(again == 'y'):
    os.system('CLS')
    sqlT.user(sqlT.my_cursor, sqlT.my_db)
    again = input("Press y to continue and n to quit: ")
    while(again != 'y' and again != 'n'):
        print("Not a correct response")
        again = input("Press y to continue and n to quit: ")


if(again == 'n'):
    print("Thank you, have a nice day!")