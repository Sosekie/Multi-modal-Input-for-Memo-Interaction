import numpy as np
import torch
import torchaudio
from scipy.spatial.distance import cosine
import soundfile as sf
from io import BytesIO
import librosa
import time

def extract_mfcc_torchaudio(audio_data, sample_rate, n_mfcc=6):
    # Convert audio data to float tensor
    waveform = torch.tensor(audio_data, dtype=torch.float32).unsqueeze(0)
    mfcc_transform = torchaudio.transforms.MFCC(
        sample_rate=sample_rate,
        n_mfcc=n_mfcc,
        melkwargs={"n_fft": 400, "hop_length": 160, "n_mels": 40, "center": False}
    )
    mfcc = mfcc_transform(waveform)
    mfcc = mfcc.mean(dim=2).squeeze().numpy()
    
    # Normalize MFCC features (mean normalization)
    mfcc_mean = np.mean(mfcc)
    mfcc_std = np.std(mfcc)
    mfcc_normalized = (mfcc - mfcc_mean) / mfcc_std

    return mfcc_normalized

def calculate_similarity(mfcc1, mfcc2):
    return cosine(mfcc1, mfcc2)

def similarity(audio_data1, audio_path2, target_sr=16000, n_mfcc=6):
    start_time = time.time()
    
    audio_data1.seek(0)
    
    print("🎵 - Load and resample audio1...")
    y1, sr1 = sf.read(audio_data1)
    if sr1 != target_sr:
        y1 = torch.tensor(y1, dtype=torch.float32)
        y1 = torchaudio.transforms.Resample(orig_freq=sr1, new_freq=target_sr)(y1.unsqueeze(0)).squeeze().numpy()
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    print("🎵 - Load and resample audio2...")
    start_time = time.time()
    y2, sr2 = torchaudio.load(audio_path2)
    if sr2 != target_sr:
        y2 = torchaudio.transforms.Resample(orig_freq=sr2, new_freq=target_sr)(y2).squeeze().numpy()
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    print("🎵 - Extract MFCC features...")
    start_time = time.time()
    mfcc1 = extract_mfcc_torchaudio(y1, target_sr, n_mfcc)
    mfcc2 = extract_mfcc_torchaudio(y2, target_sr, n_mfcc)
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    print("🎵 - Calculate similarity...")
    start_time = time.time()
    similarity_score = calculate_similarity(mfcc1, mfcc2)
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    return similarity_score