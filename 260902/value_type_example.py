# 변수에 타입 힌트를 지정해서 어떤 자료형을 사용할지 표시
service_name: str = "summary-api"   # 문자열(str)
max_length: int = 100               # 정수(int)
temperature: float = 0.2           # 실수(float)
is_enabled: bool = True            # 참/거짓(bool)

# type()으로 변수의 실제 자료형 확인
print(type(service_name), type(max_length))

# 결과
# <class 'str'> <class 'int'>