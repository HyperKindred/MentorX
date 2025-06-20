from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_jwt_extended import  JWTManager, create_access_token, get_jwt_identity, jwt_required
from database_utils import *
from deepseek_model import *


app = Flask(__name__)
app.config['JWT_SECRET_KEY'] = "secret key"

jwt = JWTManager(app)

# 网络跨域问题
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

# flask API 的开始
@app.route('/api/signIn', methods=["POST"])
def signIn():
    phone_number = request.form.get("phone_number")
    password = request.form.get("password")
    
    result = sign_in_db(phone_number)
    
    if result is None:
        data = {"ret": 1, "msg": "手机号不存在！"}
    elif password != result[0]:
        data = {"ret": 1, "msg": "密码错误！"}
    else:
        access_token = create_access_token(identity=str(result[1]))
        data = {"ret": 0, 
                "msg": "登录成功", 
                "jwt": access_token,
                "gender": result[4],
                "type": result[2],
                "name": result[3]
                }
    return jsonify(data)

@app.route('/api/register', methods=["POST"])
def register():
    phone_number = request.form.get("phone_number")
    password = request.form.get("password")
    user_type = request.form.get("type")
    name = request.form.get("name")
    gender = request.form.get("gender")
    
    success = register_db(phone_number, password, user_type, name, gender)
    
    if not success:
        data = {"ret": 1, "msg": "用户名已存在！"}
    else:
        data = {"ret": 0, "msg": f"用户{phone_number}注册成功！"}
    return jsonify(data)

@app.route('/api/updateInfo', methods=["POST"])
@jwt_required()
def updateInfo():
    user_id = request.form.get("id") or int(get_jwt_identity())
    password = request.form.get("password")
    name = request.form.get("name")
    gender = request.form.get("gender")
    
    success = update_info_db(user_id, password, name, gender)
    
    if not success:
        data = {"ret": 1, "msg": "该用户不存在！"}
    else:
        data = {"ret": 0, "msg": f"用户{user_id}信息修改成功！"}
    return jsonify(data)

@app.route('/api/getLearningStatsByPerson', methods=["POST"])
def getLearningStatsByPerson():
    user_id = request.form.get("user_id")
    user_ids = get_learning_stats_by_person_db(user_id)
    
    students = []
    if user_ids is None:
        data = {"ret": 1, "msg": "该用户不存在！"}
    else:
        for uid in user_ids:
            student = f_getLearningStatsByPerson(uid)
            students.append(student)
        data = {"ret": 0, "msg": "获取信息成功！", "students": students}
    return jsonify(data)

@app.route('/api/getLearningStatsByChapter', methods=["POST"])
def getLearningStatsByChapter():
    chapter_id = request.form.get("id")
    chapter_ids = get_learning_stats_by_chapter_db(chapter_id)
    
    chapters = []
    if chapter_ids is None:
        data = {"ret": 1, "msg": "该章节不存在！"}
    else:
        for cid in chapter_ids:
            chapter = f_getLearningStatsByChapter(cid)
            chapters.append(chapter)
        data = {"ret": 0, "msg": "获取信息成功！", "chapters": chapters}
    return jsonify(data)

@app.route('/api/getChapterList', methods=["POST"])
def getChapterList():
    course_id = request.form.get("id")
    rows = get_chapter_list_db(course_id)
    
    chapterList = []
    for row in rows:
        chapter = {"id": row[0], "name": row[1], "content": row[2]}
        chapterList.append(chapter)
    
    data = {"ret": 0, "msg": "章节课件列表成功！", "chapterList": chapterList}
    return jsonify(data)

@app.route('/api/getCourseList', methods=["GET"])
def getCourseList():
    courses = get_course_list_db()
    data = {"ret": 0, "msg": "获取课程列表成功！", "courseList": courses}
    return jsonify(data)

@app.route('/api/student/getCourseList', methods=["GET"])
@jwt_required()
def getCourseList_student():
    student_id = int(get_jwt_identity())
    courses = get_course_list_db(student_id)
    data = {"ret": 0, "msg": "获取已选课程列表成功！", "courseList": courses}
    return jsonify(data)

@app.route('/api/student/getAiList', methods=["POST"])
@jwt_required()
def getAiList():
    student_id = int(get_jwt_identity())
    course_id = request.form.get("course_id")
    rows = get_ai_list_db(student_id, course_id)
    chapters = [{"chapter_id": row[0], "chapter_name": row[1]} for row in rows]

    data = {"ret": 0, "msg": "获取聊天记录章节列表成功！", "chapters": chapters}
    return jsonify(data)

@app.route('/api/student/getAiChat', methods=["POST"])
@jwt_required()
def getAiChat():
    student_id = int(get_jwt_identity())
    chapter_id = request.form.get("chapter_id")
    rows = get_ai_chat_db(student_id, chapter_id)
    keys = ["session_id", "session_name", "type", "content", "time"]
    sessions = [{k:row[i] for i, k in enumerate(keys)} for row in rows]

    data = {"ret": 0, "msg": "获取课程列表成功！", "sessions": sessions}
    return jsonify(data)

@app.route('/api/teacher/getExercisesList', methods=["POST"])
def getExercisesList_teacher():
    chapter_id = request.form.get("id")
    rows = get_exercises_list_teacher_db(chapter_id)
    
    keys = ["id", "content", "answer", "difficulty", "type", "committed_num"]
    exercisesList = [{k:row[i] for i, k in enumerate(keys)} for row in rows]
    
    data = {"ret": 0, "msg": "获取习题列表成功！", "exercisesList": exercisesList}
    return jsonify(data)

@app.route('/api/student/getExercisesList', methods=["POST"])
@jwt_required()
def getExercisesList_student():
    chapter_id = request.form.get("chapter_id")
    student_id = int(get_jwt_identity())
    rows = get_exercises_list_student_db(student_id, chapter_id)
    
    keys = ["exercise_id", "type", "difficulty", "exercise_content", "is_official", "is_committed"]
    exercisesList = [{k:row[i] for i, k in enumerate(keys)} for row in rows]
    
    data = {"ret": 0, "msg": "获取习题列表成功！", "exercisesList": exercisesList}
    return jsonify(data)

@app.route('/api/student/getExerciseHistory', methods=["POST"])
@jwt_required()
def getExerciseHistory():
    exercise_id = request.form.get("exercise_id")
    student_id = int(get_jwt_identity())
    stats, result = get_exercise_history_db(student_id, exercise_id)
    
    if stats == 2:
        return jsonify({"ret":2, "msg":"习题未作答！"})
    keys = ["student_answer", "answer_time", "check", "analyse"]
    result_data = {k:result[i] for i, k in enumerate(keys)}
    if stats == 3:
        data = data = {"ret": 3, "msg": "习题未批改！"}
    else:
        data = {"ret": 0, "msg": "作答历史获取成功！"}
    merge_data = {**data, **result_data}
    return jsonify(merge_data)

@app.route('/api/teacher/getStudentExercises', methods=["POST"])
def getStudentExercises():
    exercise_id = request.form.get("exercise_id")
    rows = get_student_exercises_db(exercise_id)
    
    keys = ["student_id", "student_answer", "answer_time", "check", "analyse", "student_name"]
    students = [{k:row[i] for i, k in enumerate(keys)} for row in rows]  
    data = {"ret": 0, "msg": "获取学生习题作答成功！", "students": students}
    return jsonify(data)

@app.route('/api/student/joinCourse', methods=["POST"])
@jwt_required()
def joinCourse():
    course_id = request.form.get("course_id")
    student_id = int(get_jwt_identity())
    
    success = join_course_db(course_id, student_id)
    
    if not success:
        data = {"ret": 1, "msg": "该课程不存在，加入课程失败！"}
    else:
        data = {"ret": 0, "msg": "加入课程成功！"}
    return jsonify(data)

@app.route('/api/student/commitExercise', methods=["POST"])
@jwt_required()
def commitExercise():
    student_id = int(get_jwt_identity())
    exercise_id = int(request.form.get("exercise_id"))
    student_answer = request.form.get("student_answer")
    success = commit_exercise_db(student_id, exercise_id, student_answer)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "提交失败，练习已批改！"})

@app.route('/api/teacher/addCourse', methods=["POST"])
@jwt_required()
def addCourse():
    name = request.form.get("name")
    teacher_id = int(get_jwt_identity())
    
    success = add_course_db(name, teacher_id)
    
    if not success:
        return jsonify({"ret": 1, "msg": "添加课程失败"})
    return jsonify({"ret": 0})

@app.route('/api/teacher/updateExercise', methods=["POST"])
def updateExercise():
    id = request.form.get("id")
    content = request.form.get("content")
    answer = request.form.get("answer")
    difficulty = request.form.get("difficulty")
    type = request.form.get("type")

    if not content and not answer and not difficulty and not type:
        return jsonify({"ret": 1, "msg": "无修改内容！"})
    
    success = update_exercise_db(id, content, answer, difficulty, type)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "更新失败"})

@app.route('/api/teacher/updateChapter', methods=["POST"])
def updateChapter():
    id = request.form.get("id")
    content = request.form.get("content")
    name = request.form.get("name")
    
    if not content and not name:
        return jsonify({"ret": 1, "msg": "无修改内容！"})
    
    success = update_chapter_db(id, content, name)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "更新失败"})

@app.route('/api/admin/getUserList', methods=["POST"])
def getUserList():
    user_type = request.form.get("type")
    rows = get_user_list_db(user_type)
    
    keys = ["id", "phone_number", "name", "gender", "frequence", "sum_time"]
    userList = [{k: row[i] for i, k in enumerate(keys)} for row in rows]
    
    data = {"ret": 0, "userList": userList}
    return jsonify(data)

@app.route('/api/admin/deleteUser', methods=["POST"])
def deleteUser():
    id = request.form.get("id")
    success = delete_user_db(id)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "删除失败"})

@app.route('/api/admin/getSystemStats', methods=["GET"])
def getSystemStats():
    result = get_system_stats_db()
    
    if not result:
        return jsonify({"ret": 1, "msg": "未找到系统统计信息"})
    
    keys = ["S_AiChat", "S_exercises", "S_check", "T_courseware", "T_exercises", "T_check"]
    systemStats = {k: result[i] for i, k in enumerate(keys)}
    
    data = {"ret": 0, "systemStats": systemStats}
    return jsonify(data)

@app.route('/api/deleteCourse', methods=["POST"])
def deleteCourse():
    id = request.form.get("id")
    success = delete_course_db(id)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "删除失败"})

@app.route('/api/deleteChapter', methods=["POST"])
def deleteChapter():
    id = request.form.get("id")
    success = delete_chapter_db(id)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "删除失败"})

@app.route('/api/deleteExercise', methods=["POST"])
def deleteExercise():
    id = request.form.get("id")
    success = delete_exercise_db(id)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "删除失败"})
    
# 与大模型交互相关联
@app.route('/api/student/AIchat', methods=['POST'])
def AIchat():
    ChapterNo = request.form.get("ChapterNo")  
    question = request.form.get("question")
    

@app.route('/api/student/generate_exercises', methods=['POST'])
def generate_exercises():
    ChapterNo = request.form.get("ChapterNo")   #章节号->课件内容
    

@app.route('/api/student/check_exercises', methods=['POST'])
def check_exercises():
    Eno = request.form.get("Eno")   #习题号->习题内容
    ans = request.form.get("ans")
    

@app.route('/api/teacher/generate_teachcontent', methods=['POST'])
def generate_teachcontent():
    Cno = request.form.get("Cno")  
    chapter = request.form.get("chapter")
    success = ds_generate_teachcontent(Cno, chapter)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "课件生成失败！"})

@app.route('/api/teacher/generate_tasks', methods=['POST'])
def generate_tasks():
    ChapterNo = request.form.get("ChapterNo")   
    difficulty = request.form.get("difficulty")
    type = request.form.get("type")
    success = ds_generate_tasks(ChapterNo, difficulty, type)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "习题生成失败！"})

@app.route('/api/teacher/check', methods=['POST'])
def check_answer():
    Eno = request.form.get("Eno")
    student_id = request.form.get("student_id")
    success = ds_check_answer(Eno, student_id)
    return jsonify({"ret": 0} if success else {"ret": 1, "msg": "批改习题失败！"})


if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)
