# MMUI_project
## Already done:
- Implement Merge speech recognition, speech trigger.
- Implement a Virtual Memo from the Speech (create a new memo).
- Catch the memo by the gesture 

## Next steps:

Priority:
- Add text to memo by speech
- Improve catch memo function (don't overlap 2 memos while catching)
- Merge memos togheter by gesture
- Upgrading the speech part for the Merge (merge the red one, or the green) (merge the red one on the green one)
- Add some Interfaces on the screeen (see which function is ON/OFF)

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
