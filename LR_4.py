import numpy as np
from multiprocessing import Process, Pipe

def deter(ppipe, matrix):
    det = round(np.linalg.det(matrix))  
    ppipe.send(det)
    ppipe.close()

def determinant(matrix):
    if matrix.shape[0] != matrix.shape[1]:
        raise ValueError("Матрица должна быть квадратной")

    n = matrix.shape[0]
    if n == 1:
        return int(matrix[0, 0])  
    elif n == 2:
        return int(matrix[0, 0] * matrix[1, 1] - matrix[0, 1] * matrix[1, 0])  
    else:
        processes = []
        ppipes = []
        result = 0
        for i in range(n):
            minor = np.delete(np.delete(matrix, 0, axis=0), i, axis=1)
            parent_conn, child_conn = Pipe()
            p = Process(target=deter, args=(child_conn, minor))
            processes.append(p)
            ppipes.append(parent_conn)
            p.start()
        for i in range(n):
            det = ppipes[i].recv() 
            sign = (-1) ** i
            result += sign * matrix[0, i] * det
            processes[i].join()
        return result  


if __name__ == '__main__':
    matrix = np.array([[1, 0, 2], [-1, 3, 4], [-2, 1, 5]])
    det_result = determinant(matrix)
    print(f"Определитель квадратной матрицы {det_result}")
