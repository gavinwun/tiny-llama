
# Model details 

https://huggingface.co/TheBloke/Llama-2-7B-Chat-GGUF
```bash
pip3 install huggingface-hub
huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

https://huggingface.co/TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF
```bash
pip3 install huggingface-hub
huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir . --local-dir-use-symlinks False
```

llama cpp python docs - https://llama-cpp-python.readthedocs.io/en/latest/api-reference/#llama_cpp.Llama

# Usage

Modify model-quantized.py to the model you'd like to use, and tweak the settings to fit your GPU/CPU etc.

Then run directly 

```bash
cd quantized
python ./model-quantized.py
```