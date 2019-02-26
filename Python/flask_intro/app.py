#플라스크 모듈 import
import random
from flask import Flask,render_template
from faker import Faker
import requests

app = Flask(__name__)

#url route 설정
@app.route("/")
def hello():
    return "Hello World!"
    
@app.route("/multi_c")
def multi():
    return "멀캠C반"
    
@app.route("/html_tag")
def html_tag():
    return """
    <h1>html 태그도 보낼 수 있어요</h1>
    <p>안녕하세요</p>
    """
@app.route("/html_file")
def html_file():
    return render_template("html.html")
    #새로운 폴더를 templates로 만들어서 html 파일을 추가한다.
    
@app.route("/hi/<string:name>") #<date형식 : data를 담을 변수>
def hi(name):
    return render_template("hi.html", name=name)
    
@app.route("/cube/<int:num>") #인자 값을 받아올 때는 함수 안에 넣어줘야 사용 가능
def cube(num) :
    cubic_num = num ** 3 #**두개 쓰면 지수를 사용할 수 있다.
    return render_template("cube.html",num=num, cubic_num=cubic_num) #, 뒤에 원하는 변수를 html에게 전달하여 줄 수 있다.

@app.route("/dinner")
def dinner():
    menu_list = ["엽떡", "뿌링클", "치즈볼"]
    pick = random.choice(menu_list) #한개의 랜덤을 뽑을 때는 choice
    return render_template("dinner.html", pick=pick)
    
@app.route("/lotto")
def lotto():
    number = range(1,46)
    pick = random.sample(number,6) # 난수를 여러개 뽑을 때는 sample
    return render_template("lotto.html", pick = pick) #python 코드를 html 에서도 사용할 수 있도록 해준다.
    
@app.route("/random_img")
def random_img():
    return render_template("random_img.html")
    
@app.route("/ego/<string:name>")
def ego(name):
    url = "http://api.giphy.com/v1/gifs/search?api_key=x4rhsV9fqHmv0bLBSbd6I9Gb7J0f0EIu&q="
    fake = Faker("ko_KR")
    job = fake.job()
    res = requests.get(url+job).json() #요청 보내기, json을 딕셔너리 형태로 바꿔준다.
    #json은 파이썬의 딕셔너리 형태와 유사하다.
    img_url = res["data"][0]["images"]["original"]["url"]
    
    return render_template("ego.html",img_url=img_url, name=name, job=job)
    
#server 실행 옵션    
if __name__ == '__main__':
    app.run(debug = True, host = '0.0.0.0', port = 8080)
    #debug 모드를 on으로 설정하면, 파일의 내용이 수정되면 자동으로 서버를 껐다켠다.