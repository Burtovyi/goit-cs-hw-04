import os
import multiprocessing

def process_file(filename, keywords, output_queue):
    results = {}
    try:
        with open(filename, 'r') as file:
            text = file.read()
            for keyword in keywords:
                count = text.count(keyword)
                if count > 0:
                    results[keyword] = count
    except IOError as e:
        print(f"Помилка при читанні файлу {filename}: {e}")
    except Exception as e:
        print(f"Непередбачена помилка при обробці файлу {filename}: {e}")
    finally:
        output_queue.put(results)

def main():
    folder_path = 'text_files'
    
    try:
        # Перевірка наявності папки
        if not os.path.isdir(folder_path):
            raise FileNotFoundError(f"Папка '{folder_path}' не існує")
        
        files = [os.path.join(folder_path, f) for f in os.listdir(folder_path) if os.path.isfile(os.path.join(folder_path, f))]
        
        keywords = ['keyword1', 'keyword2', 'keyword3']
        
        output_queue = multiprocessing.Queue()
        
        num_processes = multiprocessing.cpu_count()
        
        files_per_process = len(files) // num_processes
        
        processes = []
        for i in range(num_processes):
            start_index = i * files_per_process
            end_index = (i + 1) * files_per_process if i < num_processes - 1 else len(files)
            process_files = files[start_index:end_index]
            process = multiprocessing.Process(target=process_file, args=(process_files, keywords, output_queue))
            processes.append(process)
            process.start()
        
        total_results = {}
        for _ in range(num_processes):
            total_results.update(output_queue.get())
        
        for process in processes:
            process.join()
        
        print("Результати пошуку:")
        for keyword, count in total_results.items():
            print(f"{keyword}: {count}")
    except FileNotFoundError as e:
        print(f"Помилка: {e}")
    except Exception as e:
        print(f"Непередбачена помилка: {e}")

if __name__ == "__main__":
    main()
