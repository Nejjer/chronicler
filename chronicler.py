import re
from datetime import datetime
from pathlib import Path

import ollama

# Конфигурация
MODEL_NAME = "qwen2.5:14b"
SUMMARIES_DIR = Path("summarizers")
OUTPUT_FILE = Path("chronicles.md")
PROMPT_TEMPLATE = """Я играю в средневековую сборку модов в майнкрафт со своим другом. 
Ниже описания событий, которые с нами произошли.
Перескажи эти события так, как будто это летопись 845 года
Используй архаичный стиль. События должны быть представлены в хронологическом порядке.

Исходный текст:
{content}

Летописная запись:"""


# Функция генерации летописи
def generate_chronicle(text: str) -> str:
    try:
        response = ollama.generate(
            model=MODEL_NAME,
            prompt=PROMPT_TEMPLATE.format(content=text),
            options={'temperature': 0.8, 'num_predict': 2048}
        )
        return response['response']
    except Exception as e:
        return f"## Ошибка генерации\n```\n{str(e)}\n```"


# Регулярное выражение для извлечения номера части файла
file_pattern = re.compile(r"part_(\d+)_analysis\.txt")

# Сортировка файлов по номерам частей
sorted_files = sorted(
    SUMMARIES_DIR.glob("*_analysis.txt"),
    key=lambda f: int(file_pattern.search(f.name).group(1)) if file_pattern.search(f.name) else float('inf'))


# Собираем все записи
def write_story():
    chronicles = []
    for summary_file in sorted_files:
        try:
            # Чтение файла
            content = summary_file.read_text(encoding="utf-8")

            # Генерация
            entry = generate_chronicle(content)

            # Форматирование записи
            chronicles.append(
                f"{entry}\n\n"
                f"---\n"
            )
            print(f"Обработано: {summary_file.name}")

        except Exception as e:
            print(f"Ошибка при обработке {summary_file.name}: {str(e)}")

    # Создаем итоговый документ
    header = f"""# Хроники Minecraft-событий\n
    **Дата составления:** {datetime.now().strftime("%Y-%m-%d %H:%M")}\n
    **Всего записей:** {len(chronicles)}\n\n
    """

    OUTPUT_FILE.write_text(
        header + "\n".join(chronicles),
        encoding="utf-8"
    )

    print(f"Готово! Результаты сохранены в {OUTPUT_FILE}")


if __name__ == "__main__":
    write_story()
