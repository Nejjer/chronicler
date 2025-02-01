import re


def split_md_file(file_path, output_dir='transcripts_splits/', max_words=500):
    print('Разделяем файл на равные части')
    # Чтение содержимого файла
    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    # Разделение содержимого на слова с сохранением переносов строк
    words = re.findall(r'\S+\s*', content)

    # Разделение слов на части по max_words слов в каждой
    for i in range(0, len(words), max_words):
        chunk = words[i:i + max_words]
        chunk_text = ''.join(chunk)

        # Сохранение каждой части в отдельный файл
        output_file_path = f"{output_dir}part_{i // max_words + 1}.md"
        with open(output_file_path, 'w', encoding='utf-8') as output_file:
            output_file.write(chunk_text)

        print(f"Создан файл: {output_file_path}")


# Пример использования
if __name__ == "__main__":
    split_md_file('transcripts/transcription.md')
