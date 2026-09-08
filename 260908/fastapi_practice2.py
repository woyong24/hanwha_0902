# Enum 기능을 사용하기 위해 가져오기
from enum import Enum

# FastAPI 가져오기
from fastapi import FastAPI


# model_name으로 받을 수 있는 값을 미리 정해둠
# 즉, alexnet / resnet / lenet 중 하나만 받도록 제한
class ModelName(str, Enum):
    alexnet = "alexnet"
    resnet = "resnet"
    lenet = "lenet"


# FastAPI 앱 생성
app = FastAPI()


# URL의 {model_name} 부분을 Path Parameter로 받음
# 예:
# http://127.0.0.1:8000/models/alexnet
# http://127.0.0.1:8000/models/resnet
# http://127.0.0.1:8000/models/lenet
@app.get("/models/{model_name}")
async def get_model(model_name: ModelName):

    # model_name이 alexnet이면
    if model_name is ModelName.alexnet:
        return {
            "model_name": model_name,
            "message": "Deep Learning FTW!"
        }

    # model_name의 실제 값이 "lenet"이면
    if model_name.value == "lenet":
        return {
            "model_name": model_name,
            "message": "LeCNN all the images"
        }

    # alexnet도 아니고 lenet도 아니면
    # 현재 Enum 기준으로 남는 값은 resnet
    return {
        "model_name": model_name,
        "message": "Have some residuals"
    }