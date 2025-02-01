import time
from pathlib import Path

import ollama

# Конфигурация
MODEL_NAME = "qwen2.5:14b"  # Убедитесь, что модель скачана через ollama pull
TRANSCRIPTS_DIR = Path("transcripts_splits")
SUMMARIES_DIR = Path("summarizers")

# Создаем выходную директорию
SUMMARIES_DIR.mkdir(exist_ok=True)


# Функция для генерации ответа через Ollama
def generate_summary(text: str) -> str:
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
            model=MODEL_NAME,
            prompt=prompt,
            options={
                'temperature': 0.7,
                'num_predict': 1024
            }
        )
        return response['response']
    except Exception as e:
        return f"Ошибка генерации: {str(e)}"


def summary_all_files():
    # Обработка файлов
    for transcript_file in TRANSCRIPTS_DIR.glob("*.md"):
        try:
            # Чтение файла
            content = transcript_file.read_text(encoding="utf-8")

            # Генерация анализа
            start_time = time.time()
            summary = generate_summary(content)
            generation_time = time.time() - start_time

            # Сохранение результата
            output_file = SUMMARIES_DIR / f"{transcript_file.stem}_analysis.txt"
            output_file.write_text(summary, encoding="utf-8")

            print(f"Обработан {transcript_file.name} за {generation_time:.2f}с")

        except Exception as e:
            print(f"Ошибка обработки {transcript_file.name}: {str(e)}")

    print("Суммаризация завершена!")


if __name__ == "__main__":
    summary_all_files()
