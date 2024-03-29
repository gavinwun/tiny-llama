# tiny-llama

Repo used to setup tiny-llama - Credits to https://towardsdatascience.com/deploy-tiny-llama-on-aws-ec2-f3ff312c896d

# Environment Setup

Note: setup is just specific to the version I was using at the time of writing, feel free to update and change as required.

Using Windows 11 and development with VSCode. All commands were performed using WSL2 terminal with Ubuntu 22.04 distro.

* CUDA Toolkit Install (handy for any packages and wants to build with it)
    ```bash
    sudo apt install build-essential
    # https://developer.nvidia.com/cuda-11-8-0-download-archive?target_os=Linux&target_arch=x86_64&Distribution=WSL-Ubuntu&target_version=2.0&target_type=deb_local
    wget https://developer.download.nvidia.com/compute/cuda/repos/wsl-ubuntu/x86_64/cuda-wsl-ubuntu.pin
    sudo mv cuda-wsl-ubuntu.pin /etc/apt/preferences.d/cuda-repository-pin-600
    wget https://developer.download.nvidia.com/compute/cuda/11.8.0/local_installers/cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
    sudo dpkg -i cuda-repo-wsl-ubuntu-11-8-local_11.8.0-1_amd64.deb
    sudo cp /var/cuda-repo-wsl-ubuntu-11-8-local/cuda-*-keyring.gpg /usr/share/keyrings/
    sudo apt-get update
    sudo apt-get -y install cuda

    # Setup paths
    echo 'export PATH=/usr/local/cuda-11.8/bin:$PATH' >> ~/.bashrc
    echo 'export LD_LIBRARY_PATH=/usr/local/cuda-11.8/lib64:$LD_LIBRARY_PATH' >> ~/.bashrc
    source ~/.bashrc
    sudo ldconfig
    ```
* Install Miniconda - https://kontext.tech/article/1064/install-miniconda-and-anaconda-on-wsl-2-or-linux
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
    # Install torch with cuda support if supported
    pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu118
    # Install other required packages
    pip install -r requirements.txt # NOTE - see CUDA section if you want to use that instead of CPU
    ```
* Download quantized models (optional)
    * if you want to test the quantized models (later you can post via REST API by POST to /query/quantized)
    ```bash
    pip3 install huggingface-hub
    huggingface-cli download TheBloke/Llama-2-7b-Chat-GGUF llama-2-7b-chat.Q4_K_M.gguf --local-dir ./quantized --local-dir-use-symlinks False
    huggingface-cli download TheBloke/TinyLlama-1.1B-Chat-v1.0-GGUF tinyllama-1.1b-chat-v1.0.Q4_K_M.gguf --local-dir ./quantized --local-dir-use-symlinks False
    ```
* Run the script
    ```bash
    # Check model.py to set to use cuda or cpu, max_tokens etc as required
    # An URL will show in the terminal  e.g. http://127.0.0.1:8000 
    uvicorn main:app --reload
    ```
* Open browser and browse to the url e.g. http://127.0.0.1/docs
* Test the POST queries with below sample JSON
```json
{
  "messages": [
    {
      "role": "system",
      "content": "You are a story generator"
    },
{
      "role": "user",
      "content": "Create a story about super hero with thunder power, along with an image prompt prefixed with 'image prompt:'"
    }
  ],
  "api_key": "some_api_key_here_logic_etc"
}
```

# AWS Linux Instructions

Install packages
```bash
sudo yum update
sudo yum install git
sudo yum install nginx
sudo amazon-linux-extras install epel
sudo yum install certbot
sudo yum groupinstall "Development Tools"
sudo yum install gcc zlib-devel bzip2 bzip2-devel readline-devel sqlite sqlite-devel openssl-devel tk-devel libffi-devel xz-devel
curl https://pyenv.run | bash

# add below pyenv commands to ~/.bashrc as well
export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init -)"

pyenv install 3.10.13
pyenv global 3.10.13

curl -O https://bootstrap.pypa.io/get-pip.py
python3 get-pip.py --user
```

Create SSL Certs

Enter the command below (update domains as required)
```
sudo certbot certonly --manual --preferred-challenges=dns -d '*.yourdomain.com' -d 'yourdomain.com'

# Renews in the future - sudo certbot renew --dry-run
```

Setup Nginx

Enter the command below (update domain as required)
```bash
sudo vim /etc/nginx/conf.d/yourdomain.com.conf

# i to insert content, esc to go back to comand and :wq to save and quite (:qa! to quit without saving)
```
Enter the details below (update domain and filenames etc as required)
```
server {
    listen 443 ssl http2;
    listen [::]:443 ssl http2;

    server_name yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;

    # Recommended SSL settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers 'ECDHE-ECDSA-AES128-GCM-SHA256:ECDHE-RSA-AES128-GCM-SHA256:ECDHE-ECDSA-AES256-GCM-SHA384:ECDHE-RSA-AES256-GCM-SHA384:DHE-RSA-AES128-GCM-SHA256:DHE-RSA-AES256-GCM-SHA384';
    ssl_prefer_server_ciphers on;
    ssl_session_cache shared:SSL:10m;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_connect_timeout 60s;
        proxy_send_timeout 60s;
        proxy_read_timeout 180s;  # Set to 3 minutes (180 seconds)
    }
}

server {
    listen 80;
    listen [::]:80;
    server_name yourdomain.com;
    return 301 https://$server_name$request_uri;
}

```

Enable Nginx
```bash
sudo systemctl start nginx
sudo systemctl enable nginx
sudo systemctl status nginx
```

Setup Repo
```bash
mkdir /home/ec2-user/tmpdir # temp drive might be too small when using Amazon Linux, create a tmpdir instead and use that
git clone https://github.com/gavinwun/tiny-llama.git
cd tiny-llama

export TMPDIR='/home/ec2-user/tmpdir/'; python3 -m pip install -r requirements.txt # NOTE - see CUDA section if you want to use that instead of CPU
```

Launch Service
```bash
python3 -m uvicorn main:app # https://www.uvicorn.org/deployment/
```