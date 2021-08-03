# Autor: Tomasz Boron

# Algorytmy

from time import time

def naive_string_matching(text, pattern):
    counter = 0
    for s in range(0, len(text) - len(pattern) + 1):
        if (pattern == text[s:s + len(pattern)]):
            counter += 1
            #print(f"Przesunięcie {s} jest poprawne")
    print("Liczba wystapien wzorca ", counter)


def transition_table(pattern):
    alphabet = []
    for letter in pattern:
        if alphabet.count(letter) == 0:
            alphabet.append(letter)
    result = []
    for q in range(len(pattern) + 1):
        result.append({})
        for a in alphabet:
            x = pattern[:q] + a
            #print("Obecny x:",x)
            k = min(len(pattern) + 1, q + 2)
            while k > 0:
                k = k - 1
                if pattern[:k] == x[-k:]:
                    break
            result[q][a] = k
    return result


def fa_string_matching(text, delta):
    counter = 0
    q = 0
    for s in range(0, len(text)):
        if text[s] not in delta[q].keys():
            q=0
            continue
        q = delta[q][text[s]]
        if (q == len(delta) - 1):
            counter += 1
            #print(f"Przesunięcie {s + 1 - q} jest poprawne")
            # s + 1 - ponieważ przeczytaliśmy znak o indeksie s, więc przesunięcie jest po tym znaku
    print("Liczba wystapien wzorca ", counter)


def prefix_function(pattern):
    pi = [0]
    k = 0
    for q in range(1, len(pattern)):
        while (k > 0 and pattern[k] != pattern[q]):
            k = pi[k - 1]
        if (pattern[k] == pattern[q]):
            k = k + 1
        pi.append(k)
    return pi


def kmp_string_matching(text, pattern):
    counter = 0
    pi = prefix_function(pattern)
    q = 0
    for i in range(0, len(text)):
        while (q > 0 and pattern[q] != text[i]):
            q = pi[q - 1]
        if (pattern[q] == text[i]):
            q = q + 1
        if (q == len(pattern)):
            counter += 1
            #print(f"Przesunięcie {i + 1 - q} jest poprawne")
            q = pi[q - 1]
    print("Liczba wystapien wzorca ", counter)

# Testy:
# Poprawnosc - uzyto przykladu z wykladu
print("Test poprawnosci")
print("Algorytm naiwny")
start_time = time()
naive_string_matching("abaabaaaaba","aba")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching("abaabaaaaba", transition_table("aba"))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching("abaabaaaaba", "aba")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

# Szybkosc - poniewaz przeprowadzono testy dla tekstow dlugich o powtarzajacym sie okresie*
# zakomentowane zostaly linijki odpowiadajace za wypisywanie indeksow liter od ktorych rozpoczyna sie
# poprawne przesuniecie, w celu poprawienia czytelnosci czasow dzialania, dla pewnosci ze algorytmy dzialaja zliczam ilosc
# wystapien wzorca; przy checi dokladnej weryfikacji prosze odkomentowac linijki postaci:
# print(f"Przesunięcie [wzor] jest poprawne")
# *(wybralem takie bo najlatwiej bylo ujac czytelnie wieksze dane wejsciowe)

print("\nTesty szybkosci algorytmow")

print("\n1 przypadkowy tekst")

print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching("fdjdj"*1000000,"djf")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching("fdjdj"*1000000, transition_table("djf"))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching("fdjdj"*1000000, "djf")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

print("\n2 maly zbior liter, wzorzec niepasujacy do tekstu")

print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching("abba"*1000000,"bab")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching("abba"*1000000, transition_table("bab"))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching("abba"*1000000, "bab")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

print("\n3 dopasowanie na kazdej z pierwszych |text|-|pattern|+1 pozycji")

print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching("aa"*10000,"aaaaa")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching("aa"*10000, transition_table("aaaaa"))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching("aa"*10000, "aaaaa")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

print("\n4 duzy zbior dostepnych znakow")

print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching("abcdefghijklmnoprstuvwz"*1000000,"abcdefghijklmnoprstuvwz")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching("abcdefghijklmnoprstuvwz"*1000000, transition_table("abcdefghijklmnoprstuvwz"))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching("abcdefghijklmnoprstuvwz"*1000000, "abcdefghijklmnoprstuvwz")
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

# Wystapienia "art" z zalaczonej ustawy i czas dzialania algorytmow

print("\nWystapienia wzorca \"art\" w zalaczonej ustawie")

file = open("1997_714.txt","r",encoding="utf8")
text=file.read()
pattern="art"
print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching(text,pattern)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
start_time = time()
fa_string_matching(text, transition_table(pattern))
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm KMP")
start_time = time()
kmp_string_matching(text, pattern)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")

print("\nDopasowanie KMP i FA >5 razy krotsze od algorytmu naiwnego")

def fa_match_time(text, delta):
    start_time=time()
    counter = 0
    q = 0
    for s in range(0, len(text)):
        if text[s] not in delta[q].keys():
            q=0
            continue
        q = delta[q][text[s]]
        if (q == len(delta) - 1):
            counter += 1
            #print(f"Przesunięcie {s + 1 - q} jest poprawne")
            # s + 1 - ponieważ przeczytaliśmy znak o indeksie s, więc przesunięcie jest po tym znaku
    end_time=time()
    print("Liczba wystapien wzorca ", counter)
    print("Czas dzialania: ", end_time - start_time, "[s]")


def kmp_match_time(text, pattern):
    counter = 0
    pi = prefix_function(pattern)
    start_time=time()
    q = 0
    for i in range(0, len(text)):
        while (q > 0 and pattern[q] != text[i]):
            q = pi[q - 1]
        if (pattern[q] == text[i]):
            q = q + 1
        if (q == len(pattern)):
            counter += 1
            #print(f"Przesunięcie {i + 1 - q} jest poprawne")
            q = pi[q - 1]
    end_time=time()
    print("Liczba wystapien wzorca ", counter)
    print("Czas dzialania: ", end_time - start_time, "[s]")


text="a"*100000
pattern="a"*1000+"b"
print("\nAlgorytm naiwny")
start_time = time()
naive_string_matching(text,pattern)
end_time = time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nAlgorytm automatu skończonego")
fa_match_time(text,transition_table(pattern))
print("\nAlgorytm KMP")
kmp_match_time(text,pattern)

print("\nWorstcase funkcja przejscia - funkcja prefiksow")

pattern="abcdefghijklmnopqrstuvwxyz"*50
print("\nTablica przejsc")
start_time=time()
transition_table(pattern)
end_time=time()
print("Czas dzialania: ", end_time - start_time, "[s]")
print("\nFunkcja prefiksow")
start_time=time()
prefix_function(pattern)
end_time=time()
print("Czas dzialania: ", end_time - start_time, "[s]")
