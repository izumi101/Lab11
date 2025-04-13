import psycopg2
import csv

conn = psycopg2.connect(database="PP", user="postgres", password="123456789", host="localhost", port="5432")
cur = conn.cursor()

with open('contacts.csv', 'r') as f:
    reader = csv.reader(f)
    next(reader)  
    for row in reader:
        cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s)", (row[0], row[1]))

conn.commit()
cur.close()
conn.close()