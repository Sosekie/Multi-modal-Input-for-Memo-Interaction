# MMUI_project

## Next steps:

Priority:
1) Implement Merge speech recognition, speech trigger.
2) Implement a Virtual Memo from the Speech (create a new memo).
3) Catch the memo by the gesture 
4) Upgrading the speech part for the Merge (merge the red one, or the green) (merge the red one on the green one)

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