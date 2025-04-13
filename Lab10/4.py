import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432", 
    database="PP",
    user="postgres",
    password="123456789"
)

cur = conn.cursor()

print("=== PhoneBook Search ===")
print("1. Search by exact name")
print("2. Search by exact phone number")
print("3. Search by part of name or phone number")
choice = input("Choose an option (1/2/3): ")

if choice == "1":
    name = input("Enter the exact name: ")
    cur.execute("""
        SELECT * FROM phonebook
        WHERE username = %s
    """, (name,))
elif choice == "2":
    phone = input("Enter the exact phone number: ")
    cur.execute("""
        SELECT * FROM phonebook
        WHERE phone = %s
    """, (phone,))
elif choice == "3":
    text = input("Enter part of the name or phone number: ")
    pattern = f"%{text}%"
    cur.execute("""
        SELECT * FROM phonebook
        WHERE username ILIKE %s OR phone ILIKE %s
    """, (pattern, pattern))
else:
    print("Invalid choice")
    cur.close()
    conn.close()
    exit()

results = cur.fetchall()

if results:
    print("\n🔎 Found results:")
    for row in results:
        print(f"ID: {row[0]}, Name: {row[1]}, Phone: {row[2]}")
else:
    print("No results found.")

cur.close()
conn.close()
