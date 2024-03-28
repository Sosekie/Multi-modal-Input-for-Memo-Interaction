# MMUI_project

## Environment

### Create env:

`conda create --name mmui`

### Active:

`conda activate mmui`

### Pip list:

#### For speech2txt:

1. pip install --upgrade pip

2. pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]

3. pip install pyaudio

if ffmpeg does not exist:



#### For gesture:

`pip3 install opencv-python numpy jupyter mediapipe`

## Run:

Run speech2txt demo:

`python speech2txt/main.py`

Run gesture demo:

`python gesture/main.py`