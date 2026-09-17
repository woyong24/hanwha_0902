from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# =========================
# 1. 데이터 형식 정의
# =========================

# User 요청 데이터 형식
# POST /users에서 name, age 형태로 데이터를 받기 위해 사용
class User(BaseModel):
    name: str
    age: int


# Item 기본 데이터 형식
# name, price를 가진 상품 데이터를 표현
class Item(BaseModel):
    name: str
    price: int


# Item 생성용 데이터 형식
# desc는 선택값이므로 입력하지 않아도 됨
class ItemSchema(BaseModel):
    name: str
    price: int
    desc: str | None = None


# Item 수정용 데이터 형식
# 수정 요청에서 사용할 데이터를 따로 구분하기 위해 사용
class ItemUpdate(BaseModel):
    name: str
    price: int
    desc: str


# =========================
# 2. 임시 데이터 저장소
# =========================

# DB 대신 사용하는 임시 딕셔너리
# key는 item_id(int), value는 item 정보(dict)
items_db: dict[int, dict] = {}

# 새 item을 생성할 때 자동으로 ID를 부여하기 위한 값
id_counter = 1


# FastAPI 앱 생성
app = FastAPI()


# =========================
# 3. 기본 GET 요청
# =========================

# 최상위 루트
# 서버가 정상 실행되는지 간단히 확인할 때 사용
@app.get("/")
async def root():
    return {"message": "ㅎㅇㅎㅇ~"}


# 간단한 GET 요청 예제
@app.get("/hello")
async def hello():
    return {"message": "Hello"}


# 사용자 목록 조회
@app.get("/users")
async def users():
    return {
        "users": [
            {"id": 1, "name": "Kim"},
            {"id": 2, "name": "Park"},
            {"id": 3, "name": "Lee"}
        ]
    }


# =========================
# 4. POST 요청
# =========================

# User 생성 요청
# BaseModel을 이용해 요청 Body의 형식을 검사
@app.post("/users")
async def create_user(user: User):
    return {
        "message": "User created",
        "user": user
    }
