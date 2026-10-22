# server.py (后端 API)
import os
import time
import psycopg2
from psycopg2.extras import RealDictCursor
from flask import Flask, jsonify, request

app = Flask(__name__)

# 从环境变量读取连接配置
DB_HOST = os.getenv("DB_HOST", "postgres-service")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_USER = os.getenv("DB_USER", "myuser")
DB_PASSWORD = os.getenv("DB_PASSWORD", "mypassword123")
DB_NAME = os.getenv("DB_NAME", "mydb")

def get_db_connection():
    return psycopg2.connect(
        host=DB_HOST,
        port=DB_PORT,
        user=DB_USER,
        password=DB_PASSWORD,
        dbname=DB_NAME
    )

def init_db():
    """初始化数据库表结构：创建 cats 和 dogs 两张表"""
    for i in range(10):
        try:
            conn = get_db_connection()
            cur = conn.cursor()
            
            # 创建 cats 表 (包含 owner_name 和 cat_name)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS cats (
                    id SERIAL PRIMARY KEY,
                    owner_name TEXT NOT NULL,
                    cat_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            # 创建 dogs 表 (包含 owner_name 和 dog_name)
            cur.execute("""
                CREATE TABLE IF NOT EXISTS dogs (
                    id SERIAL PRIMARY KEY,
                    owner_name TEXT NOT NULL,
                    dog_name TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
            """)
            
            conn.commit()
            cur.close()
            conn.close()
            print("Successfully initialized 'cats' and 'dogs' tables in PostgreSQL!")
            return
        except Exception as e:
            print(f"Waiting for Postgres ({i+1}/10)... Error: {e}")
            time.sleep(2)

init_db()

@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "ok", "service": "backend"})

# ==================== Cat 相关 API ====================
@app.route('/api/cats', methods=['GET'])
def get_cats():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, owner_name, cat_name, created_at FROM cats ORDER BY id DESC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/cats', methods=['POST'])
def create_cat():
    req = request.get_json() or {}
    owner_name = req.get("owner_name", "Anonymous")
    cat_name = req.get("cat_name", "Unknown Cat")
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO cats (owner_name, cat_name) VALUES (%s, %s) RETURNING id, owner_name, cat_name;",
        (owner_name, cat_name)
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_row), 201

# ==================== Dog 相关 API ====================
@app.route('/api/dogs', methods=['GET'])
def get_dogs():
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute("SELECT id, owner_name, dog_name, created_at FROM dogs ORDER BY id DESC;")
    data = cur.fetchall()
    cur.close()
    conn.close()
    return jsonify(data)

@app.route('/api/dogs', methods=['POST'])
def create_dog():
    req = request.get_json() or {}
    owner_name = req.get("owner_name", "Anonymous")
    dog_name = req.get("dog_name", "Unknown Dog")
    
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    cur.execute(
        "INSERT INTO dogs (owner_name, dog_name) VALUES (%s, %s) RETURNING id, owner_name, dog_name;",
        (owner_name, dog_name)
    )
    new_row = cur.fetchone()
    conn.commit()
    cur.close()
    conn.close()
    return jsonify(new_row), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)