import itertools
import time
import sys
import msoffcrypto
from io import BytesIO


def brute_force_word(file_path, dictionary, min_len, max_len, allow_repeats):
    print("\n[INFO] Перебор паролей для Word файла...\n")
    print("[INFO] Конфигурация:")
    print(f"- Словарь: {''.join(dictionary)}")
    print(f"- Минимальная длина: {min_len}")
    print(f"- Максимальная длина: {max_len}")
    print(f"- Повторы символов разрешены: {allow_repeats}")
    print("\n" + "=" * 40 + "\n")

    time.sleep(2)  # Пауза для удобства восприятия
    start_time = time.time()

    try:
        for length in range(min_len, max_len + 1):  # Перебор длины пароля
            if allow_repeats:
                combinations = itertools.product(dictionary, repeat=length)
            else:
                combinations = itertools.permutations(dictionary, length)

            for combo in combinations:
                password = ''.join(combo)
                sys.stdout.write(f"\033[92m{password}\033[0m\n")  # Вывод перебираемого пароля
                sys.stdout.flush()

                # Попытка открыть Word-файл с текущим паролем
                try:
                    with open(file_path, "rb") as f:
                        encrypted_file = msoffcrypto.OfficeFile(f)
                        encrypted_file.load_key(password=password)  # Загружаем ключ пароля
                        decrypted = BytesIO()
                        encrypted_file.decrypt(decrypted)  # Попытка расшифровки
                    print(f"\n[SUCCESS] Пароль найден: {password}")
                    elapsed_time = time.time() - start_time
                    print(f"[INFO] Выполнено за {elapsed_time:.2f} секунд(ы)")
                    return password
                except msoffcrypto.exceptions.InvalidKeyError:
                    continue  # Если пароль неверный, продолжаем перебор
    except KeyboardInterrupt:
        print("\n\n[INFO] Остановлено пользователем.")

    elapsed_time = time.time() - start_time
    print(f"\n[FAILED] Пароль не найден. Выполнено за {elapsed_time:.2f} секунд(ы)")
    return None


# =============================
# ТЕСТОВАЯ СЕКЦИЯ
# =============================

if __name__ == "__main__":
    # Задание параметров атаки
    dictionary = list("1234567890")  # Словарь символов
    min_len = 4  # Минимальная длина пароля
    max_len = 6  # Максимальная длина пароля
    allow_repeats = True  # Разрешить повторы символов (если известно, что они могут повторяться)
    file_path = "Попробуй.docx"  # Путь к защищённому файлу

    # Запуск программы
    brute_force_word(file_path, dictionary, min_len, max_len, allow_repeats)
