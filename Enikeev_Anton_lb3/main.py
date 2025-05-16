INF = float('inf')
DEBUG = True

def read_input():
    replace_cost, insert_cost, delete_cost, replace_two_cost = map(int, input().split())
    A = input().strip()
    B = input().strip()
    return replace_cost, insert_cost, delete_cost, replace_two_cost, A, B

def initialize_dp(n, m, delete_cost, insert_cost):
    D = [[INF] * (m + 1) for _ in range(n + 1)]
    D[0][0] = 0
    for i in range(1, n + 1):
        D[i][0] = D[i-1][0] + delete_cost
    for j in range(1, m + 1):
        D[0][j] = D[0][j-1] + insert_cost
    return D

def fill_dp(D, A, B, replace_cost, insert_cost, delete_cost, replace_two_cost):
    n = len(A)
    m = len(B)
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            delete = D[i-1][j] + delete_cost
            insert = D[i][j-1] + insert_cost
            match_replace = D[i-1][j-1] + (0 if A[i-1] == B[j-1] else replace_cost)
            replace_two = INF
            if j >= 2:
                replace_two = D[i-1][j-2] + replace_two_cost
            D[i][j] = min(delete, insert, match_replace, replace_two)

def backtrack_operations(D, A, B, replace_cost, insert_cost, delete_cost, replace_two_cost):
    operations = []
    i = len(A)
    j = len(B)
    
    if DEBUG:
        print("\nПошаговое восстановление операций:")
        print("(Ищем путь от правого нижнего угла к началу матрицы)")
    while i > 0 or j > 0:
        if DEBUG:
            print(f"\nПозиция: A[{i}]='{A[i-1] if i>0 else ' '}', B[{j}]='{B[j-1] if j>0 else ' '}'")
            print(f"Текущая стоимость: {D[i][j]}")

        if i > 0 and j >= 2 and D[i][j] == D[i-1][j-2] + replace_two_cost:
            if DEBUG: print(f"RT: замена '{A[i-1]}' на '{B[j-2:j]}' (-2 символа B)")
            operations.append('[RT]')
            i -= 1
            j -= 2
        elif j > 0 and D[i][j] == D[i][j-1] + insert_cost:
            if DEBUG: print(f"I: вставка '{B[j-1]}'")
            operations.append('I')
            j -= 1
        elif i > 0 and D[i][j] == D[i-1][j] + delete_cost:
            if DEBUG: print(f"D: удаление '{A[i-1]}'")
            operations.append('D')
            i -= 1
        else:
            if i > 0 and j > 0 and A[i-1] == B[j-1]:
                if DEBUG: print(f"M: совпадение '{A[i-1]}'")
                operations.append('M')
            else:
                if DEBUG: print(f"R: замена '{A[i-1]}' на '{B[j-1]}'")
                operations.append('R')
            i -= 1
            j -= 1
            
        if DEBUG: print(f"Текущие операции: {list(reversed(operations))}")
    if DEBUG: print()
    operations.reverse()
    return operations

def print_dp_matrix(D, A, B):
    if not DEBUG:
        return
    
    n = len(A)
    m = len(B)
    col_width = 4
    
    header = " " * 8 + "".join([f"{char:^{col_width}}" for char in B])
    print(header)
    
    for i in range(n + 1):
        row_label = ' ' if i == 0 else A[i-1]
        row = []
        for j in range(m + 1):
            val = D[i][j]
            row.append(" ∞ " if val == INF else f"{val:3d}")
        
        row_str = " ".join([f"{item:^{col_width-1}}" for item in row])
        print(f"{row_label:2} {row_str}")

def print_result(operations, A, B):
    print(''.join(operations))
    print(A)
    print(B)

def main():
    replace_cost, insert_cost, delete_cost, replace_two_cost, A, B = read_input()
    n = len(A)
    m = len(B)
    D = initialize_dp(n, m, delete_cost, insert_cost)
    fill_dp(D, A, B, replace_cost, insert_cost, delete_cost, replace_two_cost)
    
    if DEBUG: print("\nМатрица минимальных стоимостей:")
    print_dp_matrix(D, A, B)
    
    operations = backtrack_operations(D, A, B, replace_cost, insert_cost, delete_cost, replace_two_cost)
    print_result(operations, A, B)

if __name__ == '__main__':
    main()