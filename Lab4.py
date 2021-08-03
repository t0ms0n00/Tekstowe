from queue import LifoQueue
from spacy.tokenizer import Tokenizer
from random import random
from spacy.lang.pl import Polish
import codecs


def in_borders(x, y):
    if x >= 0 and y >= 0:
        return True
    return False


def delta(text_1, text_2, i, j):
    if text_1[i-1] == text_2[j-1]:
        return 0
    return 1


def delta_2(text_1, text_2, i, j):
    if text_1[i-1] == text_2[j-1]:
        return 0
    return 2


def edit_distance(text_1, text_2, cost_func):
    m = len(text_1)
    n = len(text_2)
    matrix = []
    for i in range(m+1):
        matrix.append([-1]*(n+1))
        matrix[i][0] = i
    for i in range(n+1):
        matrix[0][i] = i
    for i in range(1, m+1):
        for j in range(1, n+1):
            cost = cost_func(text_1, text_2, i, j)
            matrix[i][j] = min(matrix[i-1][j] + 1, matrix[i][j-1] + 1, matrix[i-1][j-1] + cost)
    queue = LifoQueue()
    x_pos = m
    y_pos = n
    act_string = text_2
    queue.put(act_string)
    queue.put("-----------------")
    while not(x_pos == 0 and y_pos == 0):
        if in_borders(x_pos - 1, y_pos) and matrix[x_pos][y_pos] - 1 == matrix[x_pos - 1][y_pos]:
            str_format = act_string[:y_pos] + "_" + act_string[y_pos:]
            act_string = act_string[:y_pos] + text_1[x_pos - 1] + act_string[y_pos:]
            queue.put(str_format)
            x_pos -= 1
        elif in_borders(x_pos, y_pos - 1) and matrix[x_pos][y_pos] - 1 == matrix[x_pos][y_pos - 1]:
            str_format = act_string[:y_pos - 1] + "[" + act_string[y_pos-1] + "]" + act_string[y_pos:]
            act_string = act_string[:y_pos - 1] + act_string[y_pos:]
            queue.put(str_format)
            y_pos -= 1
        else:
            if matrix[x_pos][y_pos] != matrix[x_pos - 1][y_pos - 1]:
                str_format = act_string[:y_pos - 1] + "[" + text_1[x_pos-1] + "->" + act_string[y_pos-1] + "]" + act_string[y_pos:]
                act_string = act_string[:y_pos - 1] + text_1[x_pos - 1] + act_string[y_pos:]
                queue.put(str_format)
            x_pos -= 1
            y_pos -= 1
    queue.put("-----------------")
    queue.put(text_1)
    while not queue.empty():
        s = queue.get()
        print(s)
    return matrix[m][n]


def edit_distance_tokens(text_1, text_2, cost_func):
    m = len(text_1)
    n = len(text_2)
    matrix = []
    for i in range(m + 1):
        matrix.append([-1] * (n + 1))
        matrix[i][0] = i
    for i in range(n + 1):
        matrix[0][i] = i
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            cost = cost_func(text_1, text_2, i, j)
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    return matrix[m][n]


def lcs(text_1, text_2):
    return (len(text_1) + len(text_2) - edit_distance_tokens(text_1, text_2, delta_2))/2


def lcs_test(text1, text2):
    m = len(text1)
    n = len(text2)
    matrix = []
    for i in range(m + 1):
        matrix.append([-1] * (n + 1))
        matrix[i][0] = 0
    for i in range(n + 1):
        matrix[0][i] = 0
    for i in range(1, m + 1):
        for j in range(1, n + 1):
            if text1[i - 1] == text2[j - 1]:
                matrix[i][j] = matrix[i-1][j-1] + 1
            else:
                matrix[i][j] = max(matrix[i][j - 1], matrix[i-1][j])
    return matrix


def read_LCS(matrix, text1, text2, i, j):
    if i == 0 or j == 0:
        return ""
    if text1[i - 1] == text2[j - 1]:
        return read_LCS(matrix, text1, text2, i - 1, j - 1) + text1[i - 1]
    if matrix[i][j - 1] > matrix[i - 1][j]:
        return read_LCS(matrix, text1, text2, i, j - 1)
    return read_LCS(matrix, text1, text2, i - 1, j)


def remove_tokens(tokens, filename):
    writer = open(filename, 'w')
    new_text = []
    for token in tokens:
        if random() >= 0.03:
            new_text.append(token)
            writer.write(token.text_with_ws)
        else:
            if '\n' in token.text:
                writer.write(token.text_with_ws)
    writer.close()
    return new_text


def diff(filename_1, filename_2):
    file_1 = open(filename_1, 'r')
    file_2 = open(filename_2, 'r')
    line = 0
    while True:
        line += 1
        line_1 = file_1.readline()
        line_2 = file_2.readline()
        if len(line_1) == 0 or len(line_2) == 0:
            break
        nlp = Polish()
        tokenizer = Tokenizer(nlp.vocab)
        tokens_1 = tokenizer(line_1)
        tokens_2 = tokenizer(line_2)
        text_1 = []
        text_2 = []
        for token in tokens_1:
            text_1.append(str(token))
        for token in tokens_2:
            text_2.append(str(token))
        if lcs(text_1, text_2) != len(tokens_1):
            print("[", line, "] < ", line_1)
            print("[", line, "] > ", line_2)
    file_1.close()
    file_2.close()


print(edit_distance("los", "kloc", delta))
print(edit_distance("Łódź", "Lodz", delta))
print(edit_distance("kwintesencja", "quintessence", delta))
print(edit_distance("ATGAATCTTACCGCCTCG", "ATGAGGCTCTGGCCCCTG", delta))

# t1 = "abbceadba"
# t2 = "berpabdecdaba"

# print("Longest common subsequence", lcs(t1, t2))
# print("LCS to compare", lcs_test(t1, t2)[len(t1)][len(t2)])
# print("Subsequence: ", read_LCS(lcs_test(t1, t2), t1, t2, len(t1), len(t2)))

with codecs.open("romeo-i-julia-700.txt", 'r', 'utf-8') as file:
    text = file.read()
    nlp = Polish()
    tokenizer = Tokenizer(nlp.vocab)
    tokens = tokenizer(text)
    text_1 = remove_tokens(tokens, "RiJ_1.txt")
    text_2 = remove_tokens(tokens, "RiJ_2.txt")
    print("Input tokens: ", len(tokens))
    print("Text 1 tokens:", len(text_1))
    print("Text 2 tokens:", len(text_2))
    print("Longest common toknes subsequence: ", lcs(text_1, text_2))
    print("Test LCS: ", lcs_test(text_1, text_2)[len(text_1)][len(text_2)])

diff("RiJ_1.txt", "RiJ_2.txt")
