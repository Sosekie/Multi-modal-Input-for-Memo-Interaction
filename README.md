# MMUI_project

## Environment
### Create env:
Using WSL and Ubuntu is a good choice.
`conda create --name mmui`
### Active:
`conda activate mmui`
### Pip list:
#### For speech2txt:
`pip install --upgrade pip`
`pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]`
if GPU allowed:
`pip install flash-attn --no-build-isolation`
else:
`pip install --upgrade optimum`
if ffmpeg does not exist:
`sudo apt update`
`sudo apt install ffmpeg`
and verifiy installation:
`ffmpeg -version`
### Run:
Run speech2txt demo:
`python speech2txt/main.py`