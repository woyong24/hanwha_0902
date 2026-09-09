# FastAPI 기초 및 CRUD

## 1. FastAPI란?

FastAPI는 Python으로 API 서버를 만들 수 있는 웹 프레임워크이다.

```python
from fastapi import FastAPI

app = FastAPI()
```

`app = FastAPI()`로 FastAPI 애플리케이션을 생성한다.

---

## 2. FastAPI 실행

FastAPI 기본 패키지와 실행에 필요한 기능을 함께 설치한다.

```bash
python -m pip install "fastapi[standard]"
```

실행:

```bash
fastapi dev main.py
```

또는:

```bash
python -m uvicorn main:app --reload
```

---

## 3. Swagger UI

FastAPI는 API를 테스트할 수 있는 문서를 자동으로 만들어준다.

```text
http://127.0.0.1:8000/docs
```

Swagger UI에서는 GET, POST, PUT, DELETE 요청을 직접 테스트할 수 있다.

---

# 4. HTTP 요청

## GET

서버의 데이터를 조회할 때 사용한다.

```python
@app.get("/hello")
async def hello():
    return {"message": "Hello"}
```

```text
GET /hello
```

---

## POST

새로운 데이터를 생성할 때 사용한다.

```python
@app.post("/users")
async def create_user(user: User):
    return {
        "message": "User created",
        "user": user
    }
```

POST 요청은 주소창에서 직접 테스트하기보다 Swagger UI에서 Request Body를 입력하여 테스트한다.

---

## PUT

기존 데이터를 수정할 때 사용한다.

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemSchema):
    ...
```

`{item_id}`는 수정할 데이터의 ID를 URL에서 전달받는 Path Parameter이다.

---

## DELETE

기존 데이터를 삭제할 때 사용한다.

```python
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):
    ...
```

---

# 5. Pydantic BaseModel

API로 들어오는 데이터의 형식을 정의하고 검증할 때 사용한다.

```python
from pydantic import BaseModel

class ItemSchema(BaseModel):
    name: str
    price: int
    desc: str | None = None
```

```python
desc: str | None = None
```

은 `desc`에 문자열을 넣을 수도 있고, 입력하지 않아도 된다는 의미이다.

---

# 6. 임시 데이터 저장소

DB를 사용하지 않고 Python 딕셔너리를 임시 데이터베이스처럼 사용할 수 있다.

```python
items_db: dict[int, dict] = {}
```

의미:

```text
key   → int 형태의 item_id
value → dict 형태의 item 데이터
```

예시:

```python
{
    1: {"id": 1, "name": "Keyboard", "price": 50000},
    2: {"id": 2, "name": "Mouse", "price": 30000}
}
```

---

## id_counter

새로운 데이터를 생성할 때 ID를 자동으로 부여하기 위해 사용한다.

```python
id_counter = 1
```

새로운 item이 생성될 때마다:

```python
id_counter += 1
```

하여 다음 ID를 준비한다.

함수 내부에서 바깥의 `id_counter` 값을 변경하려면:

```python
global id_counter
```

를 사용한다.

---

# 7. CRUD

CRUD는 데이터를 생성, 조회, 수정, 삭제하는 기본 기능이다.

```text
Create → POST   → 생성
Read   → GET    → 조회
Update → PUT    → 수정
Delete → DELETE → 삭제
```

---

## Create 생성

```python
@app.post("/items/", status_code=201)
async def create_item(item: ItemSchema):
    global id_counter

    new_item = item.model_dump()
    new_item["id"] = id_counter

    items_db[id_counter] = new_item
    id_counter += 1

    return items_db
```

주요 흐름:

```text
데이터 받기
→ dict로 변환
→ ID 추가
→ items_db 저장
→ ID 증가
```

`status_code=201`은 새로운 데이터가 정상적으로 생성되었다는 의미이다.

---

## Read 전체 조회

```python
@app.get("/items")
async def get_all_items():
    return {
        "msg": "전체 목록 조회 완료",
        "data": list(items_db.values())
    }
```

```python
items_db.values()
```

는 딕셔너리의 value만 가져온다.

`list()`로 감싸 전체 item을 리스트 형태로 반환한다.

---

## Read 단일 조회

```python
@app.get("/items/{item_id}")
async def get_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    return {
        "msg": "단일 조회 완료",
        "data": items_db[item_id]
    }
```

예:

```text
/items/1
```

을 요청하면 ID가 1인 item만 조회한다.

---

## Update 수정

```python
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemSchema):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    updated_data = item.model_dump()
    updated_data["id"] = item_id

    items_db[item_id] = updated_data

    return {
        "msg": "수정 완료",
        "data": updated_data
    }
```

기존 `item_id`는 유지하면서 새로운 데이터로 교체한다.

---

## Delete 삭제

```python
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):

    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    deleted_item = items_db.pop(item_id)

    return {
        "msg": "삭제 완료",
        "data": deleted_item
    }
```

```python
items_db.pop(item_id)
```

은 해당 데이터를 삭제하면서 삭제된 데이터도 반환한다.

삭제된 ID의 빈자리는 일반적으로 다시 당겨서 채우지 않는다.  
ID는 순번보다는 각 데이터를 구분하는 고유 식별자로 사용하는 것이 일반적이다.

---

# 8. HTTPException

요청한 데이터가 존재하지 않는 등 API 처리 중 오류가 발생했을 때 사용한다.

```python
raise HTTPException(
    status_code=404,
    detail="제품을 찾을 수 없습니다."
)
```

`404 Not Found`는 요청한 데이터를 찾을 수 없다는 의미이다.

---

# 9. model_dump()

Pydantic의 BaseModel 객체를 일반 Python 딕셔너리로 변환한다.

```python
new_item = item.model_dump()
```

변환 후에는 다음처럼 딕셔너리 데이터를 수정하거나 `items_db`에 저장할 수 있다.

```python
new_item["id"] = id_counter
```

---

# 10. 같은 경로와 HTTP Method

같은 경로라도 HTTP Method가 다르면 각각 다른 API로 사용할 수 있다.

```text
GET    /items
POST   /items
PUT    /items/{item_id}
DELETE /items/{item_id}
```

하지만 같은 Method와 같은 경로를 중복해서 만드는 것은 피해야 한다.

```text
PUT /items/{item_id}
PUT /items/{item_id}
```

처럼 중복 등록하면 먼저 등록된 라우트가 실제 요청 처리에서 우선될 수 있어 의도하지 않은 동작이 발생할 수 있다.

---

# 오늘 핵심

FastAPI에서 HTTP Method를 이용해 API를 만들고, Pydantic으로 요청 데이터의 형식을 정의했다.

DB 대신 `items_db` 딕셔너리를 사용하여 다음 CRUD 흐름을 직접 구현했다.

```text
POST   → 데이터 생성
GET    → 전체 또는 단일 데이터 조회
PUT    → 데이터 수정
DELETE → 데이터 삭제
```

또한 `HTTPException`, `model_dump()`, `global id_counter`, Path Parameter 등의 기본 사용법을 익혔다.