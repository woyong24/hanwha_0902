# FastAPI 기초

## 1. FastAPI란?

FastAPI는 Python으로 **API 서버를 만들기 위한 웹 프레임워크**이다.

쉽게 말하면:

```text
특정 주소로 요청
→ 연결된 Python 함수 실행
→ 결과를 JSON 형태로 반환
```

기본 형태:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}
```

접속:

```text
http://127.0.0.1:8000/
```

결과:

```json
{
  "Hello": "World"
}
```

---

# 2. 설치

가상환경을 활성화한 상태에서 설치하는 것이 좋다.

## pip 업데이트

```bash
python -m pip install --upgrade pip
```

## FastAPI 설치

```bash
python -m pip install "fastapi[standard]"
```

`[standard]`를 붙이면 FastAPI와 함께 개발에 자주 사용하는 패키지도 설치된다.

설치 확인:

```bash
python -m pip show fastapi
```

가상환경을 폴더마다 따로 만들었다면 **각 가상환경마다 FastAPI를 설치해야 한다.**

---

# 3. 서버 실행

파일명이 `practice2.py`라면:

```bash
fastapi dev practice2.py
```

또는:

```bash
uvicorn practice2:app --reload
```

의미:

```text
practice2 → practice2.py에서 .py를 제외한 파일명
app       → app = FastAPI()의 변수명
--reload  → 코드 저장 시 서버 자동 재시작
```

파일명이 바뀌면 실행 명령어도 실제 파일명에 맞춰야 한다.

---

## Path does not exist

예:

```text
Path does not exist practice2.py
```

현재 터미널 위치에 해당 파일이 없다는 의미이다.

CMD에서 확인:

```bash
dir /b
```

현재 폴더와 실제 파일명을 확인한다.

---

# 4. 접속 주소와 포트

FastAPI 개발 서버의 기본 주소:

```text
http://127.0.0.1:8000
```

또는:

```text
http://localhost:8000
```

개발 환경에서는 둘 다 현재 내 컴퓨터를 가리킨다고 보면 된다.

```text
127.0.0.1 → 내 컴퓨터
8000      → FastAPI 서버가 사용하는 포트
```

포트 변경:

```bash
uvicorn practice2:app --reload --port 3000
```

접속:

```text
http://127.0.0.1:3000
```

---

# 5. Swagger UI

FastAPI는 API를 직접 테스트할 수 있는 문서 화면을 자동으로 제공한다.

```text
http://127.0.0.1:8000/docs
```

Swagger UI에서는:

- 등록된 API 경로 확인
- Path / Query Parameter 입력
- API 요청 실행
- 응답 결과 확인

등을 할 수 있다.

경로가 제대로 등록되었는지 헷갈리면 `/docs`에서 먼저 확인하면 편하다.

---

# 6. 기본 GET 요청

```python
@app.get("/")
def read_root():
    return {"Hello": "World"}
```

```python
@app.get("/")
```

의 의미:

```text
/ 주소로 GET 요청이 들어오면
아래 함수를 실행
```

`return` 값이 클라이언트에게 응답으로 전달된다.

---

# 7. Path Parameter

URL의 일부를 변수처럼 사용하는 방법이다.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int):
    return {"item_id": item_id}
```

예:

```text
http://127.0.0.1:8000/items/10
```

이면:

```text
item_id = 10
```

이 된다.

---

## int_parsing 오류

```python
item_id: int
```

로 지정하면 정수만 받을 수 있다.

따라서:

```text
/items/tttt
```

처럼 문자열을 입력하면 정수로 변환할 수 없어 검증 오류가 발생한다.

대표 오류:

```text
int_parsing
```

---

# 8. Query Parameter

주소 뒤에 추가적인 값을 전달할 때 사용한다.

```python
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "q": q
    }
```

예:

```text
http://127.0.0.1:8000/items/10?q=apple
```

결과:

```json
{
  "item_id": 10,
  "q": "apple"
}
```

```python
q: str | None = None
```

은 `q`에 문자열을 받을 수 있지만 **입력하지 않아도 된다**는 의미이다.

---

# 9. ?와 &

Query Parameter는 `?` 뒤에서 시작한다.

```text
/items/?skip=1&limit=2
```

의미:

```text
?       → Query Parameter 시작
skip=1  → 첫 번째 값
&       → 다음 Query Parameter 연결
limit=2 → 두 번째 값
```

---

# 10. skip과 limit

여러 데이터 중 일부만 가져올 때 사용할 수 있다.

```python
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]
```

```python
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

의미:

```text
skip  → 앞에서 몇 개 건너뛸지
limit → 그다음 몇 개 가져올지
```

예:

```text
/items/?skip=1&limit=2
```

실행되는 범위:

```python
fake_items_db[1:3]
```

결과:

```json
[
  {"item_name": "Bar"},
  {"item_name": "Baz"}
]
```

---

# 11. 경로는 정확하게 구분된다

FastAPI는 URL 경로를 정확하게 구분한다.

예를 들어:

```python
@app.get("/items/")
```

만 등록했다면 `/item`은 별개의 경로이다.

등록되지 않은 주소로 요청하면:

```json
{
  "detail": "Not Found"
}
```

가 나타난다.

`404 Not Found`가 발생하면 다음을 확인한다.

```text
주소 철자가 맞는가
item / items를 잘못 입력하지 않았는가
현재 실행 중인 Python 파일이 맞는가
/docs에 해당 경로가 등록되어 있는가
```

---

# 12. 같은 Method + 같은 경로 중복

다음처럼 같은 GET 경로를 두 번 만들 수는 있지만 피하는 것이 좋다.

```python
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]
```

둘 다:

```text
GET /users
```

이므로 먼저 등록된 경로가 실제 요청에서 먼저 매칭된다.

따라서 `/users` 요청 결과는:

```json
[
  "Rick",
  "Morty"
]
```

이 된다.

핵심:

```text
함수 이름보다
HTTP Method + 경로가 중요하다.
```

단, 같은 경로라도 Method가 다르면 다른 API이다.

```text
GET  /users
POST /users
```

은 함께 사용할 수 있다.

---

# 13. 고정 경로와 동적 경로의 순서

```python
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "me"}


@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}
```

여기서:

```text
/users/me        → 고정 경로
/users/{user_id} → 동적 경로
```

고정 경로를 먼저 작성하는 것이 중요하다.

동적 경로를 먼저 작성하면:

```text
/users/me
```

의 `me`를 `user_id` 값으로 인식할 수 있기 때문이다.

---

# 14. Enum으로 입력값 제한

입력 가능한 값을 미리 정해둘 수 있다.

```python
from enum import Enum


class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"
```

FastAPI에서 사용:

```python
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
```

이제 `model_name`에는:

```text
alexnet
resnet
lenet
```

중 하나만 받을 수 있다.

Swagger UI에서도 선택 가능한 값이 표시된다.

---

# 15. app = FastAPI()는 보통 한 번만

```python
app = FastAPI()
```

는 FastAPI 애플리케이션 자체를 만드는 코드이다.

파일 중간에서 다시:

```python
app = FastAPI()
```

를 실행하면 새로운 FastAPI 앱을 만들게 된다.

따라서 이전 `app`에 등록했던 경로가 현재 `app`에는 없는 상황이 발생할 수 있다.

기본적으로 파일 상단에서:

```python
app = FastAPI()
```

를 한 번 만들고 계속 사용하는 것이 좋다.

---

# 16. 전체 연습 코드

```python
from fastapi import FastAPI
from enum import Enum


# 연습용 데이터
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]


# FastAPI 앱 생성
app = FastAPI()


# 고정 경로
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "me"}


# 동적 경로
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"user_id": user_id}


# 기본 GET
@app.get("/")
def read_root():
    return {"Hello": "World"}


# Path Parameter + Query Parameter
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {
        "item_id": item_id,
        "q": q
    }


# Enum
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


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


# Query Parameter
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]
```

---

# 어제 핵심 정리

```text
FastAPI()
→ FastAPI 앱 생성

@app.get("/주소")
→ GET 요청을 받을 경로 등록

{item_id}
→ Path Parameter

?key=value
→ Query Parameter

&
→ 여러 Query Parameter 연결

/docs
→ Swagger UI에서 API 확인 및 테스트

404 Not Found
→ 등록되지 않은 경로를 요청했을 때 발생

int_parsing
→ int로 받아야 하는 값에 문자열 등을 입력했을 때 발생

같은 Method + 같은 경로
→ 중복을 피해야 하며 먼저 등록된 경로가 요청에 먼저 매칭될 수 있음

고정 경로 /users/me
→ 동적 경로 /users/{user_id}보다 먼저 작성

Enum
→ 입력 가능한 값을 미리 제한

app = FastAPI()
→ 보통 하나의 파일에서 한 번 생성
```

## 전체 흐름

```text
FastAPI 앱 생성
→ 경로 등록
→ GET 요청
→ Path Parameter
→ Query Parameter
→ 타입 검증
→ 경로 순서 및 중복 이해
→ Enum으로 값 제한
→ /docs에서 테스트
```