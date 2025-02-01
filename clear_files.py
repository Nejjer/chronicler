import os


def delete_files_in_directories(directories):
    for directory in directories:
        if os.path.exists(directory) and os.path.isdir(directory):
            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                if os.path.isfile(file_path):
                    try:
                        # Удаляем файл
                        os.remove(file_path)
                        print(f"Удален файл: {file_path}")
                    except Exception as e:
                        print(f"Ошибка при удалении файла {file_path}: {e}")
        else:
            print(f"Папка не найдена или не является директорией: {directory}")


if __name__ == "__main__":
    directories_to_clear = ["summarizers", "transcripts", "transcripts_splits"]
    delete_files_in_directories(directories_to_clear)
