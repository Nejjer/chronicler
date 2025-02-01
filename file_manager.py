import logging
import os
import math
from pathlib import Path
import re


class FileManager:
    _prefix = "./temp"
    _transcribition_file_path = f"{_prefix}/transcription.txt"
    _transcribition_parts_dir_path = f"{_prefix}/segments"
    _summarize_parts_dir_path = f"{_prefix}/summarize"
    _chronice_file = "./output/chronicle.txt"

    def _transcribition_part_file_path(self, part_id):
        return f"{self._transcribition_parts_dir_path}/part_{part_id}.txt"

    def _summarize_part_file_path(self, part_id):
        return f"{self._summarize_parts_dir_path}/part_{part_id}.txt"

    def _create_dirs(self):
        os.makedirs(self._prefix, exist_ok=True)
        os.makedirs("./output", exist_ok=True)
        os.makedirs(self._transcribition_parts_dir_path, exist_ok=True)
        os.makedirs(self._summarize_parts_dir_path, exist_ok=True)

    _speakers = {
        "SPEAKER_00": "Sinep",
        "SPEAKER_01": "Woofka1",
    }

    def __init__(self, audio_file="records/dialogue.wav", max_transcription_length=500):
        self.max_transcription_length = max_transcription_length
        self.audio_file = audio_file
        self._create_dirs()
        self._clear_all_files()

    def save_transcription(self, transcription_result):
        logging.info(
            f"Saving transcription result to file {self._transcribition_file_path}"
        )

        try:
            with open(self._transcribition_file_path, "w", encoding="utf-8") as f:
                for entry in transcription_result:
                    speaker_id = transcription_result[entry]["speaker"]
                    text = transcription_result[entry]["text"]

                    if len(text.strip()) == 0:
                        continue

                    cleaned_text = text.replace("  ", " ")
                    f.write(
                        f"{self._speakers.get(speaker_id, 'Unknown Speaker')}:{cleaned_text}\n"
                    )
            logging.info(
                f"Transcription result saved to file {self._transcribition_file_path}"
            )
        except Exception as e:
            logging.error(f"Failed to save transcription result: {e}")
            raise Exception(f"Failed to save transcription result: {e}")

    def split_transcription_by_words(self):
        """
        Разделяет файл на несколько частей так, чтобы в каждом было не больше заданного количества слов.

        :param filename: Имя исходного файла
        :param max_words: Максимальное количество слов в каждом новом файле
        :raises ValueError: Если файл не найден или пуст
        """
        if not os.path.exists(self._transcribition_file_path):
            raise ValueError(f"File '{self._transcribition_file_path}' not found.")

        # Чтение содержимого файла
        with open(self._transcribition_file_path, "r", encoding="utf-8") as file:
            content = file.read().strip()

        # Проверка на пустоту файла
        if not content:
            raise ValueError("File is empty.")

        # Разделяем текст на слова
        words = content.split()
        total_words = len(words)

        # Рассчитываем количество необходимых файлов
        num_files = math.ceil(total_words / self.max_transcription_length)

        logging.info(f"Will be created {num_files} file(s).")

        # Создание новых файлов с примерно одинаковым количеством слов
        for i in range(num_files):
            words_in_part = total_words // num_files
            start_idx = i * words_in_part
            end_idx = min((i + 1) * words_in_part, total_words)
            part_words = words[start_idx:end_idx]

            # Запись в новый файл
            part_filename = self._transcribition_part_file_path(i + 1)
            with open(part_filename, "w", encoding="utf-8") as part_file:
                part_file.write(" ".join(part_words))

            logging.info(f"File created: {part_filename} ({len(part_words)} wors)")

    def get_all_splited_transcriptions(self):
        return Path(self._transcribition_parts_dir_path).glob("*.txt")

    def get_all_summaries(self):
        file_pattern = re.compile(r"part_(\d+)\.txt")

        sorted_files = sorted(
            Path(self._summarize_parts_dir_path).glob("*.txt"),
            key=lambda f: int(file_pattern.search(f.name).group(1))
            if file_pattern.search(f.name)
            else float("inf"),
        )
        return sorted_files

    def save_summatize(self, summary_text, part_id):
        # Сохранение сводки в файл
        summary_filename = self._summarize_part_file_path(part_id=part_id)
        with open(summary_filename, "w", encoding="utf-8") as summary_file:
            summary_file.write(summary_text)

    def save_chronicle(self, chro_text):
        # Сохранение хроники в файл
        chro_filename = self._chronice_file
        with open(chro_filename, "w", encoding="utf-8") as chro_file:
            chro_file.write(chro_text)

    def _clear_all_files(self):
        logging.info("Clearing all files...")
        if os.path.exists(self._prefix) and os.path.isdir(self._prefix):
            for filename in os.listdir(self._prefix):
                file_path = os.path.join(self._prefix, filename)
                if os.path.isfile(file_path):
                    try:
                        # Удаляем файл
                        os.remove(file_path)
                        logging.info(f"File deleted: {file_path}")
                    except Exception as e:
                        logging.error(f"Error deleting file {file_path}: {e}")
        else:
            logging.error(f"Not found directory for clearing files: {self._prefix}")
