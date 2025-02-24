from original_text import load_file

# Відкриття файлу оригіналу тексту
origin_text = load_file('original_text.txt').upper().replace(" ", "")

def create_table(text, columns):
    """Створює таблицю з тексту за допомогою кількості стовпців"""

    rows = len(text) // columns + (1 if len(text) % columns != 0 else 0)
    table = [[''] * columns for _ in range(rows)]

    for i, char in enumerate(text):
        row = i // columns
        col = i % columns
        table[row][col] = char
    
    return table, rows

def encrypt(text, key):
    """Шифрує текст за допомогою табличного шифру та ключа"""

    key_order = sorted(range(len(key)), key=lambda x: key[x])
    columns = len(key)
    text = text.replace(" ", "").upper()  # Видалення пробілів і перехід до великих літер
    
    # Створення таблиці за допомогою функції create_table
    table, rows = create_table(text, columns)
    
    # Якщо кількість елементів у таблиці менша, ніж потрібно, додаємо пробіли
    while len(table) * columns < len(text):
        table.append([' '] * columns)
    
    cipher_text = ''
    
    # Читання таблиці по стовпцях за порядком ключа
    for index in key_order:
        for row in table:
            if index < len(row):  # Перевірка, чи є такий стовпець
                cipher_text += row[index]
    
    return cipher_text

def decrypt(cipher_text, key):
    """Дешифрує текст за допомогою табличного шифру та ключа"""
    
    # Визначаємо кількість стовпців
    columns = len(key)  
    # Визначаємо порядок колонок під час шифрування
    key_order = sorted(range(len(key)), key=lambda x: key[x])  
    
    # Визначаємо кількість рядків
    rows = len(cipher_text) // columns + (1 if len(cipher_text) % columns else 0) 
    
    # Визначаємо, скільки символів буде в кожному стовпці
    num_full_cols = len(cipher_text) % columns  
    col_sizes = [rows if i < num_full_cols else rows - 1 for i in range(columns)]
    
    # Розподіляємо шифртекст по стовпцях
    table_columns = [''] * columns 
    index = 0
    for col_index in key_order:
        table_columns[col_index] = cipher_text[index:index + col_sizes[col_index]]
        index += col_sizes[col_index]
    
    # Відновлення тексту по рядках
    decrypted_text = ''
    for row in range(rows):
        for col in range(columns):
            # Переконуємося, що символи є в цьому рядку
            if row < len(table_columns[col]):  
                decrypted_text += table_columns[col][row]
    
    return decrypted_text

# Приклад використання
key = "MATRIX"
text = origin_text
cipher_text = encrypt(text, key)
print("Шифртекст:", cipher_text)

decrypted_text = decrypt(cipher_text, key)
print("Розшифрований текст:", decrypted_text)
