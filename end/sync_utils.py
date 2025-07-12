from database_utils import redis_client, redis_keys, connectSQL, closeSQL
import signal
import sys

def sync_redis_to_db():
    conn, cursor = connectSQL()
    try:
        values = [int(redis_client.get(key) or 0) for key in redis_keys]
        sql = "UPDATE system_stats SET S_AiChat=%s, S_exercises=%s, S_check=%s, T_courseware=%s, T_exercises=%s, T_check=%s;"
        cursor.execute(sql, values)
    finally:
        closeSQL(conn, cursor)

# 捕获Ctrl+C等信号，退出时同步一次
def setup_exit_handler():
    def handler(signum, frame):
        print("同步Redis计数到MySQL...")
        sync_redis_to_db()
        sys.exit(0)
    signal.signal(signal.SIGINT, handler)
    signal.signal(signal.SIGTERM, handler)