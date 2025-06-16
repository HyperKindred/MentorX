import pymysql


def connectSQL(p_user = 'Hypercube', p_db = 'mentorx'):
    f_conn = pymysql.connect(
        host='127.0.0.1', 
        port=3306, 
        user=p_user, 
        password='990923', 
        charset='utf8mb4', 
        autocommit=True
    )
    f_cursor = f_conn.cursor()
    f_cursor.execute("use " + p_db)
    return f_conn, f_cursor

def closeSQL(p_conn, p_cursor):
    p_cursor.close()
    p_conn.close()

def f_getLearningStatsByPerson(user_id):
    student = {}
    chapters = []
    chapter = {}
    conn, cursor = connectSQL()
    chapter_map_correctness = {}
    chapter_map_aiFrequence = {}
    sql = f"select name from user where user_id = {user_id};"
    cursor.execute(sql)
    name = cursor.fetchone()[0]
    student["id"] = user_id
    student["name"] = name

    sql = f"select chapter_id, COUNT(*) from practice_history group by chapter_id where check = 'T';"
    cursor.execute(sql)
    right = cursor.fetchall()
    for row in right:         
        chapter_map_correctness[row[0]] = row[1]
    sql = f"select chapter_id, COUNT(*) from practice_history group by chapter_id;"
    cursor.execute(sql)
    total = cursor.fetchall()
    for row in total:
        if row[0] in chapter_map_correctness.keys():
            chapter_map_correctness[row[0]] = chapter_map_correctness[row[0]] / row[1]
        else:
            chapter_map_correctness[row[0]] = 0
    sql = f"select chapter_id, COUNT(*) from communicate_history group by chapter_id where user_id = {user_id};"
    cursor.execute(sql)
    total_1 = cursor.fetchall()
    for row in total_1:
        chapter_map_aiFrequence[row[0]] = int(row[1] / 2)

    chapter_list = list(chapter_map_aiFrequence.keys() | chapter_map_aiFrequence.keys())
    for cahpter_id in chapter_list:
        sql = f"select name from chapter where id = {cahpter_id};"
        cursor.execute(sql)
        chapter_name = cursor.fetchone()[0]
        chapter["name"] = chapter_name
        if cahpter_id in chapter_map_aiFrequence.keys():
            chapter["AiFrequence"] = chapter_map_aiFrequence[cahpter_id]
        else:
            chapter["AiFrequence"] = -1

        if cahpter_id in chapter_map_correctness.keys():
            chapter["correctness"] = chapter_map_correctness[cahpter_id]
        else:
            chapter["correctness"] = -1
        chapters.append(chapter)
    
    student["chapters"] = chapters
    closeSQL(conn, cursor)
    return student