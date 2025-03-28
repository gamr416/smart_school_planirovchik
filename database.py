import sqlite3


def register_new_user(user_id):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    print(user_id)
    command = cursor.execute(
        f"""CREATE TABLE tasks{user_id}("id" INTEGER, "tag" text, "date" text, "description" text, "done" text, PRIMARY KEY("id" AUTOINCREMENT))"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()


def add_task(user_id,  tag, data, description):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    print(data)
    command = cursor.execute(
        f"""INSERT INTO tasks{user_id}(tag, date, description) VALUES('{tag}', '{data}', '{description}')"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()


def get_task(user_id, task_id):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT * FROM tasks{user_id} WHERE id={task_id}"""
    ).fetchall()
    cursor.close()
    con.close()
    return command[0]


def get_tagged_tasks(user_id, tag):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT * FROM tasks{user_id} WHERE tag='{tag}'"""
    ).fetchall()
    cursor.close()
    con.close()
    return command


def get_all_tasks(user_id):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT description, date FROM tasks{user_id}"""
    ).fetchall()
    cursor.close()
    con.close()
    return command


def mark_as_important(user_id, task_id, description):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""UPDATE tasks{user_id} SET description = '⭐{description}' WHERE id = {task_id}"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()


def delete_task(user_id, date, description):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    task_id = get_task_by_desc(user_id, description, date)
    command = cursor.execute(
        f"""DELETE FROM tasks{user_id} WHERE id = {task_id}"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()

def get_task_by_desc(user_id, description, date):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    print(description, 123, date,    781479401864389)
    command = cursor.execute(
        f"""SELECT id FROM tasks{user_id} WHERE description = '{description}' AND date = '{date}'"""
    ).fetchall()
    cursor.close()
    con.close()
    return command[0][0]


def mark_as_done(user_id, date, description):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    task_id = get_task_by_desc(user_id, description, date)
    command = cursor.execute(
        f"""UPDATE tasks{user_id} SET description = '✅{description}' WHERE id = {task_id}"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()

def get_all_tables():
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT name FROM sqlite_master WHERE type='table'"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()
    return command[1:]
# print(get_all_tables())


def get_dates_and_desc(table):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT date FROM {table}"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()
    return command

def get_id_and_desc_by_date(date, table):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT id, description FROM {table}"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()
    return command


# print(get_all_tables())print([get_dates_and_desc(i[0]) for i in get_all_tables()])
