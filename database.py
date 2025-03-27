import sqlite3


def register_new_user(user_id):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    print(user_id)
    command = cursor.execute(
        f"""INSERT INTO users(id) VALUES('{user_id}')"""
    ).fetchall()
    command = cursor.execute(
        f"""CREATE TABLE tasks{user_id}("id" INTEGER, "tag" text, "data" text, "description" text, "cycle" text, PRIMARY KEY("id" AUTOINCREMENT))"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()


def add_task(user_id,  tag, data, description, cycle):
    con = sqlite3.connect('DB')
    cursor = con.cursor()
    print(data)
    command = cursor.execute(
        f"""INSERT INTO tasks{user_id}(tag, data, description, cycle) VALUES('{tag}', '{data}', '{description}', '{cycle}')"""
    ).fetchall()
    con.commit()
    cursor.close()
    con.close()


def get_task(user_id, task_id):
    con = sqlite3.connect('db/database1')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT * FROM task{user_id} WHERE id={task_id}"""
    ).fetchall()
    cursor.close()
    con.close()
    return command[0]


def delete_task(data):
    pass


def get_tagged_tasks(user_id, tag):
    con = sqlite3.connect('db/database1')
    cursor = con.cursor()
    command = cursor.execute(
        f"""SELECT * FROM task{user_id} WHERE tag='{tag}'"""
    ).fetchall()
    cursor.close()
    con.close()
    return command[0]