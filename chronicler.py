from transformers import pipeline

combined_text = "LLM (Large Language Models) are powerful artificial intelligence models designed to process and generate human language. These models are trained on vast amounts of text data, allowing them to effectively understand context and perform a variety of tasks, such as text translation, summarization, answering questions, and content creation. LLMs use neural network architectures, particularly transformers, which help process information and generate text that closely resembles human language. One of the key features of these models is their ability to work with context and generate meaningful, coherent responses. Popular examples of LLMs include OpenAI's GPT-3 and GPT-4, Google's BERT, and others. These technologies are widely used in chatbots, content creation, customer support, programming assistance, and many other fields."


class Summarizer:
    def __init__(self):
        print('Start initialization model')
        self.llm_summarizer = pipeline("summarization", model="t5-3b")  # Инициализация локальной модели
        print('Initialization done!')

    def summarize(self):
        print('Start summarize!')
        summary = self.llm_summarizer(combined_text, max_length=100, min_length=30, do_sample=False)
        print('Summarize done!')
        # Сохраняем результат анализа
        summary_text = summary[0]['summary_text']
        print(f"Краткое описание контента: {summary_text}")


# Запуск основного кода
if __name__ == "__main__":
    Summarizer().summarize()
