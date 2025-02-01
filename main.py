import time

from chronicler import write_story
from clear_files import delete_files_in_directories
from split_to_files import split_md_file
from summarizer import summary_all_files
from transcribition import transcrib

if __name__ == "__main__":
    print('Чистим все старые обработки')
    directories_to_clear = ["summarizers", "transcripts", "transcripts_splits"]
    delete_files_in_directories(directories_to_clear)
    # print('Останаливаем олламу, чтобы освободить память')

    start_time = time.time()  # Засекаем время начала
    print('Транскрибируем аудио')
    transcrib(audio_file='records/Untitled.wav')
    print('Разбиваем файлы на части')
    split_md_file('transcripts/transcription.md')
    print('Суммаризируем транскрибицию')
    summary_all_files()
    print('Пишем летопись')
    write_story()
    end_time = time.time()  # Засекаем время окончания
    execution_time = end_time - start_time  # Вычисляем разницу
    print(f"Время выполнения скрипта: {execution_time:.4f} секунд")
    input()
