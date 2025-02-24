from original_text import load_file

import re
from collections import Counter

origin_text = load_file('original_text.txt').upper().replace(" ", "")

# Функція розшинерення ключа до довжини тексту
def extend_key(text, key):
    key = list(key)
    # Якщо довжина ключа меньша за текст, циклічно повторюємо його 
    if len(text) == len(key):
        return key
    else:
        for i in range(len(text) - len(key)):
            key.append(key[i % len(key)])
        
    return ''.join(key)

# Функція шифрування за методом Віженера
def encrypt(text, key):
    # Розширюємо ключ
    key = extend_key(text, key)
    # Список для зашифрованого тексту
    encrypted_text = []

    for i in range(len(text)):
        x = ((ord(text[i]) - ord("A")) + (ord(key[i]) - ord('A'))) % 26
        x += ord('A')
        encrypted_text.append(chr(x))

    return ''.join(encrypted_text)

# Функція розшифрування шифру за методом Віженера
def decrypted(text, key):
    key = extend_key(text, key)
    origin_text = []

    for i in range(len(text)):
        x = ((ord(text[i]) - ord('A')) - (ord(key[i])  - ord('A')) + 26) % 26
        x += ord('A')
        origin_text.append(chr(x))

    return ''.join(origin_text)

text = origin_text
key = "CRYPTOGRAPHY"
encrypted_text = encrypt(text, key)
print("Зашифрований текст:", encrypted_text)

decrypted_text = decrypted(encrypted_text, key)
print("Розшифрований текст:", decrypted_text)

# Функція для пошуку повторюваних шаблонів
def find_repeating_patterns(text, n=3):
    # Створюємо регулярний вираз для пошуку n-літерних блоків
    pattern = r"(?=(\w{%d}))" % n
    matches = re.findall(pattern, text)
    return matches

# Функція для обчислення відстаней між однаковими шаблонами
def calculate_distances(matches):
    distances = {}
    
    # Створюємо словник, де ключем є шаблон, а значенням - список індексів
    for index, match in enumerate(matches):
        if match not in distances:
            distances[match] = []
        distances[match].append(index)
    
    # Обчислюємо відстані між кожною парою повторів шаблону
    distance_list = []
    for match, indices in distances.items():
        for i in range(1, len(indices)):
            distance_list.append(indices[i] - indices[i-1])
    
    return distance_list

# Функція для пошуку ймовірної довжини ключа
def find_key_length(crypted_text, n=3):
    # Пошук повторюваних шаблонів
    matches = find_repeating_patterns(crypted_text, n)
    
    # Обчислення відстаней між повторюваними шаблонами
    distances = calculate_distances(matches)
    
    # Підрахунок найпоширеніших відстаней (ці значення можуть бути корисні для визначення довжини ключа)
    counter = Counter(distances)
    most_common = counter.most_common(10)  # Отримуємо 10 найбільш поширених відстаней
    print(f"Найбільш поширені відстані: {most_common}")
    
    return most_common

# Приклад шифротексту (замість цього використовуйте свій шифротекст)
ciphertext = encrypted_text

# Викликаємо функцію для пошуку ймовірної довжини ключа
key_length_candidates = find_key_length(ciphertext, n=3)

