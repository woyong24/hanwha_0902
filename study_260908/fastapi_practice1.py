from fastapi import FastAPI
from enum import Enum

# 연습용 가짜 데이터
fake_items_db = [
    {"item_name": "Foo"},
    {"item_name": "Bar"},
    {"item_name": "Baz"}
]

# FastAPI 앱 생성
# 보통 파일에서 한 번만 만든다.
app = FastAPI()


# 1. 고정 경로
# http://localhost:8000/users/me
@app.get("/users/me")
async def read_user_me():
    return {"user_id": "나를 me입니다"}


# 2. Path Parameter
# {user_id} 자리에 원하는 문자열을 넣을 수 있음
# 예: http://localhost:8000/users/kim
@app.get("/users/{user_id}")
async def read_user(user_id: str):
    return {"사용자아이디user_id": user_id}


# 3. 같은 경로 중복 예제
# http://localhost:8000/users
@app.get("/users")
async def read_users():
    return ["Rick", "Morty"]


# 위와 GET 방식과 경로가 완전히 같기 때문에
# /users로 들어가면 위의 Rick, Morty가 먼저 사용됨
@app.get("/users")
async def read_users2():
    return ["Bean", "Elfo"]


# 4. 가장 기본적인 GET
# http://127.0.0.1:8000/
@app.get("/")
def read_root():
    return {"Hello": "World"}


# 5. Path Parameter + Query Parameter
# item_id는 주소 안에서 받음
# q는 ?q=apple 같은 방식으로 받음
#
# http://127.0.0.1:8000/items/10
# http://127.0.0.1:8000/items/10?q=apple
@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    return {"item_id": item_id, "q": q}


# 6. Enum
# model_name으로 받을 수 있는 값을 미리 제한함
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


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

    # alexnet도 아니고 lenet도 아니면 resnet
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }


# 7. Query Parameter로 목록 일부만 가져오기
#
# skip = 앞에서 몇 개 건너뛸지
# limit = 그다음 몇 개 가져올지
#
# 전체 보기
# http://127.0.0.1:8000/items/
#
# Foo 1개를 건너뛰고 Bar, Baz 2개 가져오기
# http://127.0.0.1:8000/items/?skip=1&limit=2
@app.get("/items/")
async def read_items(skip: int = 0, limit: int = 10):
    return fake_items_db[skip : skip + limit]