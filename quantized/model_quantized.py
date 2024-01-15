from llama_cpp import Llama
import time
from datetime import datetime

from messages_type import Messages

def model_quantized_query(messages: Messages, modelPath: str = '.', modelType: str = 'llama-2-7b-chat'):
  if(modelType == 'llama-2-7b-chat'):
    modelPath = f"{modelPath}/llama-2-7b-chat.Q4_K_M.gguf"
  elif(modelType == 'tinyllama-1-1b-chat'):
    modelPath = f"{modelPath}/tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf"
  
  # https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama
  llm = Llama(
    model_path=modelPath,
    chat_format="llama-2", 
    n_ctx=1024,
    n_threads=8,
    n_gpu_layers=23, # This is the number of layers that will be run on GPU. The rest will be run on CPU. Tested to work on RTX 3050 with 4GB VRAM (Laptop)
  )  

  # Set chat_format according to the model you are using
  start_time = time.time() 
  start_time_local = datetime.fromtimestamp(start_time).strftime('%Y-%m-%d %H:%M:%S')
  print(f"Start time (local): {start_time_local}")
  
  # Convert messages to a list of dictionaries
  messages_dict_list = [message.dict() for message in messages.messages]

  print(f'Chat Completion API input - {messages_dict_list}')
  
  output = llm.create_chat_completion(
    # messages = [
    #     {"role": "system", "content": "You are a story writing assistant."},
    #     {
    #         "role": "user",
    #         "content": "Write a story of exactly 1 chapter of 500 words about a super hero with crystal powers. \
    #                     Also provide an image prompt for the chapter prefixed with 'image:'"
    #     }
    # ],
    messages = messages_dict_list,
    temperature=0.5,
  )

  print(f'Chat Completion API output - {output}')
  end_time = time.time() 
  end_time_local = datetime.fromtimestamp(end_time).strftime('%Y-%m-%d %H:%M:%S')
  print(f"End time: {end_time_local}")
  total_time_seconds = (end_time - start_time)
  print(f"Total time: {total_time_seconds} seconds")
  return output