import sounddevice as sd
import numpy as np
from scipy import signal

# Settings
SAMPLE_RATE = 44100  # External microphone's native rate
BLOCK_SIZE = 1024    # Lower = less latency, higher CPU usage

# Voice effect presets
EFFECTS = {
    '1': ('Chipmunk', 1.5, 1.0),      # pitch_shift, speed
    '2': ('Deep Voice', 0.7, 1.0),
    '3': ('Robot', 1.2, 0.8),
    '4': ('Demon', 0.6, 0.9),
    '5': ('Normal (passthrough)', 1.0, 1.0)
}

# Current effect
current_effect = 1.0

def pitch_shift_simple(audio, shift_factor):
    """Fast pitch shifting using resampling"""
    if shift_factor == 1.0:
        return audio

    # Resample to shift pitch
    num_samples = int(len(audio) / shift_factor)
    indices = np.linspace(0, len(audio) - 1, num_samples)
    shifted = np.interp(indices, np.arange(len(audio)), audio)

    return shifted

def callback(indata, outdata, frames, time, status):
    if status:
        print(status)

    try:
        # Get mono audio
        audio = indata.flatten() if indata.ndim > 1 else indata.copy()

        # Apply pitch shift
        shifted = pitch_shift_simple(audio, 1.0 / current_effect)

        # Adjust length to match output frame size
        if len(shifted) < frames:
            shifted = np.pad(shifted, (0, frames - len(shifted)))
        else:
            shifted = shifted[:frames]

        # Output to both channels (stereo)
        outdata[:, 0] = shifted
        outdata[:, 1] = shifted

    except Exception as e:
        print(f"Error: {e}")
        outdata.fill(0)

# Main
print("=== REAL-TIME VOICE CHANGER ===\n")
print("Available effects:")
for key, (name, _, _) in EFFECTS.items():
    print(f"  {key}: {name}")

choice = input("\nSelect effect (1-5): ").strip()
if choice in EFFECTS:
    effect_name, current_effect, _ = EFFECTS[choice]
    print(f"\n✓ Using: {effect_name}")
else:
    print("\n✓ Using: Chipmunk (default)")
    current_effect = 1.5

print(f"\nSample Rate: {SAMPLE_RATE} Hz")
print(f"Latency: ~{BLOCK_SIZE/SAMPLE_RATE*1000:.1f}ms")
print("\n🎤 Speak into your wired headphone mic")
print("🔊 Output will go to your MacBook speakers")
print("\nPress Enter or Ctrl+C to stop\n")

try:
    with sd.Stream(device=(0, 3),  # 0=External Mic, 3=MacBook Speakers
                   samplerate=SAMPLE_RATE,
                   blocksize=BLOCK_SIZE,
                   channels=(1, 2),  # (input_channels, output_channels)
                   callback=callback):
        print("🔴 RECORDING... (voice changer active)\n")
        input("Press Enter to stop...\n")

except KeyboardInterrupt:
    print("\n\n✓ Stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
