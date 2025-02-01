import time
from file_manager import FileManager
import ollama
import logging


# Функция для генерации ответа через Ollama
def generate_summary(text: str, model_name: str) -> str:
    prompt = f"""Проанализируй приведенную в файле транскрипцию нашего разговора во время игры в Minecraft с модами.
Сначала выбери только те события, который относятся к игре в майнкрафт.
Потом определи участника или участников события
Среди оставшихся событий, сгруппируй некоторые из них при необходимости.
По возможности снабди события деталями из разговора
И выпиши события списком в виде:
[Никнейм] [описание действия в прошедшем времени]
Старайся учитывать, что мы используем модификации, поэтому учитывай упоминания механик и предметов, которых нет в стандартной версии Minecraft.  
В ОТВЕТ НАПИШИ ТОЛЬКО СОБЫТИЯ СПИСКОМ
**Примеры:**
*   Sinep открыл свое поселение, прочитав перед этим декларацию.
*   Woofka1 начал варить пиво в своем подвале.
*   Sinep и Woofka1 отправились в шахту на поиски редких руд.
    Транскрипция:
    {text}
"""

    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt,
            options={"temperature": 0.7, "num_predict": 1024},
        )
        return response["response"]
    except Exception as e:
        return f"Ошибка генерации: {str(e)}"


def summary_all(file_manager: FileManager, model_name: str):
    # Обработка файлов
    for transcript_file in file_manager.get_all_splited_transcriptions():
        try:
            # Чтение файла
            content = transcript_file.read_text(encoding="utf-8")

            # Генерация анализа
            start_time = time.time()
            summary = generate_summary(content, model_name)
            generation_time = time.time() - start_time

            # Сохранение результата
            file_manager.save_summatize(
                summary_text=summary, part_id=transcript_file.stem
            )

            logging.info(
                f"Summarized {transcript_file.name} for {generation_time:.2f}с"
            )

        except Exception as e:
            logging.info(f"Summarize error {transcript_file.name}: {str(e)}")

    logging.info("Summarize done!")


if __name__ == "__main__":
    summary_all(FileManager())
