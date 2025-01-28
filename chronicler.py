import torch
from transformers import pipeline



def summarize_minecraft_content(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    pipe = pipeline(
        "text-generation",
        model="google/gemma-2-9b-it",
        model_kwargs={"torch_dtype": torch.bfloat16},
        device="cuda",  # replace with "mps" to run on a Mac device
    )

    prompt = (
            "Summarize the following text, focusing only on information related to Minecraft with mods: "
            + text
    )

    messages = [{"role": "user", "content": prompt}]


    outputs = pipe(messages, max_new_tokens=512)
    assistant_response = outputs[0]["generated_text"][-1]["content"].strip()
    print(assistant_response)




# Example usage






summarize_minecraft_content("./transcripts/transcription.md")
