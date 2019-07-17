#!/usr/bin/python
# coding=utf-8
# conda install mysql-python
import MySQLdb;
import os;

# db = MySQLdb.connect("182.61.39.220", "root", "Kulu@123", "test")
db = MySQLdb.connect("127.0.0.1", "root", "tpson102304", "global_fire_fighting_platform")
# 使用cursor()方法获取操作游标 
cursor = db.cursor()

# 使用execute方法执行SQL语句
cursor.execute("SELECT VERSION()")
# 使用 fetchone() 方法获取一条数据
data = cursor.fetchone()
cursor.execute("show databases;")
table_list = [tuple[0] for tuple in cursor.fetchall()]
print(table_list)
os._exit(0)

# sql = """CREATE TABLE EMPLOYEE (
#          FIRST_NAME  CHAR(20) NOT NULL,
#          LAST_NAME  CHAR(20),
#          AGE INT,  
#          SEX CHAR(1),
#          INCOME FLOAT )"""
# cursor.execute(sql)
# # SQL 插入语句
# sql = """INSERT INTO EMPLOYEE(FIRST_NAME,
#          LAST_NAME, AGE, SEX, INCOME)
#          VALUES ('Mac', 'Mohan', 20, 'M', 2000)"""
# try:
#    # 执行sql语句
#    cursor.execute(sql)
#    # 提交到数据库执行
#    db.commit()
# except:
#    # Rollback in case there is any error
#    db.rollback()
   
# sql = "INSERT INTO carinfo(name,number) VALUES ('lk2', '33')"
sql = 'INSERT INTO carinfo(name,number) VALUES ("%s", "%s")' % ('lk2', 'lk3')
try:
    row = cursor.execute(sql)
    print(row)
    db.commit()
except Exception, e:
    print("error", e)
    
sql = 'select * from carinfo where id > 5'
cursor.execute(sql)
data = cursor.fetchall()
print data
# print "Database version : %s " % data

# 关闭数据库连接
db.close()
