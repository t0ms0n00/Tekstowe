#!/usr/bin/env python
# coding: utf-8

# # Algorytmy tekstowe - laboratorium 6

# ## Autor: Tomasz Boroń

# ## Temat: Wyszukiwanie wzorca 2D

# #### Importy

# In[1]:


from queue import Queue
from string import ascii_lowercase, ascii_uppercase
from PIL import Image
from time import time


# #### Węzeł opisujący jeden stan automatu

# In[2]:


class Node:

    def __init__(self, number=-1):
        self.number = number
        self.links = {}
        self.fail_link = self


# #### Automat

# In[3]:


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
        # print("linia ", line)
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
                result[pos-len(self.final_states[ptr.number])+1] =                     self.patterns_etiquettes[self.final_states[ptr.number]]
        return result

    def text_processing(self, text):
        etiquette = 1
        for pattern in self.pattern:
            # print(pattern)
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
                if etiquette == pattern_etiq[0]: # chance to find at that position
                    for j in range(1, n):
                        if pos in lines_data[i+j].keys() and                             lines_data[i+j][pos] == pattern_etiq[j]:
                            
                            if j == n-1:
                                # print("FOUND 2D PATTERN FROM LINE ", i+1, " START POSITION ", pos) 
                                # line in file notation, indexing from 1
                                # uncomment 2 above to get place where pattern was found
                                patterns_counter += 1
                        else:
                            break
        return patterns_counter


# #### Pomocnicza funkcja zwracająca węzeł, do którego dochodzimy po danej krawędzi

# In[4]:


def next(node, letter):
    if letter in node.links.keys():
        return node.links[letter]
    return None


# #### Pomocnicza funkcja wypisująca wszystkie połączenia w automacie

# In[5]:


def print_links(root):
    print("Number ", root.number)
    for key, val in root.links.items():
        print("Link by ", key, " to ", val.number)
    print("Fail link to ", root.fail_link.number)
    for node in root.links.values():
        if node != root: print_links(node)


# #### Wstępny test

# In[6]:


fa = FA(["abc", "aab", "cba"])
print(fa.find_2d_patterns(["baabcabccc", "cbaababc", "xycbaaabzabczz", "12345cba90"]))


# #### Litera na tej samej pozycji w dwóch kolejnych liniach

# In[7]:


with open("haystack.txt", "r") as file:
    text = file.readlines()
    for sign in ascii_uppercase:
        print("Letter: ", sign)
        fa = FA([sign, sign])
        print(fa.find_2d_patterns(text))
    for sign in ascii_lowercase:
        print("Letter: ", sign)
        fa = FA([sign, sign])
        print(fa.find_2d_patterns(text))


# #### Wzorce 'th' lub 't h' w dwóch kolejnych liniach na tych samych pozycjach

# In[8]:


with open("haystack.txt", "r") as file:
    text = file.readlines()
    print("Pattern:\nth\nth")
    fa = FA(["th", "th"])
    print(fa.find_2d_patterns(text))
    print("Pattern:\nt h\nt h")
    fa = FA(["t h", "t h"])
    print(fa.find_2d_patterns(text))


# #### Wyszukiwanie liter w haystack.png

# In[9]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

a_img = Image.open("a.png")
a_pixels = image.load()
a_pixel_lines = []
for r in range (a_img.height):
    a_pixel_lines.append("")
    for c in range (a_img.width):
        a_pixel_lines[r] += str(a_pixels[c, r])
        
fa = FA(a_pixel_lines)
print(fa.find_2d_patterns(pixel_lines))


# In[10]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

r_img = Image.open("r.png")
r_pixels = image.load()
r_pixel_lines = []
for r in range (r_img.height):
    r_pixel_lines.append("")
    for c in range (r_img.width):
        r_pixel_lines[r] += str(r_pixels[c, r])
        
fa = FA(r_pixel_lines)
print(fa.find_2d_patterns(pixel_lines))


# In[11]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

e_img = Image.open("e.png")
e_pixels = image.load()
e_pixel_lines = []
for r in range (e_img.height):
    e_pixel_lines.append("")
    for c in range (e_img.width):
        e_pixel_lines[r] += str(e_pixels[c, r])
        
fa = FA(e_pixel_lines)
print(fa.find_2d_patterns(pixel_lines))


# Liczba wystąpień p a t t e r n w haystack.png

# In[12]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

p_img = Image.open("pattern.png")
p_pixels = image.load()
p_pixel_lines = []
for r in range (p_img.height):
    p_pixel_lines.append("")
    for c in range (p_img.width):
        p_pixel_lines[r] += str(p_pixels[c, r])
        
fa = FA(p_pixel_lines)
print(fa.find_2d_patterns(pixel_lines))


# Porównanie czasów dla różnych wielkości wzorca

# In[13]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

word_img = Image.open("word.png")
word_pixels = image.load()
word_pixel_lines = []
for r in range (word_img.height):
    word_pixel_lines.append("")
    for c in range (word_img.width):
        word_pixel_lines[r] += str(word_pixels[c, r])
        
start_time = time()
fa = FA(word_pixel_lines)
end_time = time()
print("Tworzenie automatu, krótki wzorzec: ", end_time - start_time, "[s]")
start_time = time()
fa.find_2d_patterns(pixel_lines)
end_time = time()
print("Szukanie wzorca, krótki wzorzec: ", end_time - start_time, "[s]")


# In[14]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

sent_img = Image.open("sentence.png")
sent_pixels = image.load()
sent_pixel_lines = []
for r in range (sent_img.height):
    sent_pixel_lines.append("")
    for c in range (sent_img.width):
        sent_pixel_lines[r] += str(sent_pixels[c, r])
        
start_time = time()
fa = FA(sent_pixel_lines)
end_time = time()
print("Tworzenie automatu, średni wzorzec: ", end_time - start_time, "[s]")
start_time = time()
fa.find_2d_patterns(pixel_lines)
end_time = time()
print("Szukanie wzorca, średni wzorzec: ", end_time - start_time, "[s]")


# In[15]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])

para_img = Image.open("paragraph.png")
para_pixels = image.load()
para_pixel_lines = []
for r in range (para_img.height):
    para_pixel_lines.append("")
    for c in range (para_img.width):
        para_pixel_lines[r] += str(para_pixels[c, r])
        
start_time = time()
fa = FA(para_pixel_lines)
end_time = time()
print("Tworzenie automatu, długi wzorzec: ", end_time - start_time, "[s]")
start_time = time()
fa.find_2d_patterns(pixel_lines)
end_time = time()
print("Szukanie wzorca, długi wzorzec: ", end_time - start_time, "[s]")


# Podział na kawałki i porównanie czasów przeszukiwania

# In[16]:


image = Image.open("haystack.png")
pixels = image.load()
pixel_lines = []
for r in range (image.height):
    pixel_lines.append("")
    for c in range (image.width):
        pixel_lines[r] += str(pixels[c, r])
        
word_img = Image.open("word.png")
word_pixels = image.load()
word_pixel_lines = []
for r in range (word_img.height):
    word_pixel_lines.append("")
    for c in range (word_img.width):
        word_pixel_lines[r] += str(word_pixels[c, r])
        
fa = FA(word_pixel_lines)


# In[17]:


def split_image(pixel_lines, parts):
    lines = len(pixel_lines)
    split_at = int(lines/parts)
    texts = []
    for i in range(parts-1):
        texts.append(pixel_lines[i*split_at:(i+1)*split_at])
    texts.append(pixel_lines[(parts-1)*split_at:])
    return texts


# In[18]:


parts = [2,4,8]

for i in parts:
    texts = split_image(pixel_lines, i)
    start_time = time()
    for text in texts:
        fa.find_2d_patterns(text)
    end_time = time()
    print("Części {} czas {} [s]".format(i ,end_time-start_time))

