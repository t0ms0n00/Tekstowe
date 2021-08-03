from time import time


class Node:

    def __init__(self, value):
        self.value = value
        self.kids = []
        self.parent = None
        self.depth = 0

    def kids_values(self):
        values = []
        for node in self.kids:
            values.append(node.value)
        return values


class Trie:

    def __init__(self, root):
        self.root = root

    def find(self, text):
        pointer = self.root
        depth = 0
        while text[depth] in pointer.kids_values():
            values = pointer.kids_values()
            index = values.index(text[depth])
            pointer = pointer.kids[index]
            depth += 1
        return pointer, depth

    def print_trie(self, root):
        print("-" * root.depth, root.value)
        for kid in root.kids:
            self.print_trie(kid)

    def all_suffixes_are(self,text):
        for i in range(len(text)):
            suffix = text[i:]
            pointer = self.root
            depth = 0
            while depth < len(suffix) and suffix[depth] in pointer.kids_values():
                values = pointer.kids_values()
                index = values.index(suffix[depth])
                pointer = pointer.kids[index]
                depth += 1
            if depth != len(suffix): return False
        return True


def compute_initial_trie(text):
    root = Node("")
    trie = Trie(root)
    for letter in list(text):
        node = Node(letter)
        pointer = trie.root
        while not len(pointer.kids) == 0:
            pointer = pointer.kids[0]
        pointer.kids.append(node)
        node.depth = pointer.depth + 1
        node.parent = pointer
    return trie


def graft(head, suffix_end):
    pointer = head
    for letter in list(suffix_end):
        node = Node(letter)
        pointer.kids.append(node)
        node.parent = pointer
        node.depth = pointer.depth + 1
        values = pointer.kids_values()
        index = values.index(letter)
        pointer = pointer.kids[index]


def build_tree_schema(text):
    trie = compute_initial_trie(text)
    for i in range(1, len(text)):
        suffix = text[i:]
        head, depth = trie.find(suffix)
        suffix_end = suffix[depth:]
        graft(head, suffix_end)
    return trie


def slow_find(node, text):
    if len(text) == 0 or not node.elem_in_kids(text[0]):
        return node
    kid = node.get_kid(text[0])
    for i in range(len(kid.text)):
        if text[i] != kid.text[i]:
            return break_path(node, kid, i, text[:i])
    return slow_find(kid, text[len(kid.text):])


def break_path(node, kid, i, text):
    node.del_old_kid(kid)
    kid.text = kid.text[i:]
    new_node = SuffixTreeNode(text, kid.left, kid.left + i - 1, node.depth + i)
    kid.left = kid.left + i
    kid.parent = new_node
    new_node.kids.append(kid)
    new_node.parent = node
    node.kids.append(new_node)
    return new_node


def suffix_tree_graft(node, left, full_text):
    begin = node.depth + left
    text = full_text[begin:]
    new_node = SuffixTreeNode(text, begin, begin + len(text) - 1, node.depth + len(text))
    new_node.parent = node
    node.kids.append(new_node)


class SuffixTreeNode:

    def __init__(self, text, left, right, depth):
        self.text = text
        self.left = left
        self.right = right
        self.parent = None
        self.kids = []
        self.depth = depth

    def elem_in_kids(self, elem):
        for kid in self.kids:
            if elem == kid.text[0]: return True
        return False

    def get_kid(self, kid_name):
        for kid in self.kids:
            if kid.text[0] == kid_name: return kid

    def del_old_kid(self, kid):
        self.kids.remove(kid)


class SuffixTree:

    def __init__(self, text):
        self.root = SuffixTreeNode(text, 0, len(text) - 1, 0)
        self.build_suffix_tree()

    def build_suffix_tree(self):
        for i in range(len(self.root.text)):
            head = slow_find(self.root, self.root.text[i:])
            suffix_tree_graft(head, i, self.root.text)

    def print_suffix_tree(self, root):
        print("-" * root.depth, root.text)
        for kid in root.kids:
            self.print_suffix_tree(kid)

    def all_suffixes_are(self):
        text = self.root.text
        for i in range(len(text)):
            suffix = text[i:]
            pointer = self.root
            depth = 0
            while depth < len(suffix) and pointer.elem_in_kids(suffix[depth]):
                pointer = pointer.get_kid(suffix[depth])
                if pointer.text != suffix[depth:depth+len(pointer.text)]: return False
                depth += len(pointer.text)
            if depth != len(suffix): return False
        return True


# ilosc pauz oznacza poziom, na którym węzeł się znajduje, jeśli pod węzłem jest więcej pauz, to ten następny jest synem obecnie oglądanego,
# ojcem danego węzła jest ostatni węzeł powyżej, którego poprzedza mniej pauz
file = open("1997_714_head.txt", "r", encoding="utf8")
text = file.read() + "$"
# print("Trie")
start = time()
trieA = build_tree_schema("bbbd")
end = time()
print("Trie built in ",end-start," [s]")
# trieA.print_trie(trieA.root)
# print("Trie")
start = time()
trieB = build_tree_schema("aabbabd")
end = time()
print("Trie built in ",end-start," [s]")
# trieB.print_trie(trieB.root)
# print("Trie")
start = time()
trieC = build_tree_schema("ababcd")
end = time()
print("Trie built in ",end-start," [s]")
# trieC.print_trie(trieC.root)
# print("Trie")
start = time()
trieD = build_tree_schema("abcbccd")
end = time()
print("Trie built in ",end-start," [s]")
# trieD.print_trie(trieD.root)
start = time()
trieE = build_tree_schema(text)
end = time()
print("Trie built in ",end-start," [s]")
# print("Suffix tree")
start = time()
suffixTreeA = SuffixTree("bbbd")
end = time()
print("Suffix tree built in ",end-start," [s]")
# suffixTreeA.print_suffix_tree(suffixTreeA.root)
# print("Suffix tree")
start = time()
suffixTreeB = SuffixTree("aabbabd")
end = time()
print("Suffix tree built in ",end-start," [s]")
# suffixTreeB.print_suffix_tree(suffixTreeB.root)
# print("Suffix tree")
start = time()
suffixTreeC = SuffixTree("ababcd")
end = time()
print("Suffix tree built in ",end-start," [s]")
# suffixTreeC.print_suffix_tree(suffixTreeC.root)
# print("Suffix tree")
start = time()
suffixTreeD = SuffixTree("abcbccd")
end = time()
print("Suffix tree built in ",end-start," [s]")
# suffixTreeD.print_suffix_tree(suffixTreeD.root)
start = time()
suffixTreeE = SuffixTree(text)
end = time()
print("Suffix tree built in ",end-start," [s]")
# poprawność - sprawdzam, czy wszystkie sufiksy znalazły się w drzewie
print(trieA.all_suffixes_are("bbbd"))
print(trieB.all_suffixes_are("aabbabd"))
print(trieC.all_suffixes_are("ababcd"))
print(trieD.all_suffixes_are("abcbccd"))
print(trieE.all_suffixes_are(text))
print(suffixTreeA.all_suffixes_are())
print(suffixTreeB.all_suffixes_are())
print(suffixTreeC.all_suffixes_are())
print(suffixTreeD.all_suffixes_are())
print(suffixTreeE.all_suffixes_are())
