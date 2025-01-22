import os
import time

import torch
import whisper
from pyannote.audio import Pipeline
import sounddevice as sd
import wave
from datetime import datetime

auth_token = os.getenv('AUTH_TOKEN')



speakers = {
    'SPEAKER_00': 'Sinep',
    'SPEAKER_01': 'Woofka1',
}

from listener_utils import words_per_segment


# Параметры записи аудио
def record_audio(output_file, duration=2, sample_rate=16000, channels=1):
    """
    Записывает аудио с микрофона и сохраняет его в указанный файл.
    """
    print("Начало записи...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=channels, dtype='int16')
    sd.wait()  # Ожидание завершения записи

    # Сохранение аудио в файл
    with wave.open(output_file, 'wb') as wf:
        wf.setnchannels(channels)
        wf.setsampwidth(2)  # 2 байта на выборку
        wf.setframerate(sample_rate)
        wf.writeframes(audio.tobytes())
    print(f"Запись завершена. Файл сохранен как {output_file}")


# Функция распознавания речи с помощью Whisper
def transcribe_audio(whisper_model, audio_file):
    """
    Распознает текст из аудио файла с использованием Whisper.
    """
    model = whisper.load_model(whisper_model)
    print("Начинается распознавание речи...")
    result = model.transcribe(audio_file)
    print("Распознавание завершено.")
    return result['text']


# Функция для выполнения диаризации (разделение по участникам)
def diarize_audio(audio_file, pyannote_pipeline):
    """
    Выполняет диаризацию аудио с использованием Pyannote.
    """
    print("Начинается диаризация...")
    diarization = pyannote_pipeline(audio_file)
    print("Диаризация завершена.")
    return diarization


# Сохранение текста в формате Markdown
def save_transcription_to_md(final_result, output_file):
    """
    Сохраняет текстовое содержание в формате Markdown.
    """
    print("Сохранение результата в Markdown файл...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Расшифровка диалога\n\n")
        for entry in final_result:
            speaker = final_result[entry]['speaker']
            text = final_result[entry]['text']
            if len(text) == 0:
                continue
            text = text.replace("  ", " ")
            start_time = final_result[entry]['start']
            end_time = final_result[entry]['end']
            f.write(f"{speakers[speaker]}:{text}\n\n")
    print(f"Результат сохранен в файл {output_file}")

def my_save_transcription_to_md(transcription, diarization, output_file):
    """
    Сохраняет текстовое содержание в формате Markdown.
    """
    print("Сохранение результата в Markdown файл...")
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(f"# Расшифровка диалога\n\n")
        for segment, speaker in zip(diarization.itertracks(yield_label=True), transcription.split('\n')):
            start_time = segment[0].start
            end_time = segment[0].end
            speaker_label = speaker[1]
            f.write(f"{speaker_label}: {speaker}\n\n")
    print(f"Результат сохранен в файл {output_file}")

def main():
    # Задаем параметры
    audio_file = "dialogue.wav"
    whisper_model_type = "turbo"  # Или другой тип модели Whisper
    output_md_file = "transcription1.md"

    # Убедитесь, что вы настроили Pyannote pipeline (нужен токен доступа)
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=auth_token)
    pipeline.to(torch.device("cuda"))
    # Записываем аудио
    #record_audio(audio_file, duration=20)  # Запись 2 секунд

    print('Загружаем модель для распознавания текста')
    model = whisper.load_model(whisper_model_type)
    print('Диарилизуем аудио')
    diarization_result = pipeline(audio_file)
    print('Преобразуем аудио в текст')
    transcription_result = model.transcribe(audio_file, word_timestamps=True)

    final_result = words_per_segment(transcription_result, diarization_result)


    # # Распознаем текст из аудио
    # transcription = transcribe_audio(whisper_model_type, audio_file)
    #
    # # Выполняем диаризацию
    # diarization_result = diarize_audio(audio_file, pipeline)
    #
    # # Сохраняем результат в Markdown
    # my_save_transcription_to_md(transcription, diarization_result, output_md_file)

    print('Сохраняем результат в Markdown')
    save_transcription_to_md(final_result, output_md_file)

if __name__ == "__main__":
    start_time = time.time()  # Засекаем время начала
    main()
    end_time = time.time()  # Засекаем время окончания
    execution_time = end_time - start_time  # Вычисляем разницу
    print(f"Время выполнения скрипта: {execution_time:.4f} секунд")
