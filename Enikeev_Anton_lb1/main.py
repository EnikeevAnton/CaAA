from collections import deque
from typing import List, Tuple
import time

DEBUG = False

class SquareCutter:
    def __init__(self, N: int):
        """ Инициализация класса для разбиения квадрата """
        self.N = N
        self.queue = deque()  # очередь для хранения состояний
        self.occupied = 0  # Массив занятых ячеек в квадрате
        self.best_count = float('inf')  # Лучшее количество квадратов в решении
        self.best_solution = []  # Лучшее разбиение квадрата.
    
    def get_splits(self, min_divider):
        """ Возвращает разбиение кв., где сторона - составное число, max = 48 """
        if min_divider == 2:  return [
            (1, 1, N // 2),
            (N // 2 + 1, 1, N // 2),
            (N // 2 + 1, N // 2 + 1, N // 2),
            (1, N // 2 + 1, N // 2)
        ], 4

        if min_divider == 3: return [
            (1, 1, (N * 2) // 3),
            (1, (N * 2) // 3 + 1, N // 3),
            (N // 3 + 1, (N * 2) // 3 + 1, N // 3),
            ((N * 2) // 3 + 1, 1, N // 3),
            ((N * 2) // 3 + 1, N // 3 + 1, N // 3),
            ((N * 2) // 3 + 1, (N * 2) // 3 + 1, N // 3)
        ], 6
        if min_divider == 5: return [
            (1, 1, (N * 3) // 5),
            ((N * 3) // 5 + 1, (N * 2) // 5 + 1, (N * 2) // 5),
            ((N * 3) // 5 + 1, 1, (N * 2) // 5),
            (1, (N * 3) // 5 + 1, (N * 2) // 5),
            ((N * 2) // 5 + 1, (N * 3) // 5 + 1, N // 5),
            ((N * 2) // 5 + 1, (N * 4) // 5 + 1, N // 5),
            ((N * 3) // 5 + 1, (N * 4) // 5 + 1, N // 5),
            ((N * 4) // 5 + 1, (N * 4) // 5 + 1, N // 5)
        ], 8

        return [], -1

    def is_occupied(self, x: int, y: int) -> bool:
        """ Проверяет, занята ли ячейка (x, y) """
        index = x * self.N + y
        return bool(self.occupied & (1 << index))

    def try_place(self, x: int, y: int, size: int) -> bool:
        """ Пробует разместить квадрат размера size на позиции (x, y) """
        if x + size > self.N or y + size > self.N:
            return False

        for i in range(x, x + size):
            for j in range(y, y + size):
                index = i * self.N + j
                if not bool(self.occupied & (1 << index)):
                    self.occupied |= (1 << index)
                else:
                    return False
        return True
    
    def first_prime_factor(self) -> int:
        """ Находит первый простой делитель числа n """

        if self.N % 2 == 0:
            return 2
        
        for i in range(3, int(self.N**0.5) + 1, 2):
            if self.N % i == 0:
                return i
            
        return -1 # число простое 

    def find_empty(self) -> Tuple[int, int]:
        """ Ищет первую пустую ячейку и возвращает её координаты """
        for i in range(self.N - (self.N + 1) // 2, self.N):
            for j in range(self.N - (self.N + 1) // 2, self.N):
                if not self.is_occupied(i, j):
                    return i, j
        return -777, -777

    def initial_filling(self) -> None:
        """ Начальное разбиение """

        squares = []

        first_square = (self.N + 1) // 2
        second_square = self.N - first_square 

        self.try_place(0, 0, first_square)
        squares.append((1, 1, first_square))

        self.try_place(0, first_square, second_square)
        squares.append((1, first_square + 1, second_square))

        self.try_place(first_square, 0, second_square)
        squares.append((first_square + 1, 1, second_square))

        self.queue.append((self.occupied, squares, self.N * self.N - first_square ** 2 - 2 * (second_square ** 2)),)

    def solve(self) -> None:
        """ Решает задачу разбиения квадрата на минимальное количество меньших квадратов """

        min_divider = self.first_prime_factor()

        if min_divider != -1:
            self.best_solution, self.best_count = self.get_splits(min_divider)
            return 
        
        self.initial_filling()

        while self.queue:
            cur_occupied, pieces_placed, remains = self.queue.pop()

            if len(pieces_placed) + 1 >= self.best_count:
                if DEBUG:
                    print(f'remove partition {pieces_placed}, len = {len(pieces_placed)}')
                continue

            self.occupied = cur_occupied
            i, j = self.find_empty()

            max_size = min(self.N - max(i, j), self.N - (self.N + 1) // 2)

            for size in range(max_size, 0, -1):
                if size * size <= remains and self.try_place(i, j, size):
                    self.add_found_solution(pieces_placed, i, j, remains, size)

                self.occupied = cur_occupied  # Восстановление состояния

    def add_found_solution(self, pieces_placed: List[Tuple[int, int, int]], i: int, j: int, remains: int, size: int) -> bool:
        """ Добавляет новое решение """
        new_pieces = pieces_placed.copy()
        new_pieces.append((i + 1, j + 1, size))
        remains -= size * size

        if remains == 0:
            if DEBUG:
                print(f'found partition {new_pieces}, len = {len(new_pieces)}')
            self.best_count = len(new_pieces)
            self.best_solution = new_pieces
            return True
        
        if DEBUG:
            print(f'add partition {new_pieces}, len = {len(new_pieces)}')

        self.queue.appendleft((self.occupied, new_pieces, remains))
        return False

    def get_solution(self) -> Tuple[int, List[Tuple[int, int, int]]]:
        self.solve()
        return self.best_count, self.best_solution

def ask_debug_mode():
    answer = input("Использовать режим отладки? [y/n]: ").lower()
    if answer == 'n':
      return False
    else:
      return True


if __name__ == "__main__":
    N = int(input().strip())
    DEBUG = ask_debug_mode()
    start_time = time.perf_counter()
    solver = SquareCutter(N)
    count, solution = solver.get_solution()
    print(count)
    for square in solution:
        print(*square)
    end_time = time.perf_counter()
    run_time = end_time - start_time
    print(f"Функция выполнилась за {run_time:.4f} секунд")
