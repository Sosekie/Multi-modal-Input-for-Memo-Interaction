# MMUI_project
## Already done:
- Implement Merge speech recognition, speech trigger.
- Implement a Virtual Memo from the Speech (create a new memo).
- Catch the memo by the gesture
- Open the memo on a new window
- Templete evaluation survey: https://docs.google.com/forms/d/e/1FAIpQLScNHHTZhl1JdlbPnvrYLgjG7TIuZC6hA3dre9IEgac6i2ZWVQ/viewform?usp=sharing

## Next steps:

Priority:
- Add text to memo by speech
- Improve catch memo function (don't overlap 2 memos while catching)
- Merge memos togheter by gesture
- Upgrading the speech part for the Merge (merge the red one, or the green) (merge the red one on the green one)
- Add some Interfaces on the screeen (see which function is ON/OFF)

How to add text:
- catch a memo
- say open
- say add
- speak content
- say stop
- say close

## Evaluation statistics about (still to choose):
- response time of functions
- how much time it takes to move a memo from a specific point to another
- better do the merge with the speech or catching 2 memos togheter
- percentage of the correct speech text on the memo said
- how much time it takes to recognize correctly the speech command
- confront the speed text writing between keyboard typing and speech talk
- confront speed merging between our modalities and the copy paste mouse/keyboard modality
- Using as references System Usability Scale (SUS) or Usability Metric for User Experience (UMUX)

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
