from queue import Queue
from string import ascii_lowercase
import pytesseract
from PIL import Image


class Node:

    def __init__(self, number=-1):
        self.number = number
        self.links = {}
        self.fail_link = self


class FA:
    def __init__(self, pattern):
        self.pattern = pattern
        self.final_states = {}
        self.trie_root = Node()
        self.make_fa(pattern)
        self.patterns_etiquettes = {}
        # print_links(self.trie_root)

    def make_fa(self, pattern):
        state = 0
        self.trie_root.number = state
        alphabet = set()
        for line in pattern:
            ptr = self.trie_root
            for i in range(len(line)):
                alphabet.add(line[i])
                if line[i] not in ptr.links.keys():
                    state += 1
                    node = Node(state)
                    ptr.links[line[i]] = node
                ptr = ptr.links[line[i]]
        q = Queue()
        for letter in alphabet:
            node = next(self.trie_root, letter)
            if node is not None:
                node.fail_link = self.trie_root
                q.put(node)
            else:
                self.trie_root.links[letter] = self.trie_root
        while not q.empty():
            node = q.get()
            for letter in alphabet:
                node_next = next(node, letter)
                if node_next is not None:
                    q.put(node_next)
                    x = node.fail_link
                    while next(x, letter) is None:
                        x = x.fail_link
                    node_next.fail_link = next(x, letter)
        for line in pattern:
            ptr = self.trie_root
            for letter in line:
                ptr = next(ptr, letter)
            self.final_states[ptr.number] = line

    def find(self, line):
        ptr = self.trie_root
        result = {}
        for pos in range(len(line)):
            letter = line[pos]
            while next(ptr, letter) is None and ptr != self.trie_root:
                ptr = ptr.fail_link
            if next(ptr, letter) is None:
                continue
            ptr = next(ptr, letter)
            if ptr.number in self.final_states.keys():
                result[pos-len(self.final_states[ptr.number])+1] = self.patterns_etiquettes[self.final_states[ptr.number]]
        return result

    def text_processing(self, text):
        etiquette = 1
        for pattern in self.pattern:
            if pattern not in self.patterns_etiquettes.keys():
                self.patterns_etiquettes[pattern] = etiquette
                etiquette += 1
        found_in_line = []
        for line in text:
            found_in_line.append(self.find(line))
        return found_in_line

    def find_2d_patterns(self, text):
        lines_data = self.text_processing(text)
        pattern_etiq = [self.patterns_etiquettes[i] for i in self.pattern]
        n = len(self.pattern) # actual considered lines
        lines_num = len(text)
        patterns_counter = 0
        for i in range(lines_num - n + 1):
            for pos, etiquette in lines_data[i].items():
                if etiquette == pattern_etiq[0]:    # chance to find at that position
                    for j in range(1, n):
                        if pos in lines_data[i+j].keys() and lines_data[i+j][pos] == pattern_etiq[j]:
                            if j == n-1:
                                # print("FOUND 2D PATTERN FROM LINE ", i+1, " START POSITION ", pos) # line in file notation, indexing from 1
                                patterns_counter += 1
                        else:
                            break
        return patterns_counter


def next(node, letter):
    if letter in node.links.keys():
        return node.links[letter]
    return None


def print_links(root):
    print("Number ", root.number)
    for key, val in root.links.items():
        print("Link by ", key, " to ", val.number)
    print("Fail link to ", root.fail_link.number)
    for node in root.links.values():
        if node != root: print_links(node)


fa = FA(["abc", "aab", "cba"])
print(fa.find_2d_patterns(["baabcabccc", "cbaababc", "xycbaaabzabczz", "12345cba90"]))

with open("haystack.txt", "r") as file:
    text = file.readlines()
    for sign in ascii_lowercase:
        print("Letter: ", sign)
        fa = FA([sign, sign])
        print(fa.find_2d_patterns(text))

with open("haystack.txt", "r") as file:
    text = file.readlines()
    print("Pattern:\nth\nth")
    fa = FA(["th", "th"])
    print(fa.find_2d_patterns(text))
    print("Pattern:\nt h\nt h")
    fa = FA(["t h", "t h"])
    print(fa.find_2d_patterns(text))

image = Image.open()

