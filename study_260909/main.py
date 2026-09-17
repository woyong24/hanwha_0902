from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# 데이터 형식 정의
# 클라이언트가 보낼 item 데이터 구조
class ItemSchema(BaseModel):
    name: str
    price: int
    desc: str | None = None


# 수정용 데이터 형식
class ItemUpdate(BaseModel):
    name: str
    price: int
    desc: str


# 임시 DB 역할
# key는 item_id, value는 item 정보
items_db: dict[int, dict] = {}

# 새 item 생성 시 사용할 ID 번호
id_counter = 1


app = FastAPI()


# 생성 Create
# 새로운 item을 받아 items_db에 저장
@app.post("/items/", status_code=201)
async def create_item(item: ItemSchema):
    global id_counter

    # Pydantic 객체를 dict로 변환
    new_item = item.model_dump()

    # 새 item에 ID 추가
    new_item["id"] = id_counter

    # items_db에 저장
    items_db[id_counter] = new_item

    # 다음 item을 위해 ID 증가
    id_counter += 1

    return items_db


# 조회(전체) Read
# 저장된 모든 item 조회
# http://127.0.0.1:8000/items
@app.get("/items")
async def get_all_items():
    return {
        "msg": "전체 목록 조회 완료",
        "data": list(items_db.values())
    }


# 조회(단일) Read
# item_id를 이용해 하나의 item만 조회
# http://127.0.0.1:8000/items/1
@app.get("/items/{item_id}")
async def get_item(item_id: int):

    # 존재하지 않는 ID면 404 에러
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    return {
        "msg": "단일 조회 완료",
        "data": items_db[item_id]
    }


# 수정 Update
# 특정 item_id의 데이터를 새로운 값으로 변경
@app.put("/items/{item_id}")
async def update_item(item_id: int, item: ItemSchema):

    # 존재하지 않는 ID면 404 에러
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    # 받은 데이터를 dict로 변환
    updated_data = item.model_dump()

    # 기존 item_id 유지
    updated_data["id"] = item_id

    # 기존 데이터를 새 데이터로 교체
    items_db[item_id] = updated_data

    return {
        "msg": "수정 완료",
        "data": updated_data
    }


# 삭제 Delete
# 특정 item_id의 데이터를 삭제
@app.delete("/items/{item_id}")
async def delete_item(item_id: int):

    # 존재하지 않는 ID면 404 에러
    if item_id not in items_db:
        raise HTTPException(
            status_code=404,
            detail="제품을 찾을 수 없습니다."
        )

    # 해당 item 삭제 후 삭제된 데이터를 저장
    deleted_item = items_db.pop(item_id)

    return {
        "msg": "삭제 완료",
        "data": deleted_item
    }