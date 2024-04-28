import os
import multiprocessing

def process_file(filename, keywords, output_queue):
    results = {}
    with open(filename, 'r') as file:
        text = file.read()
        for keyword in keywords:
            count = text.count(keyword)
            if count > 0:
                results[keyword] = count
    output_queue.put(results)

def main():
    # Папка з текстовими файлами
    folder_path = 'text_files'
    
    # Список файлів у папці
    files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
    
    # Ключові слова для пошуку
    keywords = ['keyword1', 'keyword2', 'keyword3']
    
    # Створення черги для обміну даними
    output_queue = multiprocessing.Queue()
    
    # Кількість процесів, що будуть створені
    num_processes = multiprocessing.cpu_count()
    
    # Розділення списку файлів між процесами
    files_per_process = len(files) // num_processes
    
    # Створення та запуск процесів
    processes = []
    for i in range(num_processes):
        start_index = i * files_per_process
        end_index = (i + 1) * files_per_process if i < num_processes - 1 else len(files)
        process_files = files[start_index:end_index]
        process = multiprocessing.Process(target=process_file, args=(process_files, keywords, output_queue))
        processes.append(process)
        process.start()
    
    # Збір результатів
    total_results = {}
    for _ in range(num_processes):
        total_results.update(output_queue.get())
    
    # Очікування завершення всіх процесів
    for process in processes:
        process.join()
    
    # Виведення результатів
    print("Результати пошуку:")
    for keyword, count in total_results.items():
        print(f"{keyword}: {count}")

if __name__ == "__main__":
    main()
