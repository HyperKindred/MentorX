import requests
import pymysql
from flask import Flask, request, jsonify
from flask_cors import CORS
from data_utils import *
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings
from flask_jwt_extended import JWTManager, create_access_token, get_jwt_identity, jwt_required

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("./end/multi_doc_vector_db", embedding_model, allow_dangerous_deserialization=True)
jwt = JWTManager()

app = Flask(__name__)
app.config['SECRET_KEY'] = "secret key"
jwt.init_app(app)

# 网络跨域问题
app.config.from_object(__name__)
CORS(app, resource={r'/*': {'origins': '*'}})

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
model_name = 'deepseek-r1:1.5b'

# flask API 的开始
@app.route('/api/signIn', methods=["POST"])
def signIn():
    conn, cursor = connectSQL()
    phone_number = request.form.get("phone_number")
    password = request.form.get("password")
    sql = f"select password from user where phone_number = '{phone_number}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "手机号不存在！"}
    elif password != result[0]:
        data = {"ret": 1, "msg": "密码错误！"}
    else:
        sql = f"select user_id, type, name, gender from user where phone_number = '{phone_number}';"
        result = cursor.execute(sql)
        access_token = create_access_token(identity=result[0])
        data = {"ret": 0, 
                "msg":"登录成功", 
                "jwt":access_token,
                "gender":result[3],
                "type":result[1],
                "name":result[2]
                }
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/register', methods=["POST"])
def register():
    conn, cursor = connectSQL()
    phone_number = request.form.get("phone_number")
    password = request.form.get("password")
    user_type = request.form.get("type")
    name = request.form.get("name")
    gender = request.form.get("gender")
    sql = f"select phone_number from user where phone_number = '{phone_number}';"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result != None:
        data = {"ret": 1, "msg": "用户名已存在！"}
    else:
        sql = f"insert into user(phone_number, password, type, name, gender) values('{phone_number}', '{password}', '{user_type}', '{name}', '{gender}');"
        cursor.execute(sql)
        data = {"ret": 0, "msg":f"用户{phone_number}注册成功！"}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/updateInfo', methods=["POST"])
@jwt_required()
def updateInfo():
    conn, cursor = connectSQL()
    user_id = request.form.get("id")
    if user_id == None:
        user_id = get_jwt_identity()

    sql = f"select type from user where user_id = {user_id};"
    cursor.execute(sql)
    result = cursor.fetchone()
    if result == None:
        data = {"ret": 1, "msg": "该用户不存在！"}
    else:
        password = request.form.get("password")
        if password != None:
            sql = f"update user set password = '{password}' where user_id = {user_id};"
            cursor.execute(sql)
        name = request.form.get("name")
        if name != None:
            sql = f"update user set name = '{name}' where user_id = {user_id};"
            cursor.execute(sql)
        gender = request.form.get("gender")
        if gender != None:
            sql = f"update user set gender = '{gender}' where user_id = {user_id};"
            cursor.execute(sql)
        data = {"ret": 0, "msg":f"用户{user_id}信息修改成功！"}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/getLearningStatsByPerson', methods=["POST"])
def getLearningStatsByPerson():
    conn, cursor = connectSQL()
    students = []
    user_id = request.form.get("user_id")

    if user_id != None:
        sql = f"select type from user where user_id = {user_id};"
        cursor.execute(sql)
        result = cursor.fetchone()
        if result == None:
            data = {"ret": 1, "msg": "该用户不存在！"}
        else:
            student = f_getLearningStatsByPerson(user_id)
            students.append(student)
            data = {"ret": 0, "msg":"获取信息成功！", "students":students}
    else:
        sql = f"select user_id from user where type = 'S';"
        cursor.execute(sql)
        rows = cursor.fetchall()
        id_list = [row[0] for row in rows]
        for user_id in id_list:
            student = f_getLearningStatsByPerson(user_id)
            students.append(student)
        data = {"ret": 0, "msg":"获取信息成功！", "students":students}
    closeSQL(conn, cursor)
    return jsonify(data)

@app.route('/api/student/AIchat', methods=['POST'])
def AIchat():
    ChapterNo = request.form.get("ChapterNo")  
    question = request.form.get("question")
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        closeSQL(conn, cursor)

    full_prompt = f"""请根据以下课件内容回答问题。
    课件内容：
    {content}
    
    问题：{question}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            data = {'ret':0, 'ans':result.get('response', '')}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)

@app.route('/api/student/generate_exercises', methods=['POST'])
def generate_exercises():
    ChapterNo = request.form.get("ChapterNo")   #章节号->课件内容
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        closeSQL(conn, cursor)

    difficulty = request.form.get("difficulty")
    type = request.form.get("type")
    
    type_map = {
        'choices': '选择题',
        'blanks': '填空题',
        'answers': '简答题'
    }
    TYPE = type_map.get(type, '简答题')  

    full_prompt = f"""请根据以下课件内容和要求设计一个题目
    课件内容：
    {content}
    难度等级：
    {difficulty}
    题目类型：
    {TYPE}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            data = {'ret':0, 'exercise':result.get('response', '')}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)

@app.route('/api/student/check_exercises', methods=['POST'])
def check_exercises():
    Eno = request.form.get("Eno")   #习题号->习题内容
    ans = request.form.get("ans")
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT exercise_content FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "习题获取失败"})
    finally:
        closeSQL(conn, cursor)


    full_prompt = f"""请批改练习题，0代表正确，1代表错误，2代表半对半错，并且用<>分开后给出分析与解释
    习题：
    {content}
    学生作答：
    {ans}
 
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            raw_output = result.get('response', '')
            if "<>" in raw_output:
                check, analysis = raw_output.strip().split("<>", 1)
            else:
                check = raw_output.strip()
                analysis = "无解析"
            data = {'ret':0, 'check':check, 'analysis':analysis}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)

@app.route('/api/teacher/generate_teachcontent', methods=['POST'])
def generate_teachcontent():
    Cno = request.form.get("Cno")   #课程号->课程名
    chapter = request.form.get("chapter")
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT name FROM course WHERE id = %s", (Cno,))
        result = cursor.fetchone()
        Cname = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课程名获取失败"})
    finally:
        closeSQL(conn, cursor)
  


    query = f"{Cname} {chapter}"
    context = db.similarity_search(query, k=3)

    full_prompt = f"""
    你是一位教学设计专家，请根据以下资料生成一份教学内容，要求包括：

    1. 知识讲解内容（简要概述）
    2. 实训练习安排（不少于2个）
    3. 指导建议（学生应掌握哪些技能/难点）
    4. 时间分布（理论与实践分配）

    【课程资料】
    {context}

    【课程名】{Cname}
    【章节名】{chapter}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            data = {'ret':0, 'content':result.get('response', '')}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)

@app.route('/api/teacher/generate_tasks', methods=['POST'])
def generate_tasks():
    ChapterNo = request.form.get("ChapterNo")   #章节号->课件内容
    difficulty = request.form.get("difficulty")
    type = request.form.get("type")
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        closeSQL(conn, cursor)
    
    type_map = {
        'choices': '选择题',
        'blanks': '填空题',
        'answers': '简答题'
    }
    TYPE = type_map.get(type, '简答题')  


 
    full_prompt = f"""请根据以下课件内容和要求设计一个题目，并给出参考答案，中间用<>分隔
    课件内容：
    {content}
    难度等级：
    {difficulty}
    题目类型：
    {TYPE}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            raw_output = result.get('response', '')
            if "<>" in raw_output:
                task, ans = raw_output.strip().split("<>", 1)
            else:
                task = raw_output.strip()
                ans = "无解析"
            data = {'ret':0, 'task':task, 'ans':ans}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)


@app.route('/api/teacher/check', methods=['POST'])
def generate_tasks():
    Eno = request.form.get("Eno")   #章节号->课件内容
    ans = request.form.get("ans")
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT exercise_content FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "习题获取失败"})
    finally:
        closeSQL(conn, cursor)
    try:
        conn, cursor = connectSQL()
        cursor.execute("SELECT answer FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        answer = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "答案获取失败"})
    finally:
        closeSQL(conn, cursor)
   
    type_map = {
        'choices': '选择题',
        'blanks': '填空题',
        'answers': '简答题'
    }
    TYPE = type_map.get(type, '简答题')  


 
    full_prompt = f"""请批改练习题，0代表正确，1代表错误，2代表半对半错，并且用<>分开后给出分析与解释
    题目：
    {content}
    参考答案：
    {answer}
    学生答案：
    {ans}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            raw_output = result.get('response', '')
            if "<>" in raw_output:
                check, alaysis = raw_output.strip().split("<>", 1)
            else:
                check = raw_output.strip()
                alaysis = "无解析"
            data = {'ret':0, 'check':check, 'alaysis':alaysis}
        except:
            return jsonify({"ret": 1, "msg":"模型输出结果异常！"})
    except:
        data = {'ret':1, 'msg':"模型调用失败！"}
    return jsonify(data)


if __name__ == '__main__':
    app.run(debug=True, port=5000)
