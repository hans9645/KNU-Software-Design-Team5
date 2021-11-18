import pymongo
from flask import Flask

MONGO_HOST='localhost'
mongo_conn= pymongo.MongoClient('mongodb://%s' % (MONGO_HOST))

def conn_mongodb(mongo_conn):
    try:
        mongo_conn.admin.command('ismaster')
        blog_ab=mongo_conn.blog_session_db.blog_ab
    except:
        mongo_conn=pymongo.MongoClient('mongodb://%s'% (MONGO_HOST))
        blog_ab=mongo_conn.blog_session_db.blog_ab
    return blog_ab