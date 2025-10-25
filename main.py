import sounddevice as sd
import numpy as np
from scipy import signal

# Parameters
PITCH_SHIFT = 1.5  # 1.5 = higher pitch, 0.7 = lower pitch
BLOCK_SIZE = 1024
SAMPLE_RATE = 44100

def pitch_shift(data, factor):
    """Simple pitch shifting using resampling"""
    indices = np.round(np.arange(0, len(data), factor))
    indices = indices[indices < len(data)].astype(int)
    return data[indices]

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    # Get mono input
    audio = indata[:, 0]

    # Apply pitch shift
    shifted = pitch_shift(audio, 1/PITCH_SHIFT)

    # Resize to match output
    if len(shifted) < frames:
        shifted = np.pad(shifted, (0, frames - len(shifted)))
    else:
        shifted = shifted[:frames]

    # Write to output (both channels)
    outdata[:, 0] = shifted
    outdata[:, 1] = shifted

# Start streaming
with sd.Stream(samplerate=SAMPLE_RATE,
               blocksize=BLOCK_SIZE,
               channels=2,
               callback=callback):
    print("Voice changer running... Press Ctrl+C to stop")
    sd.sleep(1000000)
