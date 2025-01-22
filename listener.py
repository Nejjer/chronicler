import os

import sounddevice as sd
import numpy as np
import whisper
from pyannote.audio import Pipeline
from scipy.io.wavfile import write
import tempfile

auth_token = os.getenv('AUTH_TOKEN')

# Инициализация моделей
whisper_model = whisper.load_model("base")  # Выберите размер модели (base, small, medium, large)
diarization_pipeline = Pipeline.from_pretrained("pyannote/speaker-diarization", use_auth_token=auth_token)

# Параметры записи
SAMPLE_RATE = 16000
DURATION = 2  # Длительность записи в секундах
TEMP_DIR = tempfile.gettempdir()

from scipy.io.wavfile import write

def save_audio_segment(audio, sample_rate, start, end, output_path):
    """Сохраняет сегмент аудио в WAV-файл."""
    # Вычисляем начало и конец сегмента в выборках
    start_sample = int(start * sample_rate)
    end_sample = int(end * sample_rate)
    # Извлекаем сегмент и сохраняем в WAV
    segment = audio[start_sample:end_sample]
    segment = (segment * 32767).astype(np.int16)  # Преобразование в 16-битный формат
    write(output_path, sample_rate, segment)

def record_audio(duration, sample_rate):
    """Записывает аудио с микрофона."""
    print("Начало записи...")
    audio = sd.rec(int(duration * sample_rate), samplerate=sample_rate, channels=1, dtype='int16')
    sd.wait()  # Ожидание окончания записи
    print("Запись завершена.")
    return audio

def save_wav(audio, sample_rate, filename):
    """Сохраняет аудио в WAV-файл."""
    write(filename, sample_rate, audio)

def diarize_audio(filename):
    """Выполняет идентификацию говорящих."""
    diarization = diarization_pipeline({"uri": "recording", "audio": filename})
    return diarization

def transcribe_segment(audio_path, segment, model):
    """Расшифровывает сегмент речи."""
    # Обрезка аудио по временным рамкам сегмента
    start_time = segment["start"]
    end_time = segment["end"]
    result = model.transcribe(audio_path, initial_prompt="", verbose=False, word_timestamps=True,
                              condition_on_previous_text=False, suppress_tokens=[])
    return start_time, end_time, result["text"]

# Основной процесс
def main():
    # 1. Записываем звук
    audio_data = record_audio(DURATION, SAMPLE_RATE)

    # 2. Сохраняем результат в WAV-файл
    temp_audio_path = f"{TEMP_DIR}/recording.wav"
    save_wav(audio_data, SAMPLE_RATE, temp_audio_path)

    # 3. Идентификация говорящих
    diarization_result = diarize_audio(temp_audio_path)
    print("Идентификация говорящих завершена.")

    transcripts = []
    for segment in diarization_result.itertracks(yield_label=True):
        start, end = segment[0].start, segment[0].end
        speaker = segment[2]  # Метка говорящего
        print(f"Распознавание речи для сегмента: {start:.2f}-{end:.2f}, Говорящий: {speaker}")

        # Сохраняем сегмент в WAV-файл
        audio_segment_path = f"{TEMP_DIR}/segment_{start:.2f}_{end:.2f}.wav"
        save_audio_segment(audio_data, SAMPLE_RATE, start, end, audio_segment_path)

        # Расшифровка сегмента
        _, _, transcript = transcribe_segment(audio_segment_path, segment[0], whisper_model)
        transcripts.append(f"[{speaker}] {transcript}")

    # 5. Вывод текста
    print("\nРезультаты распознавания:")
    for line in transcripts:
        print(line)

    # 6. Сохранение результатов в файл
    with open("dialogue_transcripts.md", "w", encoding="utf-8") as f:
        f.write("# Диалоговая летопись\n\n")
        for line in transcripts:
            f.write(f"{line}\n")
    print("Результаты сохранены в dialogue_transcripts.md")

if __name__ == "__main__":
    try:
        main()
    except Exception as err:
        print(err)
        lol = input()
