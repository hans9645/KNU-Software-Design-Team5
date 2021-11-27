from flask_login import UserMixin
from db_model.mysql import conn_mysqldb
from datetime import datetime
from sqlalchemy import create_engine, text
import bcrypt
import jwt

class User(UserMixin):

    def __init__(self,user_id, password,user_name,belong,tele):
        self.user_id=user_id
        self.password=password
        self.name=user_name
        self.belong=belong
        self.tele=tele
        
        
    
    def get_id(self):
        return str(self.user_id)

    @staticmethod
    def get(user_id):
        mysql_db=conn_mysqldb()
        param={'user_id':user_id}
        user=mysql_db.execute(text("SELECT * FROM user_info WHERE USER_ID=:user_id"),param).fetchone()
        if not user:
            return None
        user=User(user_id=user[1], password=user[2],user_name=user[3],belong=user[4],tele=user[5])
        return user


    @staticmethod
    def find(user_id):
        mysql_db=conn_mysqldb()
        user=mysql_db.execute("SELECT * FROM user_info WHERE USER_ID='%s'"%str(user_id)).fetchone()
        if not user:
            return None
        user = User(user_id=user[1], password=user[2],
                    user_name=user[3], belong=user[4],tele=user[5])
        return user



    @staticmethod
    def create(user_id, password,user_name,belong,tele):
        user=User.find(user_id)
        if user==None:
            mysql_db=conn_mysqldb()
            mysql_db.execute("INSERT INTO user_info(user_id,password, user_name, belong, phone_number) VALUES ('%s','%s','%s','%s','%s')" % (
                str(user_id), str(password), str(user_name), str(belong), str(tele)))
            return User.find(user_id)
        else:
            return None
            
    

    @staticmethod
    def delete(user_id):
        mysql_db=conn_mysqldb()
        db_cursor=mysql_db.cursor()
        deleted=mysql_db.execute("DELETE FROM user_info WHERE user_id= '%d' " %(user_id))
        return deleted
