#import sqlTesting as sqlT
import connect as sqlT

again = 'y'
while(again == 'y'):
    sqlT.user(sqlT.my_cursor, sqlT.my_db)
    again = input("Press y to continue and n to quit: ")
    while(again != 'y' and again != 'n'):
        print("Not a correct response")
        again = input("Press y to continue and n to quit: ")


if(again == 'n'):
    print("Thank you, have a nice day!")