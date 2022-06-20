DROP database test;
CREATE DATABASE test;
use test;
DROP TABLE IF EXISTS psw;
DROP TABLE IF EXISTS account;
CREATE TABLE account(
ID int Not NUll,
firstName varchar(255),
lastName varchar(255),
btcAmount float,
date varchar(255),
PRIMARY KEY (ID)
);

CREATE TABLE psw(
accountID int Not NUll,
FOREIGN KEY (accountID) REFERENCES account(ID),
pword varchar(255)
);
SHOW Tables;
#UPDATE test SET WHERE ID = 1;
#Select * FROM account; 
#Select * FROM psw;
#CASE when action = 'start' then 1 else 0
SELECT LAST(firstName) FROM account;
SELECT * FROM psw WHERE accountID=(SELECT max(accountID) FROM psw);

DROP TABLE IF EXISTS btcPrice;
CREATE TABLE btcPrice(
date varchar(255),
time varchar(255),
open varchar(255)
);
select * FROM btcPrice;