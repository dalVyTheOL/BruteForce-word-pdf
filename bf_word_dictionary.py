import time
import sys
import msoffcrypto
from io import BytesIO


def brute_force_word(file_path, wordlist_path):
    print("\n[INFO] Начат перебор паролей из словаря для Word файла...\n")
    print(f"[INFO] Используемый словарь: {wordlist_path}")
    print("\n" + "=" * 40 + "\n")

    time.sleep(2)
    start_time = time.time()

    try:
        with open(wordlist_path, 'r', encoding='utf-8') as wordlist_file:
            for line in wordlist_file:
                password = line.strip()
                sys.stdout.write(f"\033[92m{password}\033[0m\n")  # Вывод текущего пароля
                sys.stdout.flush()

                try:
                    with open(file_path, "rb") as f:
                        encrypted_file = msoffcrypto.OfficeFile(f)
                        encrypted_file.load_key(password=password)
                        decrypted = BytesIO()
                        encrypted_file.decrypt(decrypted)
                    print(f"\n[SUCCESS] Пароль найден: {password}")
                    elapsed_time = time.time() - start_time
                    print(f"[INFO] Выполнено за {elapsed_time:.2f} секунд(ы)")
                    return password
                except msoffcrypto.exceptions.InvalidKeyError:
                    continue  # Неправильный пароль, продолжаем
    except FileNotFoundError:
        print(f"[ERROR] Файл словаря не найден: {wordlist_path}")
    except KeyboardInterrupt:
        print("\n\n[INFO] Остановлено пользователем.")

    elapsed_time = time.time() - start_time
    print(f"\n[FAILED] Пароль не найден. Выполнено за {elapsed_time:.2f} секунд(ы)")
    return None


# =============================
# ТЕСТОВАЯ СЕКЦИЯ
# =============================

if __name__ == "__main__":
    file_path = "example.docx"          # Путь к защищённому файлу
    wordlist_path = "passwords.txt"      # Путь к словарю с паролями

    brute_force_word(file_path, wordlist_path)
