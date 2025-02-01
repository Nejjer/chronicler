from datetime import datetime
from file_manager import FileManager
import ollama
import logging
# Конфигурация


# Функция генерации летописи
def generate_chronicle(text: str, model_name, prompt_template) -> str:
    try:
        response = ollama.generate(
            model=model_name,
            prompt=prompt_template.format(content=text),
            options={"temperature": 0.8, "num_predict": 2048},
        )
        return response["response"]
    except Exception as e:
        return f"## Ошибка генерации\n```\n{str(e)}\n```"


# Собираем все записи
def write_story(file_manager: FileManager, model_name, prompt_template):
    chronicles = []
    for summary_file in file_manager.get_all_summaries():
        try:
            # Чтение файла
            content = summary_file.read_text(encoding="utf-8")

            # Генерация
            entry = generate_chronicle(content, model_name, prompt_template)

            # Форматирование записи
            chronicles.append(f"{entry}\n\n---\n")
            logging.info(f"Wrote for: {summary_file.name}")

        except Exception as e:
            logging.error(f"Error with {summary_file.name}: {str(e)}")

    # Создаем итоговый документ
    header = f"""# Хроники Minecraft-событий\n
    **Всего записей:** {len(chronicles)}\n\n
    """
    file_manager.save_chronicle(header + "\n".join(chronicles))

    logging.info("Done")


if __name__ == "__main__":
    write_story()
