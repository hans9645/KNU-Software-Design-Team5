from flask import Flask,Blueprint,request,render_template,redirect,make_response,jsonify,url_for,session,g
from site_control.user_mgmt import User
from flask_login import login_user,current_user,logout_user
from site_control.ariticles_mgmt import Article
import datetime
from site_control.site_sessionmgmt import BlogSession
from flask import flash
import bcrypt
import jwt

#sqlalchemy에서 Members 클래스 가져온다

#register에서 DB에 저장하려면 db객체가 필요한데 다른 데서 끌고올 방법을 모르겠네요...



#login_user:서버단에서 세션 쿠키셋관련 임포트
#current_user: 세션확인 할 때 사용
#main코드에 app에 최초 before request함수를 정의해둬서 블루프린트로 정의된 라우팅으로 들어와도 자동으로 before requset가 실행됨.
senior_school=Blueprint('senior_school',__name__)



########################################## 홈페이지 로그인 확인 후 렌더링 #############################
@senior_school.route('/home')
def home():
    '''
    #로그인 세션정보가 없을 경우
    if not session.get('user_id'):
        return render_template('home.html')
    #로그인 세션정보('userid')가 있을 경우
    else:
        user_id=session.get('user_id')
        return render_template('home.html', user_id=user_id)
    '''
    #세션확인 후 구독이력 확인
    if current_user.is_authenticated:
        rows = Article.get_home_board()
        return render_template('home.html',rows=rows)
        #return render_template("home.html",user_id=current_user.user_id)#여기에 jinja2에 들어갈 변수를 같이 넣어준다.
    else:
        rows = Article.get_home_board()
        return render_template('home.html', rows=rows)
   
# <---  로그인 확인 후 로그인 하지않았다면 로그인 페이지, 벌써 로그인 중이라면 홈 요청 및 로그인 아이디도 같이 넘겨줌  --->


#########it 기술##########
@senior_school.route('/tech_description/')
def tech():
    return render_template("it_tech.html")

@senior_school.route('/wifi_tech/')
def wifi():
    return render_template("wifi_desc.html")

@senior_school.route('/bluetooth_tech/')
def bluetooth_tech():
    return render_template("bluetooth_desc.html")


#######################################  게시판 관련 라우팅 #####################################

@senior_school.route('/bullet/')
def bullet():
    #page = request.args.get('page', type=int, default=1) 
    rows=Article.get_board()
    #rows=rows.paginate(page, per_page=10)
    
    return render_template("bulletBoard.html", rows=rows)

@senior_school.route('/article_page/<title>/<context>')
def article_page(title,context):
    return render_template("article.html",title=title, row=context)


@senior_school.route('/write_article')
def write_article():
    return render_template('write_article.html')


@senior_school.route('/delete_article/<title>')
def delete_article_article(title):
    if current_user.is_authenticated :
        if Article.check_owe(current_user.user_id,title=title)==1:
            row = Article.delete(current_user.user_id,title)
            return redirect('/bullet')
        else:
            return render_template('home.html'),401
    else:
        return redirect('/login_register')

@senior_school.route('/posting',methods=['POST'])
def posting():
    if current_user.is_authenticated:
        wuser_id=current_user.user_id
        title=request.form['title']
        context=request.form['context']
        Article.write_post(wuser_id,title,context)
        return redirect('/bullet')
    else:
        #flash("로그인 해주세요")
        return redirect('/login_register')



###################################### 가입 및 로그인 라우팅 #######################################
@senior_school.route('/set_register', methods=['POST'])
def set_register():
    en_password=bcrypt.hashpw(request.form['password'].encode('UTF-8'),bcrypt.gensalt()) #암호화
    #VARCHAR 에 맞게 decode해서 문자열로 변환
    #en_password = en_password.decode('UTF-8')
    user=User.create(request.form['user_id'],en_password,request.form['user_name'])
    print(en_password)
    if(user == None):
        return "같은 아이디가 존재합니다", 400
    
    #session['user_id'] = user.user_id    #user_id를 세션에 저장한다.
    #return render_template('home.html', user_id=request.form['user_id'])
    login_user(user,remember=True, duration=datetime.timedelta(days=30))
    return redirect('/home') 

@senior_school.route('/set_login', methods=['GET','POST'])
def login():
    if request.method == 'GET':
        return "wrong route",401
    else:
        user_id=request.form['user_id']
        password=request.form['password']

    try:
        # ID/PW 조회Query 실행
        user = User.find(user_id)

        if user.user_id == user_id and bcrypt.checkpw(password.encode('utf-8'),user.password):    #쿼리 데이터가 존재하면
            login_user(user,remember=True, duration=datetime.timedelta(days=30))
            #session['user_id'] = user_id    #user_id를 세션에 저장한다.
            return redirect("/home")
        else:
            return '비밀번호가 맞지 않습니다', 400 #아이디는 맞는데 비번 틀릴때
    except:
        return "존재하지 않는 아이디입니다", 400  #테이블에 user_id 자체가 없을때   

  
@senior_school.route('/login_register')
def login_register():
    return render_template("login_register.html")


############################################################################

################################# 로그아웃 ####################################
@senior_school.route('/logout')
def logout():
    logout_user() #어차피 라우팅 리퀘스트시 세션에 로그인 정보가 있다.
    return render_template("home.html")
    #return redirect('/home')
##########################################################################


@senior_school.route('/macdonalds')
def macdonalds():
    return render_template('macdonalds.html')




@senior_school.route('/fullstack')
def fullstack():    
    if current_user.is_authenticated:#세션확인 후 구독이력 확인
        web_page=BlogSession.get_blog_page(current_user.blog_id)#구독시 페이지정보  
        BlogSession.save_session_info(session['client_id'],current_user.user_email,web_page)
        #로그인한 방문자의 IP등을 세션라이브러리로부터 받아와서 넣는다.      
        return render_template(web_page,user_email=current_user.user_email)#여기에 jinja2에 들어갈 변수를 같이 넣어준다.
    else:
        web_page=BlogSession.get_blog_page()
        BlogSession.save_session_info(session['client_id'],'anonymous',web_page)
        #로그인하지않은 방문자의 IP등을 세션라이브러리로부터 받아와서 넣는다.
        return render_template(web_page)

'''
@senior_school.route('/logout')
def logout():
    User.delete(user_id=current_user.id)
    logout_user() #어차피 라우팅 리퀘스트시 세션에 로그인 정보가 있다.
    return redirect(url_for('blog_bp.fullstack'))


@senior_school.route('/set_login',methods=['GET','POST'])
def set_email():
    if request.method=='GET':
        #print('http check',request.headers)
        print("set_email()",request.args.get('user_email'))
        #return make_response(jsonify(success=True),200) 
        #->vue와 같은 js를 사용하지 않고 서버단에서 풀스택을 구현하는 거라 전체페이지를 리로딩하는 식으로한다.
        #return redirect(url_for('blog_bp.engA'))
        return redirect(url_for(request.form['blog_id']))
    else:
        #print('http check',request.headers)
        #http request의 헤더부분을 가져올 수 있다. 이후 content type를 확인하고 데이터를 어떻게 가져와야하는지 고민하자.
        #content type이 application/json인 경우에는 request.get_json()
        #->print('set_email',request.get_json())
        #print('blog_id',request.form['blog_id'])
        #print('only user_email',request.form['user_email'])
        #post방식으로 데이터를 가져올 수 있다. vue에서 했었음
        ID=request.form['user_id']
        PW=request.form['password']
        login_user(user,remember=True, duration=datetime.timedelta(days=30))
        #로그인 기록유지 시킴 remember me,flask_login google검색
        #세션정보가 플라스크에서 만들어져 셋쿠키로 웹브라우저에 전송, 웹브라우저는 서버주소와 쿠키를 저장,관리를 하면서 다음에 해당서버에 request를 할 때 사용한다. 
        #return redirect(url_for(request.form['blog_id']))
        return redirect('/blueprint/fullstack')
'''

@senior_school.route('/board_main',methods=['GET','POST'])
def board_main():
    print('site control에서 article_mgmt안에 게시판 관련된 클래스 선언 후(mysql과 연결) 관련 내용을 받아와서 일단 프린트 하도록 만들기.')
    #site control에서 article_mgmt안에 게시판 관련된 클래스 선언 후(mysql과 연결) 관련 내용을 받아와서 일단 프린트 하도록 만들기.
