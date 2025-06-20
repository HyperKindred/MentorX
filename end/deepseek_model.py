import requests
import re
from database_utils import connectSQL, closeSQL
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
db = FAISS.load_local("./multi_doc_vector_db", embedding_model, allow_dangerous_deserialization=True)

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
model_name = 'deepseek-r1:8b'

pattern_exercise = r"<exercise>(.*?)<-exercise>\s*<answer>(.*?)<-answer>"
pattern_check = r"<check>(.*?)<-check>\s*<analyse>(.*?)<-analyse>"

def ds_generate_teachcontent(Cno, chapter):
    conn, cursor = connectSQL()
    try:        
        cursor.execute("SELECT name FROM course WHERE id = %s;", (Cno,))
        result = cursor.fetchone()
        Cname = result[0] if result else "暂无课程名"
    except:
        return False
    
    query = f"{Cname} {chapter}"
    context = db.similarity_search(query, k=3)

    full_prompt = f"""
    你是一位教学设计专家，请根据以下资料生成一份教学内容，要求包括：

    1. 知识讲解内容
    2. 实训练习安排（不少于2个）
    3. 指导建议（学生应掌握哪些技能/难点）
    4. 时间分布（理论与实践分配）

    【课程资料】{context}
    【课程名】{Cname}
    【章节名】{chapter}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        result = response.json()
        content = result.get('response', '')     
        sql = "INSERT INTO chapter(name, content, course_id) values(%s, %s, %s);"
        cursor.execute(sql, (Cname, content, Cno))
    except:
        return False
    finally:
        closeSQL(conn, cursor)
        return True

def ds_generate_tasks(ChapterNo, difficulty, type):
    conn, cursor = connectSQL()
    try:
        cursor.execute("SELECT content FROM chapter WHERE id = %s;", (ChapterNo,))
        result = cursor.fetchone()
        content = result[0] if result else "无内容"
    except:
        return False
    
    difficulty_map = {
        4 : "极难",
        3 : "困难",
        2 : "中等",
        1 : "简单"
    }

    type_map = {
        'choices': '选择题',
        'blanks': '填空题',
        'answers': '简答题',
        'code': '编程题'
    }
    TYPE = type_map.get(type, '简答题')  
    DIFFI = difficulty_map.get(difficulty, "中等")

    full_prompt = f"""请根据以下课件内容和要求设计一个题目，并给出参考答案，
    课件内容：
    {content}
    难度等级：
    {DIFFI}
    题目类型：
    {TYPE}
    
    题目与答案包含在类型标识<>中，示例：
    <exercise>这里是示例题目<-exercise>
    <answer>这里是示例答案<-answer>
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        result = response.json()
        raw_output = result.get('response', '')
        match = re.search(pattern_exercise, raw_output, re.DOTALL)
        if match:
            exercise = match.group(1).strip()
            answer = match.group(2).strip()
            sql = '''INSERT INTO exercise(exercise_content, answer, difficulty, type, chapter_id, is_official)
            VALUES(%s, %s, %s, %s, %s, 1);
            '''
            cursor.execute(sql, (exercise, answer, difficulty, type, ChapterNo))
        else:
            return False
    except:
        return False
    finally:
        closeSQL(conn, cursor)
        return True

def ds_check_answer(Eno, student_id):
    conn, cursor = connectSQL()
    cursor.execute("SELECT exercise_content, answer FROM exercise WHERE id = %s;", (Eno,))
    result = cursor.fetchone()
    if result:
        content = result[0]
        answer = result[1]
    else:
        return False
    
    cursor.execute("SELECT student_answer FROM practice_history WHERE student_id = %s AND exercise_id = %s;", (student_id, Eno))
    result = cursor.fetchone()
    if result:
        student_answer = result[0]
    else:
        return False
    
    full_prompt = f"""请批改练习题，
    题目：
    {content}
    参考答案：
    {answer}
    学生答案：
    {student_answer}

    输出正误与做题分析，其中正误部分0代表正确，1代表错误，2代表部分正确，两部分格式参考示例：
    <check>0<-check>
    <analyse>这是示例分析<-analyse>  
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })    
        result = response.json()
        raw_output = result.get('response', '')
        match = re.search(pattern_check, raw_output, re.DOTALL)
        if match:
            check = match.group(1).strip()
            analyse = match.group(2).strip()
            sql = "UPDATE practice_history SET analyse = %s, check = %s WHERE student_id = %s AND exercise_id = %s;"
            cursor.execute(sql, (analyse, check, student_id, Eno))
        else:
            return False        
    except:
        return False
    finally:
        closeSQL(conn, cursor)
        return True

def ds_aichat():
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

def ds_generate_exercises():
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

def ds_check_exercises():
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