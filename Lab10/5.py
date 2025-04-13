import psycopg2

conn = psycopg2.connect(
    host="localhost",
    port="5432", 
    database="PP",
    user="postgres",
    password="123456789"
)

cur = conn.cursor()

print("=== Deleting data from PhoneBook ===")
print("1. Delete by exact name")
print("2. Delete by exact phone number")
choice = input("Choose an option (1/2): ")

if choice == "1":
    name = input("Enter the exact name to delete: ")
    cur.execute("""
        DELETE FROM phonebook
        WHERE username = %s
    """, (name,))
elif choice == "2":
    phone = input("Enter the exact phone number to delete: ")
    cur.execute("""
        DELETE FROM phonebook
        WHERE phone = %s
    """, (phone,))
else:
    print("Invalid choice")
    cur.close()
    conn.close()
    exit()

conn.commit()

if cur.rowcount > 0:
    print("Record deleted successfully.")
else:
    print("No record found to delete.")

cur.close()
conn.close()
