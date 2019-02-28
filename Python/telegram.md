# Telegram을 이용해 chatbot 만들기

- Telegram을 설치하고 BotFather을 추가, 새로운 chatbot을 생성한다.
- message.py를 다음과 같이 작성한다.

```python
import requests

token = "###"
chat_id = "###"
# url = f"https://api.telegram.org/bot{token}/sendMessage?chat_id={chat_id}&text=안녕하세요"
url = f"https://api.hphk.io/telegram/bot{token}/sendMessage?chat_id={chat_id}&text=안녕하세요"

res = requests.get(url)
print(res)
# print(url)
```

> 안녕하세요

- c9에서 작업할 경우 chatbot 생성을 막아놓았기 때문에 경로를 api.telegram.org로 작성하면 실행되지 않는다.
- 따라서 우회하는 url을 작성하여 실행한다.
- 지난번에 배웠던 챗봇 기능들을 하나씩 추가해보도록 하자.



## token값 환경변수로 지정하기

- github에 token, api key 등을 사용하게되면 유출될 가능성이 있으므로 감춰두는게 좋다.
- vi로 bashrc 파일을 실행한다.
- 마지막줄에 다음을 추가한다.

```bash
export TELE_TOKEN="###"
```

- 이를 통해 해당 컴퓨터가 아니면 token값을 이용할 수 없게 만들 수 있다.

- 다시 app.py로 돌아와 다음과 같이 token 값을 지정해준다.

```python
import = os
token = os.getenv("TELE_TOKEN")
```

- 설정을 마친 후엔 bash로 꼭 다음 명령어를 수행해주어야 한다.

```bash
$ exec $SHELL
$ echo $TELE_TOKEN
```

- echo 명령어를 수행했을 때 입력한 token값이 반환되면 성공적으로 설정된 것이다.



## 코스피 지수 가져오기

- 다음 내용을 추가해보자.

```python
from bs4 import BeautifulSoup

url = f"https://api.hphk.io/telegram/bot{token}/sendMessage?chat_id={chat_id}&text="

sise_url = "https://finance.naver.com/sise/"
sise_html = requests.get(sise.url).text
sise_soup = BeautifulSoup(sise_html, "html.parser")
sise = sise_soup.select("#KOSPI_now").text

res = requests.get(url+sise)
```

> 2,229.36



## 로또 기능 추가하기

- 다음 코드로 간단하게 로또번호도 전송할 수 있다.

```python
import random

lotto = str(random.sample(range(1, 46), 6))
res = requests.get(url+lotto)
```



## app.py로 flask 구성하기

- 지금까지 일방적으로 메시지를 보내는 기능을 구현했다면, 이제는 통신을 통해 메시지를 주고받는 기능을 구현할 것이다.
- app.py 파일을 작성한 뒤 다음과 같이 작성한다.

```python
from flask import Flask
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello World!"
    
if __name__ == "__main__" :
    app.run(host="0.0.0.0", port=8080)
```

- 요청 받은 명령어에 대해서 특정 함수를 실행하려면 우선 telegram으로부터 요청받았다는 사실을 c9 서버로 알려야 한다.
- 이를 web hook이라고 한다.
- https://api.telegram.org/bot<token값>/setWebhook?url=<서버주소>/<token값> 명령을 url로 수행하자.
- 이때 서버주소는 http를 https로 수정하고, 포트번호를 지워주어야 한다.

![1551320557290](assets/1551320557290.png)

- 이런 json 파일을 받았다면 성공적으로 webhook이 만들어진 상태이다.

```python
@app.route(f"/{token}", methods=["POST"])
def telegram():
    msg_info = request.get_json()
    chat_id = msg_info.get("message").get("from").get("id")
    text = msg_info.get("message").get("text")
    
    return_url = f"{api_url}/bot{token}/sendMessage?chat_id={chat_id}&text={text}"
    requests.get(return_url)
    
    return '', 200
```

> ![1551321811191](assets/1551321811191.png)

- 이제 이런 식으로 루트를 추가하면 보내는 메시지에 똑같이 답하는 기능이 추가되는 것을 볼 수 있다.

