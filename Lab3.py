import string
from queue import PriorityQueue
import os
from time import time
import random


def find_node_to_swap(node, all_nodes):
    queue = PriorityQueue()
    act_node_to_swap = None
    for elem in all_nodes:
        queue.put(elem)
    while not queue.empty():
        test = queue.get()
        if node == test:
            break
    while not queue.empty():
        to_swap = queue.get()
        if to_swap.weight < node.weight and to_swap.level < node.level:
            if to_swap == node.parent or to_swap.parent == node:      # nie mozna zmienic z parentem
                continue
            if to_swap.parent is None:  # nie mozna zmienic z rootem
                continue
            act_node_to_swap = to_swap
    return act_node_to_swap


def swap(node1, node2):
    # print("ZMIANA ",node1.letter,node1.level,node1.weight, "z",node2.letter,node2.level,node2.weight)
    if node1.parent == node2.parent:
        parent = node1.parent
        parent.left, parent.right = parent.right, parent.left
        parent.left.code_elem = "0"
        parent.right.code_elem = "1"
    parent_1 = node1.parent
    parent_2 = node2.parent
    if parent_1.left == node1:
        parent_1.left = node2
        node2.code_elem = "0"
    else:
        parent_1.right = node2
        node2.code_elem = "1"
    node2.parent = parent_1
    if parent_2.left == node2:
        parent_2.left = node1
        node1.code_elem = "0"
    else:
        parent_2.right = node1
        node1.code_elem = "1"
    node1.parent = parent_2
    node1.level, node2.level = node2.level, node1.level


class Node:

    def __init__(self, letter=None, parent=None, left=None, right=None, weight=None, code_elem=None):
        self.letter = letter
        self.parent = parent
        self.left = left
        self.right = right
        self.weight = weight
        self.code_elem = code_elem
        self.type = "external"
        self.level = None

    def __lt__(self, other):
        if self.type < other.type:
            return True
        elif self.type == other.type:
            if self.level == other.level:
                return self.weight < other.weight
            else:
                return self.level > other.level
        else:
            return False

    def code(self):
        code = ""
        ptr = self
        while ptr.parent is not None:
            code = ptr.code_elem + code
            ptr = ptr.parent
        return code

    def add_child(self, code_elem, node):
        if code_elem == "0":
            self.left = node
        else:
            self.right = node
        node.code_elem = code_elem

    def increment(self, root, all_nodes):
        ptr = self
        while ptr is not None:
            if ptr != root:
                swap_node = find_node_to_swap(ptr, all_nodes)
                if swap_node is not None:
                    swap(ptr, swap_node)
            ptr.weight += 1
            ptr = ptr.parent


class HuffmanTree:

    def __init__(self, root):
        self.root = root

    def print_tree(self, ptr):
        if ptr.left is None and ptr.right is None:
            code = ""
            ptr_up = ptr
            while ptr_up.parent is not None:
                code = ptr_up.code_elem + code
                ptr_up = ptr_up.parent
            print(code, "", ptr.letter)
        else:
            self.print_tree(ptr.left)
            self.print_tree(ptr.right)

    def get_all_codes(self, root, d):
        ptr = root
        if ptr.left is None and ptr.right is None:
            code = ""
            ptr_up = ptr
            while ptr_up.parent is not None:
                code = ptr_up.code_elem + code
                ptr_up = ptr_up.parent
            d[ptr.letter] = code
        else:
            self.get_all_codes(ptr.left, d)
            self.get_all_codes(ptr.right, d)

    def get_all_letters(self, root, d):
        ptr = root
        if ptr.left is None and ptr.right is None:
            code = ""
            ptr_up = ptr
            while ptr_up.parent is not None:
                code = ptr_up.code_elem + code
                ptr_up = ptr_up.parent
            d[code] = ptr.letter
        else:
            self.get_all_letters(ptr.left, d)
            self.get_all_letters(ptr.right, d)


def count_letters(text):
    counter = {}
    for letter in text:
        if letter in counter:
            counter[letter] += 1
        else:
            counter[letter] = 0
    return counter


def get_min(arr1, arr2):
    if len(arr2) == 0:
        mini = arr1[0]
        arr1.pop(0)
    elif len(arr1) == 0:
        mini = arr2[0]
        arr2.pop(0)
    elif arr1[0].weight < arr2[0].weight:
        mini = arr1[0]
        arr1.pop(0)
    else:
        mini = arr2[0]
        arr2.pop(0)
    return mini


def static_huffman(letter_counts):
    nodes = []
    for a, weight in letter_counts.items():
        nodes.append(Node(letter=a, weight=weight))
    internal_nodes = []
    leafs = sorted(nodes, key=lambda n: n.weight)
    while len(leafs) + len(internal_nodes) > 1:
        element_1, element_2 = get_min(leafs, internal_nodes), get_min(leafs, internal_nodes)
        internal_nodes.append(Node(left=element_1, right=element_2, weight=element_1.weight + element_2.weight))
        element_1.parent = internal_nodes[-1]
        element_2.parent = internal_nodes[-1]
        element_1.code_elem = "0"
        element_2.code_elem = "1"
    return internal_nodes[0]


def static_encode(text, tree):
    coded_text = ""
    codes = {}
    tree.get_all_codes(tree.root, codes)
    for letter in text:
        coded_text += codes[letter]
    return codes, coded_text


def static_decode(coded_text, tree):
    text = ""
    letters = {}
    tree.get_all_letters(tree.root, letters)
    act_text = ""
    for bit in coded_text:
        act_text += bit
        if act_text in letters:
            text += letters[act_text]
            act_text = ""
    return text


# ----------------------------------------------------------------
# adaptive huffmann

def bits_2_string(b):
    return ''.join([chr(int(b, 2))])


def adaptive_huffman_encode(text):
    all_nodes = []
    nodes = {"#": Node(letter="#", weight=0)}
    root = nodes["#"]
    root.level = 0
    all_nodes.append(root)
    result = ""
    for letter in list(text):
        if letter in nodes:
            node = nodes[letter]
            # print(node.code() + ' ' + node.letter)
            result += node.code()
            node.increment(root, all_nodes)
        else:
            updated_node = nodes["#"]
            # print(updated_node.code() + ' ' + updated_node.letter)
            # print("{0:b}".format(ord(letter)) + ' ' + letter)
            result += updated_node.code()
            result += "{0:b}".format(ord(letter))
            node = Node(letter=letter, parent=updated_node, weight=1)
            nodes[letter] = node
            zero_node = Node(letter="#", parent=updated_node, weight=0)
            updated_node.add_child("0", zero_node)
            updated_node.add_child("1", node)
            updated_node.type = "internal"
            zero_node.type = "external"
            node.type = "external"
            zero_node.level = updated_node.level + 1
            node.level = updated_node.level + 1
            all_nodes.append(zero_node)
            all_nodes.append(node)
            nodes["#"] = zero_node
            updated_node.increment(root, all_nodes)
    return result


def adaptive_huffman_decode(code):
    all_nodes = []
    nodes = {"#": Node(letter="#", weight=0)}
    root = nodes["#"]
    root.level = 0
    all_nodes.append(root)
    result = ""
    bin_code = code[0:7]
    sign = bits_2_string(bin_code)
    result += sign
    updated_node = nodes["#"]
    node = Node(letter=sign, parent=updated_node, weight=1)
    nodes[sign] = node
    zero_node = Node(letter="#", parent=updated_node, weight=0)
    updated_node.add_child("0", zero_node)
    updated_node.add_child("1", node)
    updated_node.type = "internal"
    zero_node.type = "external"
    node.type = "external"
    zero_node.level = updated_node.level + 1
    node.level = updated_node.level + 1
    all_nodes.append(zero_node)
    all_nodes.append(node)
    nodes["#"] = zero_node
    updated_node.increment(root, all_nodes)
    i = 7
    ptr = root
    while i < len(code):
        left_elem = ptr.left.code_elem
        if left_elem == code[i]:
            ptr = ptr.left
        else:
            ptr = ptr.right
        if ptr.type == "external":
            if ptr.letter == "#":
                bin_code = code[i+1:i+8]
                sign = bits_2_string(bin_code)
                result += sign
                updated_node = nodes["#"]
                node = Node(letter=sign, parent=updated_node, weight=1)
                nodes[sign] = node
                zero_node = Node(letter="#", parent=updated_node, weight=0)
                updated_node.add_child("0", zero_node)
                updated_node.add_child("1", node)
                updated_node.type = "internal"
                zero_node.type = "external"
                node.type = "external"
                zero_node.level = updated_node.level + 1
                node.level = updated_node.level + 1
                all_nodes.append(zero_node)
                all_nodes.append(node)
                nodes["#"] = zero_node
                updated_node.increment(root, all_nodes)
                i += 7
                ptr = root
            else:
                sign = ptr.letter
                result += sign
                node = nodes[sign]
                node.increment(root, all_nodes)
                ptr = root
        i += 1
    return result


def generate_rand_uniform_letters(filename):        # zakladam poprawnosc nazwy pliku
    size = 1024
    if filename == "texts/rand_uniform_10kB.txt":
        size *= 10
    elif filename == "texts/rand_uniform_100kB.txt":
        size *= 100
    elif filename == "texts/rand_uniform_1MB.txt":
        size *= 1024
    file = open(filename, "w")
    for i in range(size):
        letter = random.choice(string.ascii_letters)
        file.write(letter)
    file.close()


def str_to_bytes(text):
    b = bytearray()
    for i in range(0, len(text), 8):
        b.append(int(text[i:i+8], 2))
    return bytes(b)


def test(filename):
    source = open(filename, "r")
    text = source.read()
    source.close()
    input_file_size = os.path.getsize(filename)

    print("Static Huffman encoding")
    start_time = time()
    root = static_huffman(count_letters(text))
    tree = HuffmanTree(root)
    something, coded_text = static_encode(text, tree)
    end_time = time()
    print("It took: ", end_time - start_time, "[s]")

    with open("static_coded_text.bin", "wb") as f:
        f.write(str_to_bytes(coded_text))
    code = coded_text

    print("Static Huffman decoding")
    start_time = time()
    decoded_text = static_decode(code, tree)
    end_time = time()
    print("It took: ", end_time - start_time, "[s]")

    print()
    if text == decoded_text:
        print("Static decode test passed")
    else:
        print("Static decode test failed")
        exit(1)
    print()

    print("Adaptive Huffman encoding")
    start_time = time()
    coded_text = adaptive_huffman_encode(text)
    end_time = time()
    print("It took: ", end_time - start_time, "[s]")

    with open("adaptive_coded_text.bin", "wb") as f:
        f.write(str_to_bytes(coded_text))
    code = coded_text

    print("Adaptive Huffman decoding")
    start_time = time()
    decoded_text = adaptive_huffman_decode(code)
    end_time = time()
    print("It took: ", end_time - start_time, "[s]")

    print()
    static_coded_file_size = os.path.getsize("static_coded_text.bin")
    adaptive_coded_file_size = os.path.getsize("adaptive_coded_text.bin")
    print("Static Huffman code compress ratio ", 1 - (static_coded_file_size / input_file_size))
    print("Adaptive Huffman code compress ratio ", 1 - (adaptive_coded_file_size / input_file_size))

    print()
    if text == decoded_text:
        print("Adaptive decode test passed")
    else:
        print("Adaptive decode test failed")
        exit(1)


test("texts/guttenberg_1kB.txt")
