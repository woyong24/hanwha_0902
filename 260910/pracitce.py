
num1 = 50
num2 = 100

if num2 > num1:
    print("100은 50보다 큽니다.")
elif num1 == num2:
    print("num1과 num2는 같다")

# 다중 Elif문 
score = 75

if score >= 90:
  print("Grade: A")
elif score >= 80:
  print("Grade: B")
elif score >= 70:
  print("Grade: C")
elif score >= 60:
  print("Grade: D")

day = 3
if day == 1:
  print("Monday")
elif day == 2:
  print("Tuesday")
elif day == 3:
  print("Wednesday")
elif day == 4:
  print("Thursday")
elif day == 5:
  print("Friday")
elif day == 6:
  print("Saturday")
elif day == 7:
  print("Sunday")


# Lambda식
x = lambda a, b: a if a > b else b
print(x(8,5))
# Lambda식 / 제조데이터 예시
grade = lambda yield_rate: "High" if yield_rate >= 90 else "Low"
print(grade(3.1))


# Match case
day = 4

match day:
    case 1:
        print("Monday")
    case 2:
        print("Tuesday")
    case 3:
        print("Wednesday")
    case 4:
        print("Thursday")
    case 5:
        print("Friday")
    case 6:
        print("Saturday")
    case 7:
        print("Sunday")
    case _:
        print("Invalid day")


# While문
i = 1
while i <= 5:
    print(i)
    i += 1 

# for ... in 문으로 똑같이 구현 가능 (무한루프에 빠질 일이 없음)
for i in range(1, 6):
    print(i)

# Range아니면 다 출력
composers = ["Beethoven", "Chopin", "Rachmaninoff", "Liszt", "Tchaikovsky"]
for x in composers:
    print(x)

# (시작값, 끝값, 간격)
for i in range(2, 30, 3):
    print(i)

# 중첩 for문, 약간 경우의 수 느낌 (장비 3개, 레시피 2개 연결해서 보고 싶을 때)
equipment = ["EQ1", "EQ2", "EQ3"]
recipes = ["R1", "R2"]

for eq in equipment:
    for recipe in recipes:
        print(eq, recipe)

# 여기까지하고 점심 이후로 조퇴해서 내용을 모른다..................

# Streealit-FastAPI 연결해서 뭐시기 공부 10일(목) 내용 정리하기