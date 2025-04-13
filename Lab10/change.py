import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432", 
    database="PP",
    user="postgres",
    password="123456789"
)

cur = conn.cursor()

print("Updating data")
search = input("Input name or phone to search: ")

cur.execute("""
    SELECT * FROM phonebook
    WHERE username::text = %s OR phone::text = %s
""", (search, search))
result = cur.fetchone()

if result:
    print(f"Data found: Name: {result[1]}, Number: {result[2]}")
    new_username = input("new name (leave it if you don't want to change): ")
    new_phone = input("new phone number (leave it if you don't want to change): ")

    updated_username = new_username if new_username else result[1]
    updated_phone = new_phone if new_phone else result[2]

    cur.execute("""
        UPDATE phonebook
        SET username = %s, phone = %s
        WHERE id = %s
    """, (updated_username, updated_phone, result[0])) 
    conn.commit()
    print("All good")
else:
    print("no such data in table")

cur.close()
conn.close()
