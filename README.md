# tiny-llama

Repo used to setup tiny-llama - Credits to https://towardsdatascience.com/deploy-tiny-llama-on-aws-ec2-f3ff312c896d

# Environment Setup

* Install Anaconda (recommended) - https://www.anaconda.com/
    * Setup conda evironment 
    ```bash
    conda create -n tiny-llama 
    conda activate tiny-llamas
    conda install python=3.10.13
    conda install conda-forge::rust
    python -m pip install --upgrade pip
    ```
* Setup repo
    ```bash
    pip install -r requirements.txt
    ```
* Run the script
    ```bash
    # An URL will show in the terminal  e.g. http://127.0.0.1:8000
    uvicorn main:app --reload
    ```
* Open browser and browse to the url e.g. http://127.0.0.1/docs

    
