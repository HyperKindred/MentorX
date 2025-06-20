import pymysql


def connectSQL(p_user = 'root', p_db = 'mentorx'):
    f_conn = pymysql.connect(
        host='127.0.0.1', 
        port=3306, 
        user=p_user, 
        password='123456', 
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
    conn, cursor = connectSQL()
    chapter_map_correctness = {}
    chapter_map_aiFrequence = {}
    sql = "SELECT name FROM user WHERE user_id = %s;"
    cursor.execute(sql, (user_id,))
    name = cursor.fetchone()[0]
    student["id"] = user_id
    student["name"] = name

    sql = "SELECT chapter_id, COUNT(*) FROM practice_history WHERE check = 'T' AND student_id = %s GROUP BY chapter_id;"
    cursor.execute(sql, (user_id,))
    right = cursor.fetchall()
    for row in right:         
        chapter_map_correctness[row[0]] = row[1]
    
    sql = "SELECT chapter_id, COUNT(*) FROM practice_history WHERE student_id = %s GROUP BY chapter_id;"
    cursor.execute(sql, (user_id,))
    total = cursor.fetchall()
    for row in total:
        if row[0] in chapter_map_correctness.keys():
            chapter_map_correctness[row[0]] = chapter_map_correctness[row[0]] / row[1]
        else:
            chapter_map_correctness[row[0]] = 0
    
    sql = "SELECT chapter_id, COUNT(*) FROM communicate_history WHERE user_id = %s GROUP BY chapter_id;"
    cursor.execute(sql, (user_id,))
    total_1 = cursor.fetchall()
    for row in total_1:
        chapter_map_aiFrequence[row[0]] = int(row[1] / 2)

    chapter_list = list(set(chapter_map_correctness.keys()) | set(chapter_map_aiFrequence.keys()))
    for chapter_id in chapter_list:
        chapter = {}
        sql = "SELECT name FROM chapter WHERE id = %s;"
        cursor.execute(sql, (chapter_id,))
        chapter_name = cursor.fetchone()[0]
        chapter["name"] = chapter_name
        chapter["AiFrequence"] = chapter_map_aiFrequence.get(chapter_id, -1)
        chapter["correctness"] = chapter_map_correctness.get(chapter_id, -1)
        chapters.append(chapter)
    
    student["chapters"] = chapters
    closeSQL(conn, cursor)
    return student

def f_getLearningStatsByChapter(chapter_id):
    conn, cursor = connectSQL()
    chapter = {}
    sql = "SELECT name FROM chapter WHERE id = %s;"
    cursor.execute(sql, (chapter_id,))
    chapter["name"] = cursor.fetchone()[0]
    
    sql = "SELECT COUNT(*) FROM communicate_history WHERE chapter_id = %s;"
    cursor.execute(sql, (chapter_id,))
    chapter["AiFrequence"] = cursor.fetchone()[0] / 2
    
    sql = "SELECT COUNT(*) FROM practice_history WHERE chapter_id = %s;"
    cursor.execute(sql, (chapter_id,))
    total = cursor.fetchone()[0]
    
    sql = "SELECT COUNT(*) FROM practice_history WHERE chapter_id = %s AND check = 'T';"
    cursor.execute(sql, (chapter_id,))
    right = cursor.fetchone()[0]
    
    chapter["correctness"] = right / total if total > 0 else 0
    
    closeSQL(conn, cursor)
    return chapter

def sign_in_db(phone_number):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT password, user_id, type, name, gender FROM user WHERE phone_number = %s;"
        cursor.execute(sql, (phone_number,))
        return cursor.fetchone()
    finally:
        closeSQL(conn, cursor)

def register_db(phone_number, password, user_type, name, gender):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT phone_number FROM user WHERE phone_number = %s;"
        cursor.execute(sql, (phone_number,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return False
        
        sql = "INSERT INTO user(phone_number, password, type, name, gender) VALUES(%s, %s, %s, %s, %s);"
        cursor.execute(sql, (phone_number, password, user_type, name, gender))
        return True
    finally:
        closeSQL(conn, cursor)

def update_info_db(user_id, password, name, gender):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT type FROM user WHERE user_id = %s;"
        cursor.execute(sql, (user_id,))
        user_exists = cursor.fetchone()
        
        if not user_exists:
            return False
        
        if password:
            sql = "UPDATE user SET password = %s WHERE user_id = %s;"
            cursor.execute(sql, (password, user_id))
        if name:
            sql = "UPDATE user SET name = %s WHERE user_id = %s;"
            cursor.execute(sql, (name, user_id))
        if gender:
            sql = "UPDATE user SET gender = %s WHERE user_id = %s;"
            cursor.execute(sql, (gender, user_id))
        
        return True
    finally:
        closeSQL(conn, cursor)

def get_learning_stats_by_person_db(user_id):
    conn, cursor = connectSQL()
    try:
        if user_id:
            sql = "SELECT type FROM user WHERE user_id = %s;"
            cursor.execute(sql, (user_id,))
            result = cursor.fetchone()
            return [user_id] if result else None
        else:
            sql = "SELECT user_id FROM user WHERE type = 'S';"
            cursor.execute(sql)
            return [row[0] for row in cursor.fetchall()]
    finally:
        closeSQL(conn, cursor)

def get_learning_stats_by_chapter_db(chapter_id):
    conn, cursor = connectSQL()
    try:
        if chapter_id:
            sql = "SELECT name FROM chapter WHERE id = %s;"
            cursor.execute(sql, (chapter_id,))
            result = cursor.fetchone()
            return [chapter_id] if result else None
        else:
            sql = "SELECT id FROM chapter;"
            cursor.execute(sql)
            return [row[0] for row in cursor.fetchall()]
    finally:
        closeSQL(conn, cursor)

def get_chapter_list_db(course_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT id, name, content FROM chapter WHERE course_id = %s;"
        cursor.execute(sql, (course_id,))
        return cursor.fetchall()
    finally:
        closeSQL(conn, cursor)

def get_ai_list_db(course_id, student_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT chapter.id, chapter.name FROM chapter, communicate_history WHERE course_id = %s AND student_id = %s AND chapter.id = communicate_history.chapter_id;"
        cursor.execute(sql, (course_id, student_id))
        return cursor.fetchall()
    finally:
        closeSQL(conn, cursor)

def get_ai_chat_db(student_id, chapter_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT session_id, session_name, type, content, time FROM communicate_history WHERE student_id = %s AND chapter_id = %s;"
        cursor.execute(sql, (student_id, chapter_id))
        return cursor.fetchall()
    finally:
        closeSQL(conn, cursor)

def get_course_list_db(student_id = None):
    conn, cursor = connectSQL()
    try:
        if student_id is None:
            sql = "SELECT DISTINCT id FROM course;"
            cursor.execute(sql)
        else:
            sql = "SELECT DISTINCT id FROM course_student WHERE student_id = %s;"
            cursor.execute(sql, (student_id))
        course_ids = [row[0] for row in cursor.fetchall()]
        
        courses = []
        for course_id in course_ids:
            sql = "SELECT name, teacher FROM course WHERE id = %s;"
            cursor.execute(sql, (course_id,))
            course_info = cursor.fetchone()
            
            sql = "SELECT name FROM user WHERE user_id = %s;"
            cursor.execute(sql, (course_info[1],))
            teacher_name = cursor.fetchone()[0]
            
            sql = "SELECT COUNT(*) FROM course_student WHERE course_id = %s;"
            cursor.execute(sql, (course_id,))
            student_count = cursor.fetchone()[0]
            
            courses.append({
                "id": course_id,
                "name": course_info[0],
                "teacher_id": course_info[1],
                "teacher_name": teacher_name,
                "student_num": student_count
            })
        
        return courses
    finally:
        closeSQL(conn, cursor)

def get_exercises_list_teacher_db(chapter_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT id, exercise_content, answer, difficulty, type FROM exercise WHERE chapter_id = %s AND is_official = 1;"
        cursor.execute(sql, (chapter_id,))
        rows =  cursor.fetchall()

        new_rows = []
        for row in rows:
            sql = "SELECT COUNT(*) FROM practice_history WHERE exercise_id = %s;"
            cursor.execute(sql, (row[0],))
            count = cursor.fetchone()[0] or 0  
            new_rows.append( (*row, count) )   
        rows = new_rows  
        return rows
    finally:
        closeSQL(conn, cursor)

def get_exercises_list_student_db(student_id, chapter_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT id, type, difficulty, exercise_content, is_official FROM exercise WHERE chapter_id = %s AND (is_official = 1 OR student_id = %s);"
        cursor.execute(sql, (chapter_id, student_id))
        rows =  cursor.fetchall()

        new_rows = []
        for row in rows:
            sql = "SELECT student_answer FROM practice_history WHERE exercise_id = %s AND student_id = %s;"
            cursor.execute(sql, (row[0], student_id))
            result = cursor.fetchone()
            new_rows.append( (*row, 1 if result else 0) )   
        rows = new_rows  
        return rows
    finally:
        closeSQL(conn, cursor)

def join_course_db(course_id, student_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT * FROM course WHERE id = %s;"
        cursor.execute(sql, (course_id,))
        result = cursor.fetchone()
        
        if result is None:
            return False
        
        sql = "INSERT INTO course_student values(%s, %s);"
        cursor.execute(sql, (course_id, student_id))   
        return True
    finally:
        closeSQL(conn, cursor)

def commit_exercise_db(student_id, exercise_id, student_answer):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT `check` FROM practice_history WHERE student_id = %s AND exercise_id = %s;"
        cursor.execute(sql, (student_id, exercise_id))
        result = cursor.fetchone()
        if not result:
            sql = "SELECT chapter_id FROM exercise WHERE id = %s;"
            cursor.execute(sql, (exercise_id,))
            chapter_id = cursor.fetchone()[0]
            sql = "INSERT INTO practice_history(student_id, exercise_id, student_answer, chapter_id, time) values(%s, %s, %s, %s, CURRENT_TIMESTAMP);"
            cursor.execute(sql, (student_id, exercise_id, student_answer, chapter_id))
            return True
        elif result[0]:
            return False
        else:
            sql = "UPDATE practice_history SET student_answer = %s, time = CURRENT_TIMESTAMP WHERE student_id = %s AND exercise_id = %s;"
            cursor.execute(sql, (student_answer, student_id, exercise_id))
            return True
    finally:
        closeSQL(conn, cursor)

def add_course_db(name, teacher_id):
    conn, cursor = connectSQL()
    try:
        sql = "INSERT INTO course(name, teacher) VALUES(%s, %s);"
        cursor.execute(sql, (name, teacher_id))
        return True
    finally:
        closeSQL(conn, cursor)

def update_exercise_db(id, content, answer, difficulty, type):
    conn, cursor = connectSQL()
    try:
        if content:
            sql = "UPDATE exercise SET exercise_content = %s WHERE id = %s;"
            cursor.execute(sql, (content, id))
        if answer:
            sql = "UPDATE exercise SET answer = %s WHERE id = %s;"
            cursor.execute(sql, (answer, id))
        if difficulty:
            sql = "UPDATE exercise SET difficulty = %s WHERE id = %s;"
            cursor.execute(sql, (difficulty, id))
        if type:
            sql = "UPDATE exercise SET type = %s WHERE id = %s;"
            cursor.execute(sql, (type, id))
        
        return True
    finally:
        closeSQL(conn, cursor)

def update_chapter_db(id, content, name):
    conn, cursor = connectSQL()
    try:
        if content:
            sql = "UPDATE chapter SET content = %s WHERE id = %s;"
            cursor.execute(sql, (content, id))
        if name:
            sql = "UPDATE chapter SET name = %s WHERE id = %s;"
            cursor.execute(sql, (name, id))
        
        return True
    finally:
        closeSQL(conn, cursor)

def get_user_list_db(user_type):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT user_id, phone_number, name, gender, frequence, sum_time FROM user WHERE type = %s;"
        cursor.execute(sql, (user_type,))
        return cursor.fetchall()
    finally:
        closeSQL(conn, cursor)

def delete_user_db(user_id):
    conn, cursor = connectSQL()
    try:
        sql = "DELETE FROM user WHERE user_id = %s;"
        cursor.execute(sql, (user_id,))
        return True
    finally:
        closeSQL(conn, cursor)

def get_system_stats_db():
    conn, cursor = connectSQL()
    try:
        sql = "SELECT * FROM system_stats;"
        cursor.execute(sql)
        return cursor.fetchone()
    finally:
        closeSQL(conn, cursor)

def get_exercise_history_db(student_id, exercise_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT student_answer, time, `check`, analyse FROM practice_history WHERE student_id = %s AND exercise_id = %s;"
        cursor.execute(sql, (student_id, exercise_id))
        result = cursor.fetchone()
        if not result:
            return 2, None
        if result[2] is None:
            return 3, result
        return 0, result
    finally:
        closeSQL(conn, cursor)

def get_student_exercises_db(exercise_id):
    conn, cursor = connectSQL()
    try:
        sql = "SELECT student_id, student_answer, time, `check`, analyse, user.name FROM practice_history, user WHERE exercise_id = %s AND practice_history.student_id = user.user_id;"
        cursor.execute(sql, (exercise_id,))
        return cursor.fetchall()
    finally:
        closeSQL(conn, cursor)

def delete_course_db(course_id):
    conn, cursor = connectSQL()
    try:
        sql = "DELETE FROM course WHERE id = %s;"
        cursor.execute(sql, (course_id,))
        return True
    finally:
        closeSQL(conn, cursor)

def delete_chapter_db(chapter_id):
    conn, cursor = connectSQL()
    try:
        sql = "DELETE FROM chapter WHERE id = %s;"
        cursor.execute(sql, (chapter_id,))
        return True
    finally:
        closeSQL(conn, cursor)

def delete_exercise_db(exercise_id):
    conn, cursor = connectSQL()
    try:
        sql = "DELETE FROM exercise WHERE id = %s;"
        cursor.execute(sql, (exercise_id,))
        return True
    finally:
        closeSQL(conn, cursor)