import pikepdf
from tqdm import tqdm

passwords = [line.strip() for line in open("pass.txt", encoding="UTF-8")]  # Использование словаря для перебора паролей

for password in tqdm(passwords, "Подбор пароля для Pdf-файла"):
    try:
        with pikepdf.open("test.pdf", password=password) as pdf:  # Зашифрованный файл
            print("Пароль найден: ", password)
            break
    except pikepdf.PasswordError:
        continue