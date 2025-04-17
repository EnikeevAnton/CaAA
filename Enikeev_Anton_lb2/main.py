from collections import deque

class AhoCorasick:
    def __init__(self):
        self.trie = [{}]
        self.output = [set()]  # Хранит кортежи (pattern_index, length)
        self.fail = [0]
        self.dict_suffix = [0]

    def add_pattern(self, pattern, pattern_index):
        """Добавляет точный шаблон (без джокеров)."""
        node = 0
        for char in pattern:
            if char not in self.trie[node]:
                self.trie.append({})
                self.output.append(set())
                self.fail.append(0)
                self.dict_suffix.append(0)
                self.trie[node][char] = len(self.trie) - 1
            node = self.trie[node][char]
        self.output[node].add((pattern_index, len(pattern)))

    def build(self):
        queue = deque()
        for char, node in self.trie[0].items():
            queue.append(node)
            self.fail[node] = 0
            self.dict_suffix[node] = 0

        while queue:
            current = queue.popleft()
            for char, child in self.trie[current].items():
                queue.append(child)
                f = self.fail[current]
                while f and char not in self.trie[f]:
                    f = self.fail[f]
                self.fail[child] = self.trie[f].get(char, 0)
                if self.output[self.fail[child]]:
                    self.dict_suffix[child] = self.fail[child]
                else:
                    self.dict_suffix[child] = self.dict_suffix[self.fail[child]]

    def get_next_node(self, node, char):
        if char in self.trie[node]:
            return self.trie[node][char]
        original_node = node
        while node != 0 and char not in self.trie[node]:
            node = self.fail[node]
        next_node = self.trie[node].get(char, 0)
        self.trie[original_node][char] = next_node
        return next_node

    def search_all(self, text):
        """Возвращает список (start_position, pattern_index) для точных шаблонов."""
        node = 0
        occurrences = []
        for i, char in enumerate(text):
            node = self.get_next_node(node, char)
            temp = node
            while temp:
                if self.output[temp]:
                    for (pattern_index, pattern_length) in self.output[temp]:
                        start_position = i - pattern_length + 2  # 1-based
                        occurrences.append((start_position, pattern_index))
                temp = self.dict_suffix[temp]
        return occurrences
    
    def get_fail_chain(self, node):
        """Возвращает цепочку суффиксных ссылок (fail) для узла."""
        chain = []
        current = node
        while current != 0:
            current = self.fail[current]
            chain.append(current)
        return chain

    def get_dict_suffix_chain(self, node):
        """Возвращает цепочку сжатых ссылок (dict_suffix) для узла."""
        chain = []
        current = node
        while current != 0:
            next_node = self.dict_suffix[current]
            chain.append(next_node)
            current = next_node
        return chain
    
    def max_fail_chain(self):
        """Находит самую длинную цепочку суффиксных ссылок и её длину."""
        max_length = 0
        max_chain = []
        for node in range(1, len(self.trie)):
            chain = self.get_fail_chain(node)
            if len(chain) > max_length:
                max_length = len(chain)
                max_chain = [node] + chain
        return max_length, max_chain
    
    def max_dict_suffix_chain(self):
        """Находит самую длинную цепочку сжатых ссылок и её длину."""
        max_length = 0
        max_chain = []
        for node in range(len(self.trie)):
            chain = self.get_dict_suffix_chain(node)
            if len(chain) > max_length:
                max_length = len(chain)
                max_chain = [node] + chain
        return max_length, max_chain

def print_trie(ac, node=0, prefix=""):
    if ac.output[node]:
        output_str = ", ".join(f"(№{p}, длина={l})" for p, l in ac.output[node])
    else:
        output_str = ""
    print(f"{prefix}Узел {node}: {output_str}")
    for char, child in ac.trie[node].items():
        print(f"{prefix}  '{char}' -> Узел {child}")
        print_trie(ac, child, prefix + "    ")

def print_automaton(ac):
    print("\nАвтомат Ахо–Корасик:")
    total = len(ac.trie)
    for i in range(total):
        print(f"Узел {i}:")
        if ac.trie[i]:
            print("  Потомки:")
            for char, child in ac.trie[i].items():
                print(f"    '{char}' -> Узел {child}")
        else:
            print("  Потомки: {}")
            
        print(f"  Суффиксная ссылка: Узел {ac.fail[i]}")
        print(f"  Хорошая (сжатая) ссылка: Узел {ac.dict_suffix[i]}")
        
        if ac.output[i]:
            outs = ", ".join(f"(№{p}, длина={l})" for p, l in ac.output[i])
            print(f"  Вывод: {{{outs}}}")
        else:
            print("  Вывод: {}")
            
        print("-" * 40)
    
    print()

def find_wildcard_matches(text, pattern, wild_char):
    """Находит вхождения шаблона с джокерами, используя AhoCorasick."""
    sub_patterns = []
    n = len(pattern)
    i = 0
    while i < n:
        if pattern[i] != wild_char:
            start = i
            while i < n and pattern[i] != wild_char:
                i += 1
            sub = pattern[start:i]
            sub_patterns.append((sub, start)) 
        else:
            i += 1

    if not sub_patterns:
        pattern_len = len(pattern)
        return [i + 1 for i in range(len(text) - pattern_len + 1)] if pattern_len <= len(text) else []

    ac = AhoCorasick()
    for idx, (sub, offset) in enumerate(sub_patterns):
        ac.add_pattern(sub, idx)
    ac.build()

    len_text = len(text)
    len_pattern = len(pattern)
    C = [0] * (len_text - len_pattern + 1) if len_text >= len_pattern else []
    matches = ac.search_all(text)

    for (start_pos, pattern_idx) in matches:
        sub, offset = sub_patterns[pattern_idx]
        pattern_start = start_pos - 1 - offset 
        if 0 <= pattern_start < len(C):
            C[pattern_start] += 1

    valid_starts = []
    required = len(sub_patterns)
    for i in range(len(C)):
        if C[i] == required:
            valid = True
            for j in range(len_pattern):
                if pattern[j] != wild_char and (i + j >= len_text or text[i + j] != pattern[j]):
                    valid = False
                    break
            if valid and (i + len_pattern <= len_text):
                valid_starts.append(i + 1)

    return sorted(valid_starts)


def classic_aho():
    text = input()
    n = int(input())
    patterns = []
    for i in range(n):
        patterns.append(input())

    ac = AhoCorasick()
    for i, pattern in enumerate(patterns, start=1):
        ac.add_pattern(pattern, i)
   
    print("\nБор:")
    print_trie(ac)
    ac.build()
    print(f"Бор в виде словаря: {ac.trie}")

    print_automaton(ac)
    fail_length, fail_chain = ac.max_fail_chain()
    dict_suffix_length, dict_suffix_chain = ac.max_dict_suffix_chain()

    print(f"Самая длинная цепочка суффексных ссылок: {fail_chain} (длина = {fail_length})")
    print(f"Самая длинная цепочка сжатых ссылок: {dict_suffix_chain} (длина = {dict_suffix_length})")

    occurrences = ac.search_all(text)
    occurrences.sort(key=lambda x: (x[0], x[1]))
    
    out_lines = [f"{pos} {p}" for pos, p in occurrences]
    print("\n".join(out_lines))

def searc_with_joker():
    text = input().strip()
    pattern = input().strip()
    wild_char = input().strip()

    matches = find_wildcard_matches(text, pattern, wild_char)


    for pos in matches:
        print(pos)


if __name__ == "__main__":
    n = int(input())

    if n == 1:
        classic_aho()
    else:
        searc_with_joker()