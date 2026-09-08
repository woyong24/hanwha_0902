FastAPI 기초 복습 노트

비전공자 기준으로 "코드가 왜 필요한지"와 "주소창에서 어떻게 확인하는지" 중심으로 정리한 노트입니다.

1. FastAPI가 뭐냐

FastAPI는 파이썬으로 API 서버를 만들 때 사용하는 프레임워크다.

쉽게 생각하면:

특정 주소로 요청이 들어오면

그 주소에 연결해 둔 파이썬 함수를 실행하고

결과를 JSON 형태로 돌려주는 방식이다.

예:

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

브라우저에서 아래 주소로 들어가면:

http://127.0.0.1:8000/

결과:

{"Hello":"World"}

2. 설치

가상환경을 켠 상태에서 설치하는 것이 좋다.

pip 업데이트

python -m pip install --upgrade pip

FastAPI 설치

python -m pip install "fastapi[standard]"

[standard]를 붙이면 FastAPI와 함께 개발에 자주 필요한 패키지도 같이 설치된다.

설치 확인:

python -m pip show fastapi

가상환경을 폴더마다 따로 만들었다면, 각 가상환경마다 FastAPI를 따로 설치해야 한다.

3. 서버 실행

파일명이 pratice2.py라면:

fastapi dev pratice2.py

또는:

uvicorn pratice2:app --reload

여기서:

pratice2 = 파일명 pratice2.py에서 .py를 뺀 것

app = 코드의 app = FastAPI()에서 변수명

--reload = 코드 저장 시 서버 자동 재시작

파일명이 바뀌면 실행 명령어의 파일명도 바꿔야 한다.

예:

practice.py

라면:

fastapi dev practice.py

Path does not exist 오류

Path does not exist pratice2.py

이 오류는 현재 터미널 위치에 해당 파일이 없다는 뜻이다.

CMD에서 확인:

dir /b

현재 폴더에 실제 파일명이 무엇인지 확인하면 된다.

4. 접속 주소와 포트

기본 주소:

http://127.0.0.1:8000

또는:

http://localhost:8000

개발 환경에서는 둘 다 자기 컴퓨터를 가리킨다고 보면 된다.

8000은 Uvicorn의 기본 포트 번호다.

쉽게 생각하면:

127.0.0.1 = 내 컴퓨터
8000 = 그 컴퓨터에서 FastAPI 서버가 사용하는 번호

원하면 포트를 바꿀 수 있다.

uvicorn pratice2:app --reload --port 3000

그러면:

http://127.0.0.1:3000

으로 접속한다.

5. /docs

FastAPI는 API를 테스트할 수 있는 문서 화면을 자동으로 만들어준다.

http://127.0.0.1:8000/docs

여기에서 GET 경로를 선택하고 Try it out을 눌러 값을 직접 입력해볼 수 있다.

코드를 만들었는데 어떤 주소가 등록되어 있는지 헷갈리면 /docs를 먼저 확인하면 편하다.

6. 기본 GET

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/")는:

/ 주소로 GET 요청이 들어오면 아래 함수를 실행해라

라는 뜻이다.

http://127.0.0.1:8000/

결과:

{"Hello":"World"}

7. Path Parameter

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

{item_id}는 주소 안에서 값을 받는 부분이다.

예:

http://127.0.0.1:8000/items/10

여기서는:

item_id = 10

이 된다.

item_id: int라고 했기 때문에 정수만 받을 수 있다.

int_parsing 오류

예를 들어:

http://127.0.0.1:8000/items/tttt

처럼 문자를 넣으면 정수로 바꿀 수 없어서 오류가 난다.

대표 오류 내용:

"type": "int_parsing"

뜻:

item_id를 정수로 바꾸려고 했는데 실패했다.

8. Query Parameter

다시 이 코드:

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}

여기서:

q: str | None = None

은 q라는 문자열 값을 선택적으로 받을 수 있다는 뜻이다.

예:

http://127.0.0.1:8000/items/10?q=apple

결과:

{"item_id":10,"q":"apple"}

주소의 ? 뒤에 붙는 값이 Query Parameter다.

9. ?와 &

예:

http://127.0.0.1:8000/items/?skip=1&limit=2

뜻:

?skip=1

? = Query Parameter 시작

&limit=2

& = Query Parameter를 하나 더 이어서 적음

즉:

skip = 1
limit = 2

를 전달한 것이다.

10. skip과 limit

데이터:

fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

코드:

@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

의미:

skip = 앞에서 몇 개 건너뛸지

limit = 그다음 몇 개 가져올지

주소:

http://127.0.0.1:8000/items/?skip=1&limit=2

데이터 순서:

0 = Foo
1 = Bar
2 = Baz

skip=1이므로 Foo를 건너뛴다.

limit=2이므로 그다음 Bar, Baz 두 개를 가져온다.

결과:

[
  {"item_name":"Bar"},
  {"item_name":"Baz"}
]

코드 내부에서는:

fake_items_db[1 : 1 + 2]

즉:

fake_items_db[1:3]

이 실행된 것이다.

11. /item과 /items는 다르다

FastAPI에서는 주소를 정확하게 구분한다.

만약 코드에:

@app.get("/items/")

만 있다면:

/items/

는 존재하지만:

/item

은 존재하지 않는다.

그래서 /item으로 접속하면:

{"detail":"Not Found"}

가 뜬다.

12. {"detail":"Not Found"}

이 오류는 보통 404 오류다.

뜻:

내가 접속한 주소에 해당하는 경로를 FastAPI 코드에서 등록하지 않았다.

확인할 것:

주소 철자가 맞는가

item과 items를 헷갈리지 않았는가

현재 실행 중인 파이썬 파일이 맞는가

/docs에 내가 만든 경로가 실제로 보이는가

13. 같은 경로를 두 번 만들면

@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]

@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]

둘 다:

GET /users

로 동일하다.

FastAPI는 먼저 등록된 경로를 먼저 매칭한다.

따라서:

http://127.0.0.1:8000/users

로 접속하면:

["Rick","Morty"]

가 나온다.

두 번째 Bean, Elfo 함수는 같은 /users 요청으로는 사용되지 않는다.

핵심:

함수 이름보다 @app.get() 안에 적힌 경로가 중요하다.

14. 고정 경로와 동적 경로 순서

@app.get("/users/me")
async def read_user_me():
    return {"user_id": "나를 me입니다"}

@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"사용자아이디user_id": user_id}

/users/me는 고정 경로다.

/users/{user_id}는 동적 경로다.

고정 경로인 /users/me를 먼저 두는 것이 중요하다.

왜냐하면 동적 경로를 먼저 두면 me도 user_id 값으로 받아들이는 상황이 생길 수 있기 때문이다.

15. Enum으로 입력값 제한

from enum import Enum

class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"

이렇게 하면 모델 이름을 미리 정해둘 수 있다.

@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):
    ...

이제 model_name에는 아무 문자열이나 들어가는 것이 아니라 정해둔 값 중 하나가 들어오도록 제한할 수 있다.

테스트:

http://127.0.0.1:8000/models/alexnet
http://127.0.0.1:8000/models/lenet
http://127.0.0.1:8000/models/resnet

/docs에서는 선택 가능한 값이 표시되어 테스트하기 편하다.

16. app = FastAPI()는 보통 한 번만

파일 중간에서 다시:

app = FastAPI()

를 실행하면 새로운 FastAPI 앱을 만들어버린다.

예:

app = FastAPI()

@app.get("/users")
def users():
    ...

app = FastAPI()

두 번째 app = FastAPI() 이후에는 첫 번째 앱에 등록했던 /users가 현재 app에 없는 상태가 될 수 있다.

따라서 기본적으로:

app = FastAPI()

는 파일 위쪽에서 한 번만 만들고 계속 사용하는 것이 좋다.

17. 현재 연습 코드

from fastapi import FastAPI
from enum import Enum

# 연습용 데이터
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# FastAPI 앱 생성
# 보통 파일에서 한 번만 만든다.
app = FastAPI()


# 고정 경로
# http://localhost:8000/users/me
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "나를 me입니다"}


# Path Parameter
# user_id 자리에 원하는 문자열을 넣을 수 있다.
# 예: http://localhost:8000/users/kim
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"사용자아이디user_id": user_id}


# 같은 GET 경로가 두 개면 먼저 등록된 것이 사용된다.
# http://localhost:8000/users
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]


# 가장 기본 주소
# http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Path Parameter + Query Parameter
# 예: http://127.0.0.1:8000/items/10
# 예: http://127.0.0.1:8000/items/10?q=apple
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# model_name으로 받을 수 있는 값을 미리 제한
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# Enum 테스트
# http://127.0.0.1:8000/models/alexnet
# http://127.0.0.1:8000/models/lenet
# http://127.0.0.1:8000/models/resnet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):

    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }

    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }

    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }


# Query Parameter 연습
# skip = 앞에서 몇 개 건너뛸지
# limit = 그다음 몇 개 가져올지
#
# 전체 보기:
# http://127.0.0.1:8000/items/
#
# Foo를 건너뛰고 Bar, Baz 두 개 가져오기:
# http://127.0.0.1:8000/items/?skip=1&limit=2
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]

18. 지금 단계에서 기억할 것

FastAPI를 처음 배울 때는 우선 아래 흐름만 잡으면 된다.

1. app = FastAPI()로 앱 생성

2. @app.get("/주소")로 경로 생성

3. 주소 안의 {값}은 Path Parameter

4. ?key=value 형태는 Query Parameter

5. Query Parameter가 여러 개면 &로 연결

6. return으로 결과 반환

7. /docs에서 API 테스트

8. 없는 주소로 들어가면 404 Not Found

9. 타입을 int로 지정했는데 문자를 넣으면 검증 오류

10. 같은 GET + 같은 경로가 중복되면 먼저 등록된 경로가 사용됨