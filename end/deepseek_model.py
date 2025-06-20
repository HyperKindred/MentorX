import requests
import re
from database_utils import connectSQL, closeSQL
from langchain.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings


embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2")
db = FAISS.load_local("./multi_doc_vector_db", embedding_model, allow_dangerous_deserialization=True)

OLLAMA_API_URL = 'http://localhost:11434/api/generate'
model_name = 'deepseek-r1:1.5b'

pattern_exercise = r"<exercise>(.*?)<-exercise>\s*<answer>(.*?)</answer>"
pattern_check = r"<check>(.*?)<-check>\s*<analyse>(.*?)</analyse>"

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

    1. 知识讲解内容(尽量详细和具体，可以根据资料进行拓展)
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
        cleaned_content = re.sub(r"<think>.*?</think>", "", content, flags=re.DOTALL).strip()   
        sql = "INSERT INTO chapter(name, content, course_id) values(%s, %s, %s);"
        cursor.execute(sql, (Cname, cleaned_content, Cno))
    except:
        return False
    finally:
        closeSQL(conn, cursor)
        return True

def ds_generate_tasks(ChapterNo, difficulty, type, student_id = None):
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
    <exercise>这里是示例题目</exercise>
    <answer>这里是示例答案</answer>
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
            if student_id:
                sql = '''INSERT INTO exercise(exercise_content, answer, difficulty, type, chapter_id, is_official, student_id)
                VALUES(%s, %s, %s, %s, %s, 0, %s);
                '''
                cursor.execute(sql, (exercise, answer, difficulty, type, ChapterNo, student_id))
            else:
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
        return False, "该习题不存在！"
    
    cursor.execute("SELECT student_answer FROM practice_history WHERE student_id = %s AND exercise_id = %s;", (student_id, Eno))
    result = cursor.fetchone()
    if result:
        student_answer = result[0]
    else:
        return False, "该习题未作答！"
    
    full_prompt = f"""请批改练习题，
    题目：
    {content}
    参考答案：
    {answer}
    学生答案：
    {student_answer}

    输出正误与做题分析，其中正误部分0代表正确，1代表错误，2代表部分正确，两部分格式参考示例：
    <check>0</check>
    <analyse>这是示例分析</analyse>  
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
            return False, "模型输出结果异常！"       
    except:
        return False, "模型调用异常！"
    finally:
        closeSQL(conn, cursor)
        return True, None

def ds_aichat(student_id, chapter_id, content, session_id):
    conn, cursor = connectSQL()      
    cursor.execute("SELECT content FROM chapter WHERE id = %s", (chapter_id,))
    result = cursor.fetchone()
    if result:
        teachcontent = result[0]
    else:
        return False, "该章节无内容！"

    full_prompt = f"""请根据以下课件内容回答问题。
    课件内容：{teachcontent}   
    问题：{content}
    """
    try:
        response = requests.post(OLLAMA_API_URL, json={
            'model': model_name,
            'prompt': full_prompt,
            'stream': False
        })
        try:
            result = response.json()
            answer = {'ret':0, 'ans':result.get('response', '')}
            if session_id is None:
                cursor.execute("SELECT MAX(session_id) FROM communicate_history;") 
                res = cursor.fetchone()
                session_id = res[0] + 1 if res else 1
            sql = "INSERT INTO communicate_history values(%s, %s, 'Q', %s, CURRENT_TIMESTAMP, %s, '默认名称');"
            cursor.execute(sql, (student_id, chapter_id, content, session_id))
            sql = "INSERT INTO communicate_history values(%s, %s, 'A', %s, CURRENT_TIMESTAMP + INTERVAL '3 seconds', %s, '默认名称');"
            cursor.execute(sql, (student_id, chapter_id, answer, session_id))
            return True, answer
        except:
            return False, "模型输出结果异常！"
    except:
        return False, "模型调用失败！"
    finally:
        closeSQL(conn, cursor)