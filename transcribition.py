import gc
import os

import torch
import whisper
from dotenv import load_dotenv
from pyannote.audio import Pipeline

load_dotenv()

auth_token = os.getenv('AUTH_TOKEN')

speakers = {
    'SPEAKER_00': 'Sinep',
    'SPEAKER_01': 'Woofka1',
}

from listener_utils import words_per_segment


# Сохранение текста в формате Markdown
def save_transcription_to_md(final_result, output_file):
    """
    Сохраняет текстовое содержание в формате Markdown.
    """
    print("Сохранение результата в Markdown файл...")
    with open(output_file, 'w', encoding='utf-8') as f:
        for entry in final_result:
            speaker = final_result[entry]['speaker']
            text = final_result[entry]['text']
            if len(text) == 0:
                continue
            text = text.replace("  ", " ")
            f.write(f"{speakers[speaker]}:{text}\n")
    print(f"Результат сохранен в файл {output_file}")


def clear_gpu_memory(model):
    # Удаляем модель
    del model

    # Очищаем кеш CUDA
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Вызываем сборщик мусора
    gc.collect()


def transcrib(audio_file='records/dialogue.wav', whisper_model_type='turbo',
              output_md_file='transcripts/transcription.md'):
    print('Загружаем модель для диарилизации')
    pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=auth_token)
    pipeline.to(torch.device("cuda"))

    print('Загружаем модель для распознавания текста')
    model = whisper.load_model(whisper_model_type)
    print('Диарилизуем аудио')
    diarization_result = pipeline(audio_file)
    print('Преобразуем аудио в текст')
    transcription_result = model.transcribe(audio_file, word_timestamps=True)
    print('Очищаем память ГПУ')
    clear_gpu_memory(model)
    final_result = words_per_segment(transcription_result, diarization_result)

    print('Сохраняем результат в Markdown')
    save_transcription_to_md(final_result, output_md_file)


if __name__ == "__main__":
    transcrib()
