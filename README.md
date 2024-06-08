# MMUI_project
## The system is capable of
- Implement a Virtual Memo with speech and gesture (create a new memo).
- Catch the memo by the gesture
- Merge 2 memos using multimodality
- Merge 2 memos using only gesture
- Open the memo on a new window
- Templete evaluation survey: https://docs.google.com/forms/d/e/1FAIpQLScNHHTZhl1JdlbPnvrYLgjG7TIuZC6hA3dre9IEgac6i2ZWVQ/viewform?usp=sharing

How to add text:
- catch a memo
- say open
- say add
- speak content
- say stop
- say close

## Evaluation statistics about:
- response time of functions
- quality recognition of gesture and gesture
- better do the merge with the speech or catching 2 memos togheter
- preference between this Virtual Memo System or typing the letters on the keyboard by hand
- Using Usability Metric for User Experience (UMUX)

## Environment

Windows, Anaconda

### Create env:

`conda create --name mmui`

### Active:

`conda activate mmui`

### Pip list:

#### For speech2txt:

- Open Powershell as Administrator

- Install Chocolatey(if not exist):
`Set-ExecutionPolicy Bypass -Scope Process -Force; [System.Net.ServicePointManager]::SecurityProtocol = [System.Net.ServicePointManager]::SecurityProtocol -bor 3072; iex ((New-Object System.Net.WebClient).DownloadString('https://chocolatey.org/install.ps1'))`

- choco install git -y (if not exist)

- pip install --upgrade pip

- pip install --upgrade git+https://github.com/huggingface/transformers.git accelerate datasets[audio]

- pip install pyaudio

- pip install torchaudio

##### Install ffmpeg on windows:

- Install ffmpeg in mmui:
`choco install ffmpeg`

#### For gesture:

`pip3 install opencv-python numpy jupyter mediapipe`

## Run:

- Run speech2txt demo:

`python speech2txt/main.py`

- Run gesture demo:

`python gesture/main.py`
