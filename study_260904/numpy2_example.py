import numpy as np

# 0부터 8까지 숫자를 만든 뒤 3x3 형태로 변경
matrix = np.arange(9).reshape(3, 3)

# 1행 이후, 1열 이후의 값만 추출
# [행 범위, 열 범위] 형태로 사용
print("부분 행렬:\n", matrix[1:, 1:])

# 각 요소가 5보다 큰지 True / False로 확인
mask = matrix > 5
print("조건 마스크:\n", mask)

# True인 위치의 값만 추출
print("5보다 큰 값들:", matrix[mask])


# 결과
# 부분 행렬:
# [[4 5]
#  [7 8]]

# 조건 마스크:
# [[False False False]
#  [False False False]
#  [ True  True  True]]

# 5보다 큰 값들: [6 7 8]