DEBUG = 1


def prefix_function(pattern):
    m = len(pattern)
    pi = [0] * m
    k = 0
    if DEBUG:
        print("Построение pi-функции:")
    for q in range(1, m):
        if DEBUG:
            action = []
        while k > 0 and pattern[k] != pattern[q]:
            if DEBUG:
                action.append(f"{pattern[k]}!={pattern[q]}: откат k->pi[{k-1}]={pi[k-1]}")
            k = pi[k - 1]
        if pattern[k] == pattern[q]:
            k += 1
            if DEBUG:
                action.append(f"{pattern[q]}={pattern[q]}: k++ -> {k}")
        else:
            if DEBUG and not action:
                action.append(f"{pattern[k]}!={pattern[q]} и k=0")
        pi[q] = k
        if DEBUG:
            print(f"q={q}: {'; '.join(action)}; pi[{q}]={k}")
    if DEBUG:
        print("Результат pi:", pi, "\n")
    return pi


def kmp_search(pattern, text):
    n, m = len(text), len(pattern)
    if m == 0:
        return [0] if n == 0 else [-1]

    pi = prefix_function(pattern)
    q = 0
    result = []
    if DEBUG:
        print("Поиск вхождений:")
    for i, ch in enumerate(text):
        while q > 0 and pattern[q] != ch:
            if DEBUG:
                print(f"i={i}: {pattern[q]}!={ch}, откат q->pi[{q-1}]={pi[q-1]}")
            q = pi[q - 1]
        if pattern[q] == ch:
            q += 1
            if DEBUG:
                print(f"i={i}: {ch} совпало, q-> {q}")
        if DEBUG and q == 0:
            print(f"i={i}: {pattern[q]}!={ch}, q={q}")
        if q == m:
            pos = i - m + 1
            result.append(pos)
            if DEBUG:
                print(f"Найдено вхождение с {pos}")
            q = pi[q - 1]
    return result if result else [-1]


def is_cyclic_shift(A, B):
    if len(A) != len(B):
        return -1
    if not A:
        return 0
    if DEBUG:
        print("Проверка циклического сдвига:")
    pi = prefix_function(A)
    q = 0
    n = len(A)
    for i in range(2*n):
        ch = B[i] if i < n else B[i-n]
        while q > 0 and A[q] != ch:
            if DEBUG:
                print(f"i={i}: {A[q]}!={ch}, откат q->pi[{q-1}]={pi[q-1]}")
            q = pi[q-1]
        if A[q] == ch:
            q += 1
            if DEBUG:
                print(f"i={i}: {ch} совпало, q-> {q}")
        if DEBUG and q == 0:
            print(f"i={i}: {A[q]}!={ch}, q={q}")

        if q == n:
            pos = i - n + 1
            if DEBUG:
                print(f"Найден сдвиг {pos}")
            return pos if pos < n else -1
    return -1

if __name__ == "__main__":
    key = int(input())
    A = input().strip()
    B = input().strip()
    if key == 1:
        result = kmp_search(A, B)
        print(','.join(map(str, result)))
    else:
        result = is_cyclic_shift(A, B)
        print(result)