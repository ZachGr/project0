CREATE database btc;
use btc;
DROP TABLE IF EXISTS account;
DROP TABLE IF EXISTS psw;

CREATE TABLE account(
id int NOT NULL AUTO_INCREMENT,
fname varchar(255),
lname varchar(255),
btcAmount float,
tdate varchar(255),
PRIMARY KEY (id)
);
show tables;
select * FROM account;
select * FROM psw;

CREATE TABLE psw(
accountID int Not NUll AUTO_INCREMENT,
FOREIGN KEY (accountID) REFERENCES account(id),
pword varchar(255)
);
select * FROM btcPrice;

DROP TABLE IF EXISTS btcPrice;
CREATE TABLE btcPrice(
date varchar(255),
time varchar(255),
open varchar(255)
);