import mysql.connector
import json

def create_connection(connection_info):
    """创建并返回数据库连接和游标"""
    # 使用上下文管理器自动处理连接关闭
    return mysql.connector.connect(**connection_info)

def execute_query(connection, query, params=None):
    """执行SQL查询并返回所有结果"""
    with connection.cursor() as cursor:
        cursor.execute(query, params or ())
        return cursor.fetchall()

def fetch_records(connection, query, params=None):
    """通用的记录获取函数，打印所有查询到的记录"""
    try:
        rows = execute_query(connection, query, params)
        for row in rows:
            print(row)
        if not rows:
            print("No records found.")
    except mysql.connector.Error as err:
        print("Database error:", err)

def read_config():
    """读取配置文件"""
    with open('config.json') as f:
        return json.load(f)

if __name__ == "__main__":
    connection_info = read_config()
    try:
        conn = create_connection(connection_info)
        with conn:
            # Example usages
            print("Fetching all records:")
            fetch_records(conn, 'SELECT * FROM History')
            print("\nFetching records by date:")
            fetch_records(conn, "SELECT * FROM History WHERE DATE(RecordDate) = %s", ('2021-06-01',))
            print("\nFetching records by label:")
            fetch_records(conn, "SELECT * FROM History WHERE label = %s", ('Wheat',))
    except mysql.connector.Error as err:
        print("Connection error:", err)
