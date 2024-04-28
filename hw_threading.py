import os
import threading

# Функція для пошуку ключових слів у файлі
def search_keywords_in_file(file_path, keywords, results):
    file_name = os.path.basename(file_path)
    found_keywords = []
    with open(file_path, 'r') as file:
        for line in file:
            for keyword in keywords:
                if keyword in line:
                    found_keywords.append((keyword, file_name))
                    break
    results.extend(found_keywords)

# Функція для обробки списку файлів у потоці
def process_files(files, keywords, results):
    for file_path in files:
        search_keywords_in_file(file_path, keywords, results)

def main():
    # Задані ключові слова для пошуку
    keywords = ['keyword1', 'keyword2', 'keyword3']
    # Список файлів для обробки
    files = ['file1.txt', 'file2.txt', 'file3.txt']  # Потрібно вказати реальні шляхи до файлів

    # Розділити список файлів між потоками
    num_threads = min(len(files), os.cpu_count())  # Використовуємо максимальну кількість доступних ядер
    files_per_thread = len(files) // num_threads
    thread_chunks = [files[i:i+files_per_thread] for i in range(0, len(files), files_per_thread)]

    # Створити потоки для обробки файлів
    threads = []
    results = []
    for chunk in thread_chunks:
        thread = threading.Thread(target=process_files, args=(chunk, keywords, results))
        threads.append(thread)
        thread.start()

    # Почекати завершення всіх потоків
    for thread in threads:
        thread.join()

    # Вивести результати пошуку
    for keyword, file_name in results:
        print(f"Keyword '{keyword}' found in file '{file_name}'")

if __name__ == "__main__":
    main()
