#!/usr/bin/env python
# coding: utf-8

# # Algorytmy tekstowe - laboratorium 5

# ## Autor: Tomasz Boroń

# ## Temat: Metryki w przestrzeni napisów

# #### Wstępne informacje

# Ze względu na wolne działanie algorytmu DBSCAN w połączeniu z metrykami o złożoności kwadratowej musiałem obciąć zbiór linii do ok. 250 linijki pliku lines.txt.  
# Czasy wykonania uwzględnione są poniżej w miejscach wywoływania funkcji.  
# Poglądowe wyniki klasteryzacji dodatkowo zapisałem w plikach tekstowych, które umieściłem w dołączonym folderze results.zip  
# Pliki z końcówką "_sl.txt" to wyniki przy zastosowaniu stoplisty.

# #### Importy

# In[1]:


from math import sqrt
from spacy.tokenizer import Tokenizer
from spacy.lang.en import English
from time import time


# #### Zmienne globalne

# In[2]:


init_etiquette = "UNDEFINED"
noise_etiquette = "NOISE"


# #### Klasa reprezentująca jeden wiersz pliku

# In[3]:


class DBElement:
    def __init__(self, value):
        self.value = value
        self.etiquette = init_etiquette

    def set_etiquette(self, etiquette):
        self.etiquette = etiquette


# #### Funkcje do wyznaczania n-gramów

# In[4]:


def n_grams_no_count(text, n):
    n_grams = set()
    tmp = text[:n]
    n_grams.add(tmp)
    for i in range(n, len(text)):
        tmp = tmp[1:] + text[i]
        n_grams.add(tmp)
    return n_grams


# In[5]:


def n_grams_with_count(text, n):
    n_grams = {}
    tmp = text[:n]
    n_grams[tmp] = 1
    for i in range(n, len(text)):
        tmp = tmp[1:] + text[i]
        if tmp in n_grams.keys():
            n_grams[tmp] += 1
        else:
            n_grams[tmp] = 1
    return n_grams


# #### Metryka DICE

# In[6]:


def dice(text_1, text_2, *args):
    n = args[0]
    set_1 = n_grams_no_count(text_1, n)
    set_2 = n_grams_no_count(text_2, n)
    return 1 - (2*len(set_1 & set_2) / ((len(set_1)) + len(set_2)))


# #### Metryka cosinusowa

# In[7]:


def vector_norm(dict):
    norm = 0
    for val in dict.values():
        norm += (val * val)
    return sqrt(norm)


# In[8]:


def cosine_metric(text_1, text_2, *args):
    n = args[0]
    d_1 = n_grams_with_count(text_1, n)
    d_2 = n_grams_with_count(text_2, n)
    scalar = 0
    for key, val in d_1.items():
        if key in d_2.keys():
            scalar = scalar + d_1[key] * d_2[key]
    text_1_norm = vector_norm(d_1)
    text_2_norm = vector_norm(d_2)
    return 1 - (scalar / (text_1_norm * text_2_norm))


# #### Metryka LCS

# In[9]:


def lcs(text_1, text_2, *args):
    m = len(text_1)
    n = len(text_2)
    max_substring = 0
    matrix = []
    for i in range(m+1):
        matrix.append([-1]*(n+1))
    for i in range(m+1):
        matrix[i][0] = 0
    for i in range(n+1):
        matrix[0][i] = 0
    for i in range(m):
        for j in range(n):
            if text_1[i] != text_2[j]:
                matrix[i+1][j+1] = 0
            else:
                matrix[i+1][j+1] = matrix[i][j] + 1
                if matrix[i+1][j+1] > max_substring:
                    max_substring = matrix[i+1][j+1]
    return 1-max_substring/max(m, n)


# #### Metryka Levenshteina

# In[10]:


def Levenshtein_metric(text_1, text_2, *args):
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
            cost = 0 if text_1[i-1] == text_2[j-1] else 1
            matrix[i][j] = min(matrix[i - 1][j] + 1, matrix[i][j - 1] + 1, matrix[i - 1][j - 1] + cost)
    return matrix[m][n]/max(m, n)


# #### DBSCAN

# In[11]:


def range_query(database, metric, representative, eps, *args):
    n = args[0] if len(args) > 0 else None
    neighbours = []
    for point in database:
        if metric(representative.value, point.value, n) <= eps:
            # print("Znaleziono sąsiada ", point.value)
            neighbours.append(point)
    return neighbours


# In[12]:


def dbscan(database, metric, eps, min_points, *args):
    n = args[0] if len(args) > 0 else None
    cluster_num = 0
    for index in range(len(database)):
        point = database[index]
        if index%10 == 0: 
            print(index)
        if point.etiquette != init_etiquette:
            continue
        neighbours = range_query(database, metric, point, eps, n)
        if len(neighbours) < min_points:
            point.set_etiquette(noise_etiquette)
            continue
        cluster_num += 1
        point.set_etiquette(str(cluster_num))
        neighbours.remove(point)
        for neighbour in neighbours:
            if neighbour.etiquette == noise_etiquette:
                neighbour.set_etiquette(str(cluster_num))
            if neighbour.etiquette != init_etiquette:
                continue
            neighbour.set_etiquette(str(cluster_num))
            new_neighbours = range_query(database, metric, neighbour, eps, n)
            if len(new_neighbours) >= min_points:
                neighbours.extend(new_neighbours)


# In[13]:


def get_etiquette(point):
    return point.etiquette


# #### Część testowa

# #### Metryka DICE

# In[14]:


db = []

with open("lines.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))
        
start_time = time()
dbscan(db, dice, 0.75, 3, 10)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_dice.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Metryka cosinusowa

# In[15]:


db = []

with open("lines.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, cosine_metric, 0.75, 3, 10)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_cosine.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### LCS

# In[16]:


db = []

with open("lines.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, lcs, 0.75, 3)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_lcs.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Odległość edycyjna

# In[17]:


db = []

with open("lines.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, Levenshtein_metric, 0.65, 3)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_levenshtein.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Stoplista

# In[18]:


with open("lines.txt",'r') as file:
    text = str(file.readlines())
    nlp = English()
    tokenizer = Tokenizer(nlp.vocab)
    tokens = tokenizer(text)
phrase_counter = {}
for token in tokens:
    key = str(token)
    if key not in phrase_counter.keys():
        phrase_counter[key] = 1
    else:
        phrase_counter[key] += 1
phrase_list = []
for key, val in phrase_counter.items():
    phrase_list.append((val, key))
phrase_list.sort(reverse = True)
tmp = phrase_list[0:len(phrase_list)//25]
stop_list = [x[1] for x in tmp]
for elem in stop_list:
    if len(elem) < 3:
        stop_list.remove(elem)
# print(stop_list)

with open("lines_w_stoplist.txt", 'w') as file, open("lines.txt",'r') as data:
    for line in data:
        words = tokenizer(line)
        for word in words:
            if str(word) not in stop_list:
                file.write(str(word))
                file.write(' ')


# #### Część testowa ze stoplistą

# #### Metryka DICE

# In[19]:


db = []

with open("lines_w_stoplist.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, dice, 0.75, 3, 10)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_dice_sl.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Metryka cosinusowa

# In[20]:


db = []

with open("lines_w_stoplist.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, cosine_metric, 0.75, 3, 10)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_cosine_sl.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### LCS

# In[21]:


db = []

with open("lines_w_stoplist.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))

start_time = time()
dbscan(db, lcs, 0.75, 3)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_lcs_sl.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Odległość edycyjna

# In[22]:


db = []

with open("lines_w_stoplist.txt", 'r') as file:
    while 1:
        line = file.readline()
        if not line:
            break
        db.append(DBElement(line))
        
start_time = time()
dbscan(db, Levenshtein_metric, 0.65, 3)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

db.sort(key = lambda x: get_etiquette(x))

i = 0
with open("results_levenshtein_sl.txt", 'w') as file:
    while i < len(db):
        file.write("========CLUSTER========\n")
        if get_etiquette(db[i]) != "NOISE":
            comparator = i
            while get_etiquette(db[comparator]) == get_etiquette(db[i]):
                file.write(db[i].value)
                i += 1
            file.write("\n")
        else:
            file.write(db[i].value)
            file.write("\n")
        i += 1


# #### Ocena jakości klasteryzacji

# #### Funkcja konwertująca wynikowy plik .txt na listę klastrów

# In[28]:


def file_to_clusters(filename):
    cluster = []
    clusters = []
    with open(filename, 'r') as file:
        for line in file:
            if line == "========CLUSTER========\n":
                cluster = []
            elif line == "\n":
                clusters.append(cluster)
            else:
                cluster.append(line)
    return clusters


# #### Indeks Dunna

# Odległość między klastrami - najmniejsza odległość pomiędzy 1 elementem klastra pierwszego i 1 elementem klastra drugiego.  
# Wielkość klastra - największa odległość między elementami klastra.

# In[29]:


def inter_cluster_dist(cluster1, cluster2, metric, *args):
    n = args[0]
    value = metric(cluster1[0], cluster2[0], n)
    for elem1 in cluster1:
        for elem2 in cluster2:
            value = min(value, metric(elem1, elem2, n))
    return value


# In[30]:


def inside_cluster_dist(cluster, metric, *args):
    n = args[0]
    value = 0
    for elem1 in cluster:
        for elem2 in cluster:
            value = max(value, metric(elem1, elem2, n))
    return value


# In[31]:


def dunn_index(filename, metric, *args):
    n = args[0] # for metrics with n-grams
    clusters = file_to_clusters(filename)
    numerator = 1.0
    denominator = -1.0
    for i in range(len(clusters)):
        act = clusters[i]
        denominator = max(denominator, inside_cluster_dist(act, metric, n))
        for j in range(i+1,len(clusters)):
            neighbour = clusters[j]
            numerator = min(numerator, inter_cluster_dist(act, neighbour, metric, n))
    return numerator/denominator


# #### Silhouette

# In[39]:


def calc_a(point, cluster, metric, *args):
    n = args[0]
    numerator = 0
    denominator = len(cluster)-1
    for neighbour in cluster:
        numerator += metric(point, neighbour, n)
    return numerator/denominator


# In[40]:


def calc_b(point, cluster, clusters, metric, *args):
    n = args[0]
    min_val = 1
    for group in clusters:
        if group != cluster:
            dist_sum = 0
            for elem in group:
                dist_sum += metric(point, elem, n)
            min_val = min(min_val, dist_sum/len(group))
    return min_val


# In[41]:


def silhouette(filename, metric, *args):
    n = args[0] # for metrics with n-grams
    clusters = file_to_clusters(filename)
    a_values = []
    b_values = []
    for i in range(len(clusters)):
        if len(clusters[i]) == 1:
            a_values.append(0)
        else:
            for point in clusters[i]:
                a_values.append(calc_a(point, clusters[i], metric, n))
        for point in clusters[i]:
            b_values.append(calc_b(point, clusters[i], clusters, metric, n))
    s_values = []
    for i in range(len(a_values)):
        value = 1-a_values[i]/b_values[i] if a_values[i]<b_values[i] else b_values[i]/a_values[i]-1
        s_values.append(value)
    return sum(s_values)/len(s_values)


# #### Wyniki oceny jakości

# In[42]:


print("Dunn index for dice, no stoplist", dunn_index("results_dice.txt", dice, 10))
print("Silhouette index for dice, no stoplist", silhouette("results_dice.txt", dice, 10))


# In[43]:


print("Dunn index for dice, stoplist", dunn_index("results_dice_sl.txt", dice, 10))
print("Silhouette index for dice, stoplist", silhouette("results_dice_sl.txt", dice, 10))


# In[44]:


print("Dunn index for cosine, no stoplist", dunn_index("results_cosine.txt", cosine_metric, 10))
print("Silhouette index for cosine, no stoplist", silhouette("results_cosine.txt", cosine_metric, 10))


# In[45]:


print("Dunn index for cosine, stoplist", dunn_index("results_cosine_sl.txt", cosine_metric, 10))
print("Silhouette index for cosine, stoplist", silhouette("results_cosine_sl.txt", cosine_metric, 10))


# In[46]:


print("Dunn index for lcs, no stoplist", dunn_index("results_lcs.txt", lcs, 10))
print("Silhouette index for lcs, no stoplist", silhouette("results_lcs.txt", lcs, 10))


# In[47]:


print("Dunn index for lcs, stoplist", dunn_index("results_lcs_sl.txt", lcs, 10))
print("Silhouette index for lcs, stoplist", silhouette("results_lcs_sl.txt", lcs, 10))


# In[48]:


print("Dunn index for Levenshtein, no stoplist", dunn_index("results_levenshtein.txt", Levenshtein_metric, 10))
print("Silhouette index for Levenshtein, no stoplist", silhouette("results_levenshtein.txt", Levenshtein_metric, 10))


# In[49]:


print("Dunn index for Levenshtein, stoplist", dunn_index("results_levenshtein_sl.txt", Levenshtein_metric, 10))
print("Silhouette index for Levenshtein, stoplist", silhouette("results_levenshtein_sl.txt", Levenshtein_metric, 10))


# #### Wnioski

# - Współczynnik Silhouette sugeruje dobrą klasteryzację, natomiast współczynnik Dunne'a zawsze jest zaskakująco niski. Spoglądając dodatkowo w pliki wynikowe można stwierdzić, że wszystkie metody poza metryką Levenshteina dość dobrze przeprowadzały klasteryzację.  
# - Poprawienie jakości klasteryzacji można by sprawdzić używając innego algorytmu klasteryzacji, np. k-means. Natomiast niewątpliwą zaletą DBSCANA jest to, że nie musimy znać liczby klastrów, trzeba dopasować jedynie espilon określający czy teksty są dostatecznie podobne oraz rozmiar zbioru podobnych linii aby można było z nich stworzyć grupę.  
# - Zauważalną wadą DBSCANA jest jego kwadratowa złożoność, która w kombinacji z metryką obliczaną w czasie O(n^2) mocno spowalnia działanie programu.  
# - Przy użyciu stoplisty zwykle wzrastała wartość indeksu Dunne'a a malała wartość Silhouette. Zmiany te poza Levenshteinem są niewielkie, natomiast wyraźne zmiany pojawiły się w długości czasu przetwarzania - krótszy tekst, mniej obliczeń. Zatem uważam, że wprowadzenie stoplisty jest zaletą, dlatego że skraca przetwarzane linie o słowa, które nie powinny mieć większego wpływu na wynik (co widać po kryteriach jakości). Stoplista znacząco poprawiła wyniki z metodą Levenshteina, natomiast i tak są one znacznie niższe niż pozostałe, więc w praktyce nie zdecydowałbym się na tę metrykę.
