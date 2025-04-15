import itertools
import time
import sys
import pikepdf
from tqdm import tqdm


def brute_force_pdf(file_path, dictionary, min_len, max_len, allow_repeats):
    print("\n[INFO] Перебор паролей для PDF файла...\n")
    print("[INFO] Конфигурация:")
    print(f"- Словарь: {''.join(dictionary)}")
    print(f"- Минимальная длина: {min_len}")
    print(f"- Максимальная длина: {max_len}")
    print(f"- Повторы символов разрешены: {allow_repeats}")
    print("\n" + "=" * 40 + "\n")

    time.sleep(2)
    start_time = time.time()

    try:
        for length in range(min_len, max_len + 1):
            if allow_repeats:
                combinations = itertools.product(dictionary, repeat=length)
            else:
                if length > len(dictionary):
                    continue  # Невозможно сделать без повторов
                combinations = itertools.permutations(dictionary, length)

            total_combinations = (
                len(dictionary) ** length if allow_repeats else math.perm(len(dictionary), length)
            )
            for combo in tqdm(combinations, total=total_combinations, desc=f"Длина {length}"):
                password = ''.join(combo)
                sys.stdout.write(f"\rПробуем: {password}   ")
                sys.stdout.flush()

                try:
                    with pikepdf.open(file_path, password=password) as pdf:
                        print(f"\n[SUCCESS] Пароль найден: {password}")
                        elapsed_time = time.time() - start_time
                        print(f"[INFO] Выполнено за {elapsed_time:.2f} секунд(ы)")
                        return password
                except pikepdf.PasswordError:
                    continue
    except KeyboardInterrupt:
        print("\n\n[INFO] Остановлено пользователем.")

    elapsed_time = time.time() - start_time
    print(f"\n[FAILED] Пароль не найден. Выполнено за {elapsed_time:.2f} секунд(ы)")
    return None


# =============================
# ТЕСТОВАЯ СЕКЦИЯ
# =============================

if __name__ == "__main__":
    import math  # Нужно для perm()

    # Конфигурация
    dictionary = list("viature")  # Словарь символов
    min_len = 4
    max_len = 5
    allow_repeats = True
    file_path = "test.pdf"

    brute_force_pdf(file_path, dictionary, min_len, max_len, allow_repeats)
