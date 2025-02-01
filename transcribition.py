import gc
import os
import logging
from listener_utils import words_per_segment

import torch
import whisper
from dotenv import load_dotenv
from pyannote.audio import Pipeline
from file_manager import FileManager

load_dotenv()

auth_token = os.getenv("AUTH_TOKEN")


def clear_gpu_memory(model):
    # Удаляем модель
    del model

    # Очищаем кеш CUDA
    if torch.cuda.is_available():
        torch.cuda.empty_cache()

    # Вызываем сборщик мусора
    gc.collect()


def transcrib(file_manager: FileManager, whisper_model_type="turbo"):
    logging.info("Load model for diarization")
    pipeline = Pipeline.from_pretrained(
        "pyannote/speaker-diarization-3.1", use_auth_token=auth_token
    )
    pipeline.to(torch.device("cuda"))

    logging.info("Load whisper")
    model = whisper.load_model(whisper_model_type)

    logging.info("Diadizating audio")
    diarization_result = pipeline(file_manager.audio_file)

    logging.info("Transcribition audio")
    transcription_result = model.transcribe(
        file_manager.audio_file, word_timestamps=True
    )

    logging.info("Clear GPU memory")
    clear_gpu_memory(model)

    final_result = words_per_segment(transcription_result, diarization_result)

    file_manager.save_transcription(final_result)


if __name__ == "__main__":
    transcrib(FileManager())
