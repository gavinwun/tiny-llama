# To run script below - 
# follow instructions at https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
# or https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF

from llama_cpp import Llama
import time
from datetime import datetime

# https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama
llm = Llama(
  # model_path="./tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf", 
  model_path="./llama-2-7b-chat.Q4_K_M.gguf", 
  chat_format="llama-2", 
  n_ctx=1024,
  n_threads=8,
  n_gpu_layers=23, # This is the number of layers that will be run on GPU. The rest will be run on CPU. Tested to work on RTX 3050 with 4GB VRAM (Laptop)
)  

# Set chat_format according to the model you are using
start_time = time.time() 
start_time_local = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
print(f"Start time (local): {start_time_local}")
outputs = llm.create_chat_completion(
  messages = [
      {"role": "system", "content": "You are a story writing assistant."},
      {
          "role": "user",
          "content": "Write a story of exactly 1 chapter of 500 words about a super hero with crystal powers. \
                      Also provide an image prompt for the chapter prefixed with 'image:'"
      }
  ],
  temperature=0.5,
)

print(f'Chat Completion API outputs - {outputs}')
end_time = time.time() 
end_time_local = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
print(f"End time: {end_time_local}")
total_time_seconds = (end_time - start_time)
print(f"Total time: {total_time_seconds} seconds")
