from sqlalchemy import create_engine,text

db = {
    'user' : 'root',
    'passwd':'qwe123',
    'database' : 'school',
    'charset' : 'utf8',
    'host' : 'localhost' ,
    'port':3306 
}

db_url=f"mysql+mysqlconnector://{db['user']}:{db['passwd']}@{db['host']}:{db['port']}/{db['database']}?charset=utf8"


def conn_mysqldb():
    db_conn= create_engine(db_url, encoding='utf-8',max_overflow=0)
    db_conn.connect()
    return db_conn


#데이터베이스와 연결이 끊길 경우 확인 후 다시 연결하거나 이미 연결되어 있는 경우에는 
#return 으로 연결된 객체를 반환하도록 함.


# def conn_mysqldb():
#     if not MYSQL_CONN.open:
#         MYSQL_CONN.close()
#         MYSQL_CONN.ping(reconnect=True)
#     return MYSQL_CONN
# #데이터베이스와 연결이 끊길 경우 확인 후 다시 연결하거나 이미 연결되어 있는 경우에는 
# #return 으로 연결된 객체를 반환하도록 함.
