from db_model.mongoDB import conn_mongodb
from datetime import datetime

class BlogSession():
    blog_page={'A':'blog_engA.html','B':'blog_engB.html'}
    session_count=0

    @staticmethod
    def save_session_info(session_ip,user_email, webpage_name):
                            #접속 때마다 접속정보를 mongodb에 저장하는 함수
        now =datetime.now()
        now_time=now.strftime("%d-%m-%Y %H:%M:%S") #https:strftime.org

        mongo_db=conn_mongodb(conn_mongodb)
        mongo_db.insert_one({
            'session_ip':session_ip,
            'user_email':user_email,
            'page':webpage_name,
            'access_time':now_time
             }) 

    
    @staticmethod
    def get_blog_page(blog_id=None):#인자를 안넣어도 되고 넣으면 사용가능하게 하는 문법.
        if blog_id==None:
            if BlogSession.session_count==0:
                BlogSession.session_count=1
                return BlogSession.blog_page['A']
            else:
                BlogSession.session_count=0
                return BlogSession.blog_page['B']
        else:
            return BlogSession.blog_page[blog_id]