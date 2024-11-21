import aiomysql
import asyncio


async def main():
    conn = await aiomysql.connect(host='localhost', port=3306, user='user', password='password', db='test_db')

    async with conn.cursor() as cur:
        while True:
            print('''Выберите действие: 
1 - SELECT
2 - DELETE
3 - CREATE
4 - INSERT INTO
5 - SHOW 
6 - USE
0 - Выход''')

            q = int(input("Введите номер: "))
            if q == 0:
                print("Выход...")
                break

            if q == 1:  # SELECT
                columns = input('''Напишите, что вы хотите выбрать (например: *, column_name): ''')
                table = input('''Напишите имя таблицы, откуда вы хотите выбрать: ''')
                question = f"SELECT {columns} FROM {table};"

            elif q == 2:  # DELETE
                table = input('''Введите название таблицы, из которой хотите удалить: ''')
                condition = input('''Введите условие удаления (например: id=1): ''')
                question = f"DELETE FROM {table} WHERE {condition};"

            elif q == 3:  # CREATE
                obj_type = input('''Выберите объект:
1 - DATABASE
2 - TABLE

Введите номер: ''')
                if obj_type == '1':
                    db_name = input('''Введите имя базы данных: ''')
                    question = f"CREATE DATABASE {db_name};"
                elif obj_type == '2':
                    table_name = input('''Введите имя таблицы: ''')
                    columns = input('''Введите столбцы и их типы (например: id INT PRIMARY KEY, name VARCHAR(100)): ''')
                    question = f"CREATE TABLE {table_name} ({columns});"

            elif q == 4:  # INSERT INTO
                table = input('''Введите название таблицы для вставки данных: ''')
                columns = input('''Введите столбцы (например: column1, column2): ''')
                values = input('''Введите значения (например: value1, value2): ''')
                question = f"INSERT INTO {table} ({columns}) VALUES ({values});"

            elif q == 5:  # SHOW
                obj_type = input('''Выберите объект:
1 - DATABASES
2 - TABLES

Введите номер: ''')
                if obj_type == '1':
                    question = "SHOW DATABASES;"
                elif obj_type == '2':
                    question = "SHOW TABLES;"

            elif q == 6:  # USE
                db_name = input('''Введите имя базы данных для использования: ''')
                question = f"USE {db_name};"

            else:
                print("Такого номера нет!")
                continue

            print('Ваш SQL-запрос:', question)
            prequestion = int(input('''Всё верно?
1 - Да
2 - Нет

Введите номер: '''))
            if prequestion == 1:
                await cur.execute(question)
                if q == 1 or q == 5:
                    result = await cur.fetchall()
                    print("Результаты запроса:", result)
                elif q == 4:
                    await conn.commit()
                    result = await cur.fetchall()
                    print("Результаты запроса:", result)
                else:
                    await conn.commit()
                    print("Запрос выполнен успешно.")

            else:
                print('Давайте заново!')

    conn.close()


if __name__ == "__main__":
    asyncio.run(main())
