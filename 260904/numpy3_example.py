import numpy as np

# 0부터 11까지 총 12개의 값을 가진 1차원 배열 생성
vec = np.arange(12)

# 1차원 배열을 3행 4열의 2차원 배열로 변환
matrix_3x4 = vec.reshape(3, 4)
print("3x4 행렬:\n", matrix_3x4)

# 전치 행렬 생성
# 행과 열의 위치를 서로 바꿈
# 3x4 → 4x3
transposed = matrix_3x4.T
print("전치(Transpose) 결과:\n", transposed)


# 결과
# 3x4 행렬:
# [[ 0  1  2  3]
#  [ 4  5  6  7]
#  [ 8  9 10 11]]

# 전치(Transpose) 결과:
# [[ 0  4  8]
#  [ 1  5  9]
#  [ 2  6 10]
#  [ 3  7 11]]