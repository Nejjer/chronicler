import time
import logging
from chronicler import write_story
from summarizer import summary_all
from transcribition import transcrib
from file_manager import FileManager

PROMPT_CHRONICLER_TEMPLATE = """Я играю в средневековую сборку модов в майнкрафт со своим другом. 
Ниже описания событий, которые с нами произошли.
Перескажи эти события так, как будто это летопись 845 года
Используй архаичный стиль. События должны быть представлены в хронологическом порядке.

Исходный текст:
{content}

Летописная запись:"""

MODEL_NAME = "qwen2.5:3b"  # Убедитесь, что модель скачана через ollama pull

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,  # Уровень логов
        format="%(asctime)s - %(levelname)s - %(message)s",  # Формат сообщения
    )
    logging.info("Start")

    start_time = time.time()  # Засекаем время начала

    file_manager = FileManager(audio_file="records/dialogue.wav")
    transcrib(file_manager=file_manager)
    file_manager.split_transcription_by_words()
    summary_all(file_manager, MODEL_NAME)
    write_story(file_manager, MODEL_NAME, PROMPT_CHRONICLER_TEMPLATE)

    end_time = time.time()  # Засекаем время окончания
    execution_time = end_time - start_time  # Вычисляем разницу
    logging.info(f"Executing time: {execution_time:.4f} seconds")

    input()
