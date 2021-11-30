from flask import Flask,jsonify,request,render_template, make_response,session
from flask_login import LoginManager, current_user, login_required,login_user,logout_user
from flask_cors import CORS
from site_view import site_blueprint
import os #추후 확장을 위한 임포트
from site_control.user_mgmt import User


#request argument를 받는데 사용함.
#make_response http status를 받기 위해
#LoginManager:세션 관리 등록, current_user:객체 로그인 정보를 참조하기위해
#login_required:로그인된 사용자만 엑세스 가능한 api 만들기 위해 
#login_user: 로그인을 하면 해당 객체를 로그인 유저객체에 넘겨줘 세션이 만들어지고 
#logout_user: 로그아웃을 통한 세션 해제
#oauth2 보안 로그인 프로토콜 ->social login
#session: requset 요청을 한 웹브라우저의 IP주소 등을 가져올 수 있는 라이브러리

#https 만을 지원하는 기능을 http에서 테스트할 때 필요한 설정
os.environ['OAUTHLIB_INSECURE_TRANSPORT']='1'

app= Flask(__name__,static_url_path="/static")
#서버 생성, static_url_path설정을 통해 static폴더에서 html의 필요한 폴더를 가져오라고 함.
CORS(app, resources={r"/api/*": {"origins": "*"}})#CORS: 자바스크립트를 사용한 api 등의 리소스 호출시 동일 출처(같은 호스트네임)가 아니더라도 정상적으로 사용 가능하도록 도와주는 방법

app.secret_key="secret_key" #보안을 높이려면 바뀌는 코드를 넣어야하지만 그럴 경우 껏다키면 세션이 사라짐.



app.register_blueprint(site_blueprint.senior_school,url_prefix="/")
login_manager=LoginManager()
login_manager.init_app(app) #flask객체를 로그인매니저에 등록.
login_manager.session_protection="strong"  #세션코드를 보다 복잡하게 만드는 코드
# ->누군가 로그인을 할 경우 로그인 매니저에서 세션 관리


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)
#user_id를 받아와 mySQL에서 해당 아이디 기반의 레코드를 가져와 객체로 리턴.
#플라스크 내부적으로 세션으로부터 user_id를 분리해낸다.

@login_manager.unauthorized_handler
def unauthorized():
    return make_response(jsonify(success=False),401)
#로그인되지 않은 사용자가 로그인이 필요한 api에 request했을 때 자동호출되는 코드
# 로그인 실패용 html 만들고 연결시키자. 

@app.before_request#웹 브라우저가 request를 하기 전에 자동으로 호출하는 함수를 뜻함.
def app_before_request():
    if 'client_ip' not in session:
        session['client_ip']=request.environ.get('HTTP_X_REAL_IP',request.remote_addr)

if __name__=='__main__':
    app.run(host='localhost',port='8080',debug=True)