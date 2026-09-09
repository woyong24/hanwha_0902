from fastapi import FastAPI, HTTPException
from pydantic import BaseModel


# 데이터용
class ItemSchema(BaseModel):
    name: str
    price: int
    desc: str | None = None

# ItemUpdate
class ItemUpdate(BaseModel):
    name: str
    price: int
    desc: str

items_db: dict[int, dict] = {}
id_counter = 1

app = FastAPI()

# 생성 Create
@app.post("/items/", status_code=201)
async def create_item(item: ItemSchema):
    global id_counter
    new_item = item.model_dump()
    new_item["id"] = id_counter

    items_db[id_counter] = new_item
    id_counter += 1

    return items_db

# 조회(전체) Read
# http://127.0.0.1:8000/items
@app.get("/items")
async def get_all_items():
    return {"msg": "전체 목록 조회 완료", "data": list(items_db.values())}


# 조회(단일) Read
# http://127.0.0.1:8000/items/1
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

# 수정 Update
@app.put("/items/{item_id}")
async def update_item(item_id:int, item:ItemSchema):
    if item_id not in items_db:
        raise HTTPException(status_code=404, detail="제품을 찾을 수 없습니다.")

    updated_data = item.model_dump()
    updated_data["id"] = item_id
    items_db[item_id] = updated_data

    return {"msg": "수정 완료", "data": updated_data}


# 삭제 Delete
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