import numpy as np
from original_text import load_file

# Відкриття файлу оригіналу тексту
origin_text = load_file('original_text.txt').upper().replace(" ", "")

# Визначення порядку перестановки символів у шифрі 
def get_permutation_key(keyword):
    sorted_key = sorted(enumerate(keyword), key=lambda x: x[1])

    return [i for i, _ in sorted((sorted_key), key=lambda x: x)]

# Функція шифрування методом перевстановки
def encrypt_transposition(text, keyword):
    # Отримання порядку перестановки символів
    key_order = get_permutation_key(keyword)

    # Визначення розміру таблиці
    num_cols = len(keyword)
    num_rows = -(-len(text) // num_cols)
    # Доповнення тексту пробілами
    text += ' ' * (num_cols * num_rows - len(text))

    # Побудова матриці та перестановка стовпців у відповідності до key_order
    matrix = np.array(list(text)).reshape(num_rows, num_cols)
    encrypted_text = ''.join(matrix[:, key_order].flatten(order='F'))

    return encrypted_text

# Функція розшифровки за методом перестановки
def decrypt_transposition(ciphertext, keyword):
    # Отримання порядку перестановки символів
    key_order = get_permutation_key(keyword)

    # Визначення розміру таблиці
    num_cols = len(keyword)
    num_rows = -(-len(ciphertext) // num_cols)

    # Перевірка довжини тексту. Якщо менша за очікувану, додаємо пробіли
    expected_len = num_cols * num_rows
    ciphertext += ' ' * (expected_len - len(ciphertext))

    # Створення порожньої матриці
    matrix = np.empty((num_rows, num_cols), dtype=str)
    # Заповнення матриці
    index = 0
    for col in key_order:
        matrix[:, col] = list(ciphertext[index:index + num_rows])
        index += num_rows

    # Відновлення вихідного тексту
    decrypted_text = ''.join(matrix.flatten(order='C')).rstrip()

    return decrypted_text

# Функція подвійного шивлування методом перестановки
def double_encrypt_transposition(text, key1, key2):
    return encrypt_transposition(encrypt_transposition(text, key1), key2)

# Функція розшифрування за методом подвійної перестановки
def double_decryption_transposition(ciphertext, key1, key2):
    return decrypt_transposition(decrypt_transposition(ciphertext, key2), key1)

# Вхідні параметри
keyword1 = "SECRET"
keyword2 = "CRYPTO"
text = origin_text

ciphertext = encrypt_transposition(text, keyword1)
decrypted_text = decrypt_transposition(ciphertext, keyword1)

double_encrypt = double_encrypt_transposition(origin_text, keyword1, keyword2)
double_decrypt = double_decryption_transposition(double_encrypt, keyword1, keyword2)

print("Зашифрований текст:", ciphertext)
print("Розшифрований текст:", decrypted_text)

print('Подвійний шифр:', double_encrypt)
print('Розшифровка подвійнийного шифру:', double_decrypt)