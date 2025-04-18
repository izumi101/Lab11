import psycopg2

# Подключение к базе данных
conn = psycopg2.connect(
    dbname="PP",
    user="postgres",
    password="123456789",
    host="localhost",
    port="5432"
)
cur = conn.cursor()

# 1. Поиск по шаблону
def search_phonebook(pattern):
    cur.execute("SELECT * FROM search_phonebook(%s);", (pattern,))
    return cur.fetchall()

# 2. Добавить или обновить одного пользователя
def insert_or_update_user(username, phone):
    cur.execute("CALL insert_or_update_user(%s, %s);", (username, phone))
    conn.commit()
    print(f"Пользователь {username} с номером {phone} добавлен/обновлен.")

# 3. Массовое добавление пользователей
def insert_many_users(usernames, phones):
    conn = psycopg2.connect(
        dbname="PP",
        user="postgres",
        password="123456789",
        host="localhost",
        port="5432"
    )
    cur_proc = conn.cursor()
    try:
        cur_proc.execute("CALL insert_many_users(%s, %s);", (usernames, phones))
        conn.commit()
        print("Процедура insert_many_users выполнена.")
        print("Смотри сообщения NOTICE в pgAdmin или логе.")
    except psycopg2.Error as e:
        print(f"Ошибка при выполнении insert_many_users: {e}")
        conn.rollback()
    finally:
        cur_proc.close()
        conn.close()



# 4. Пагинация
def get_paginated(limit, offset):
    cur.execute("SELECT * FROM get_phonebook_paginated(%s, %s);", (limit, offset))
    return cur.fetchall()

# 5. Удаление по имени или номеру
def delete_user(username, phone):
    cur.execute("CALL delete_user(%s, %s);", (username, phone))
    conn.commit()
    print(f"Пользователь {username} с номером {phone} удален.")

if __name__ == "__main__":
    while True:
        print("\nВыберите действие:")
        print("1. Поиск по шаблону")
        print("2. Добавить/обновить пользователя")
        print("3. Массовое добавление пользователей")
        print("4. Пагинация")
        print("5. Удалить пользователя")
        print("0. Выход")

        choice = input("Введите номер действия: ")

        if choice == '1':
            pattern = input("Введите шаблон для поиска: ")
            result = search_phonebook(pattern)
            print("Результаты поиска:")
            for row in result:
                print(row)
        elif choice == '2':
            username = input("Введите имя пользователя: ")
            phone = input("Введите номер телефона: ")
            insert_or_update_user(username, phone)
        elif choice == '3':
            names_str = input("Введите имена пользователей через запятую: ")
            phones_str = input("Введите номера телефонов через запятую: ")
            names = [name.strip() for name in names_str.split(',')]
            phones = [phone.strip() for phone in phones_str.split(',')]
            invalid = insert_many_users(names, phones)
            print("Количество неверных записей:", invalid)
        elif choice == '4':
            limit = int(input("Введите лимит записей на странице: "))
            offset = int(input("Введите смещение (начальная запись): "))
            result = get_paginated(limit, offset)
            print(f"Страница (limit={limit}, offset={offset}):")
            for row in result:
                print(row)
        elif choice == '5':
            username = input("Введите имя пользователя для удаления: ")
            phone = input("Введите номер телефона для удаления: ")
            delete_user(username, phone)
        elif choice == '0':
            break
        else:
            print("Некорректный ввод. Пожалуйста, выберите действие из меню.")

    cur.close()
    conn.close()