import requests
import pymysql
from flask import Flask, request, jsonify
from langchain.vectorstores import FAISS
from langchain.embeddings import HuggingFaceEmbeddings

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("./end/multi_doc_vector_db", embedding_model, allow_dangerous_deserialization=True)
app = Flask(__name__)
OLLAMA_API_URL = 'http://localhost:11434/api/generate'
model_name = 'deepseek-r1:1.5b'
config = {
    'host': 'localhost',      # 或远程 IP
    'port': 3306,             # 默认 MySQL 端口
    'user': 'Hypercube',  # 替换为你的用户名
    'password': '990923',  # 替换为你的密码
    'database': 'mentorx',   # 替换为你的数据库名
    'charset': 'utf8mb4'
}
@app.route('/api/student/AIchat', methods=['POST'])
def AIchat():
    ChapterNo = request.form.get("ChapterNo")  
    question = request.form.get("question")
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        cursor.close()
        conn.close()

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
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        cursor.close()
        conn.close()

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
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT exercise_content FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "习题获取失败"})
    finally:
        cursor.close()
        conn.close()


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
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM course WHERE id = %s", (Cno,))
        result = cursor.fetchone()
        Cname = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课程名获取失败"})
    finally:
        cursor.close()
        conn.close()
  


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
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT content FROM chapter WHERE id = %s", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "课件获取失败"})
    finally:
        cursor.close()
        conn.close()
    
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
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT exercise_content FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "习题获取失败"})
    finally:
        cursor.close()
        conn.close()
    try:
        conn = pymysql.connect(**config)
        cursor = conn.cursor()
        cursor.execute("SELECT answer FROM exercise WHERE id = %s", (Eno,))
        result = cursor.fetchone()
        answer = result[0] if result else "无内容"
    except:
        return jsonify({"ret": 1, "msg": "答案获取失败"})
    finally:
        cursor.close()
        conn.close()
   
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
