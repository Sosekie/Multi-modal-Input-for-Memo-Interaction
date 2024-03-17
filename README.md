# MMUI_project

## Environment

### Choosing Linux:

Using WSL and Ubuntu is a good choice.\
How to set up WSL: https://learn.microsoft.com/en-us/windows/wsl/install
\
How to set up Ubuntu: https://maurogiusti.medium.com/running-ubuntu-on-windows-10-with-wsl2-c4f06b3c353

### Create env:

`conda create --name mmui`

### Active:

`conda activate mmui`

### Pip list:

#### For speech2txt:

`pip install --upgrade pip`

`pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]`

if ffmpeg does not exist:

`sudo apt update`

`sudo apt install ffmpeg`

and verifiy installation:

`ffmpeg -version`

## Run:

Run speech2txt demo:

`python speech2txt/main.py`