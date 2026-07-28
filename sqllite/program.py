import sqlite3

# connect to the database 
connection = sqlite3.connect('example.db')
print(connection)

# mediator to act 
cursor = connection.cursor()
# A cursor is an object that lets you send SQL commands to the database and get the results back.

# create the table 
cursor.execute(
  '''Create Table If Not Exists Employees(
    id Integer Primary Key,
    name Text Not Null,
    age Integer,
    Department Text Not Null
  )
  '''
)

# after the creation of the table you need to commit it
connection.commit()
# make it as a habit after every sql query you need to commit as in git 

# cursor.execute(
#   '''
#   Select * From Employees
#   '''
# )

# Insert into the table 
cursor.executemany(
    """
    INSERT INTO employees (name, age, department)
    VALUES (?, ?, ?)
    """,
    [
        ("Kedar", 22, "Software"),
        ("Rahul", 25, "HR"),
        ("Priya", 24, "Finance"),
        ("Arjun", 27, "Marketing"),
        ("Sneha", 23, "Software"),
        ("Vikram", 30, "Operations"),
        ("Ananya", 26, "Sales"),
        ("Rohit", 29, "IT Support"),
        ("Meera", 28, "Finance"),
        ("Aditya", 31, "Software")
    ]
)
connection.commit()

# Query the data from the table 

# cursor.execute(
#   '''
#   Select * from Employees
#   '''
# )
rows = cursor.fetchall()
# to get all the rows from the select * 
# to print th equeried data 
for row in rows:
  print(row)
# update the table 

cursor.execute(
  '''
  Update Employees
  Set age =21 
  where name = "Kedar"
  '''
)

connection.commit()

cursor.execute(
  '''
  Select age From Employees Where name = "Kedar"
  '''
)

connection.commit()
