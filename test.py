import sqlite3

connection = sqlite3.connect('data.db')

#create cursor/pointer
cursor = connection.cursor()

#Create table users
create_table = "CREATE TABLE users (id int, username text, password text)"
cursor.execute(create_table)

# Insert user #1
user = (1, "Jose", "asdf")
insert_query = "INSERT INTO users VALUES (?, ?, ?)"
cursor.execute(insert_query, user)

# Insert user #2, & 3
users = [
    (2, 'jj', 'asdf'),
    (3, 'kk', 'asdf')
]
cursor.executemany(insert_query, users)

select_query = "SELECT * FROM users"
for row in cursor.execute(select_query):
    print(row)

connection.commit()

connection.close()
