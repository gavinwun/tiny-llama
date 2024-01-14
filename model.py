# Install transformers from source - only needed for versions <= v4.34
# pip install git+https://github.com/huggingface/transformers.git
# pip install accelerate

from messages_type import Messages
import torch
from transformers import pipeline



def model_query(messages: Messages):
    pipe = pipeline(
        "text-generation",
        model="TinyLlama/TinyLlama-1.1B-Chat-v1.0",
        torch_dtype=torch.bfloat16,
        # Use "cuda" to run on GPU 
        device_map="cpu", 
    )
    
    print(f'CUDA is available = {torch.cuda.is_available()}')

    # We use the tokenizer's chat template to format each message - see https://huggingface.co/docs/transformers/main/en/chat_templating
    # messages = [
    #     {
    #         "role": "system",
    #         "content": "You are a friendly chatbot who always funny and interesting. You only reply with the actual answer without repeating my question.",
    #     },
    #     {"role": "user", "content": f"{query}"},
    # ]
    prompt = pipe.tokenizer.apply_chat_template(
        messages, tokenize=False, add_generation_prompt=True
    )
    outputs = pipe(
        prompt,
        max_new_tokens=4096,
        do_sample=True,
        temperature=0.7,
        top_k=50,
        top_p=0.95,
    )


    output = outputs[0]["generated_text"]
    return output


if __name__ == "__main__":
    print(model_query("tell me a joke about politicians"))