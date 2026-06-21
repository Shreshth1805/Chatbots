import sqlite3

## Connect to SQLite
connection=sqlite3.connect("student.db")

## create a cursor object to insert record,create table:
cursor=connection.cursor()

## Create the Table:
table_info="""
CREATE TABLE IF NOT EXISTS Student(NAME VARCHAR(25), CLASS VARCHAR(25), SECTION VARCHAR(25),MARKS INT)
"""
cursor.execute(table_info)

## Inserting Records:
cursor.execute('''INSERT INTO Student VALUES("Krish","Data Science","A",90)''')
cursor.execute('''INSERT INTO Student VALUES("John","Data Science","B",100)''')
cursor.execute('''INSERT INTO Student VALUES("Mukesh","Data Science","A",76)''')
cursor.execute('''INSERT INTO Student VALUES("Jacob","DEVOPS","A",50)''')
cursor.execute('''INSERT INTO Student VALUES("Dipesh","DEVOPS","A",35)''')

## Display all the records:
print("The inserted records are:")
data=cursor.execute('''SELECT * FROM Student''')
for row in data:
    print(row)

## Commiting the changes:
connection.commit()
connection.close()    