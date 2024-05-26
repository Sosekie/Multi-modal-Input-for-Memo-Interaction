import numpy as np
import torch
import torchaudio
import soundfile as sf
import time

def rms_energy(audio_data):
    """Calculate the RMS energy of an audio signal."""
    return np.sqrt(np.mean(np.square(audio_data)))

def loudness_difference(audio_data1, audio_path2, target_sr=16000):
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
    
    print("🎵 - Calculate RMS energy...")
    start_time = time.time()
    rms1 = rms_energy(y1)
    rms2 = rms_energy(y2)
    print(f"Time elapsed: {time.time() - start_time:.2f} seconds")
    
    loudness_diff = abs(rms1 - rms2)
    print(f"🎵 - Loudness difference: {loudness_diff}")
    
    return loudness_diff
