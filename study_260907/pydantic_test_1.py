# 예제 1번

from pydantic import BaseModel


class User(BaseModel):
    name: str
    age: int
    email: str


user = User(
    name="Alice",
    # age는 int 타입이지만 문자열 "25"를 넣어도 Pydantic이 25로 변환
    age="25",
    email="alice@example.com",
)

print(user)
print(user.age)
print(type(user.age))

