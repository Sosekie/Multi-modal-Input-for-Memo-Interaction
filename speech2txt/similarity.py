import numpy as np
import torch
import torchaudio
from scipy.spatial.distance import cosine
import soundfile as sf
from io import BytesIO
import librosa

def extract_mfcc_torchaudio(audio_data, sample_rate, n_mfcc=6):
    # Convert audio data to float tensor
    waveform = torch.tensor(audio_data, dtype=torch.float32).unsqueeze(0)
    mfcc_transform = torchaudio.transforms.MFCC(
        sample_rate=sample_rate,
        n_mfcc=n_mfcc,
        melkwargs={"n_fft": 200, "hop_length": 60, "n_mels": 12, "center": False}
    )
    mfcc = mfcc_transform(waveform)
    return mfcc.mean(dim=2).squeeze().numpy()

def calculate_similarity(mfcc1, mfcc2):
    return 1 - cosine(mfcc1, mfcc2)

def similarity(audio_data1, audio_path2, target_sr=200, n_mfcc=5):
    audio_data1.seek(0)

    y1, sr1 = sf.read(audio_data1)
    
    # Resample audio1 if necessary
    if sr1 != target_sr:
        y1 = librosa.resample(y1, orig_sr=sr1, target_sr=target_sr)
        sr1 = target_sr

    y2, sr2 = librosa.load(audio_path2, sr=target_sr)

    mfcc1 = extract_mfcc_torchaudio(y1, sr1, n_mfcc)
    mfcc2 = extract_mfcc_torchaudio(y2, sr2, n_mfcc)

    return calculate_similarity(mfcc1, mfcc2)