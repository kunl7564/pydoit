#!/usr/bin/python
# coding=utf-8
# conda install mysql-python
import MySQLdb;
import os;

# return db
def connect(ip, username, password, dbname):
    return MySQLdb.connect(ip, username, password, dbname)

def close(db):
    db.close()

def removeTable(db, tableName):
    db.cursor().execute("DROP TABLE IF EXISTS %s" % tableName)
    
def execSql(db, sql):
    cursor = db.cursor()
    try:
        cursor.execute(sql)
        cursor.commit()
    except:
        cursor.rollback()

def fetchAll(db, tableName):
    cursor = db.cursor()
    try:
        results = cursor.execute("select * from %s" % tableName)
        return results
    except:
        print("fetch error")
        
        
# db = connect("127.0.0.1", "root", "tpson102304", "global_fire_fighting_platform")
# results = fetchAll(db, "user")
# print(results)

db = connect("47.111.170.106", "root", "Tpson@102304", "gfs_dev")
results = fetchAll(db, "user0")
print(results)

