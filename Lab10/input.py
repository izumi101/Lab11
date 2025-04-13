import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    host="localhost",
    port="5432",  
    database="PP",
    user="postgres",
    password="123456789"
)

cur = conn.cursor()

while True:
    username = input("Input name or exit to leave")
    if username.lower() == 'exit':
        break

    phone = input("Input phone number")


    cur.execute("INSERT INTO phonebook (username, phone) VALUES (%s, %s);", (username, phone))
    conn.commit()
    print("data has been updated!\n")


cur.close()
conn.close()
