"""
Test audio OUTPUT only (no microphone needed)
Plays a simple tone to verify speakers/headphones work
"""
import sounddevice as sd
import numpy as np

print("=== Audio Output Test ===\n")

# Test configurations
configs = [
    ("44100 Hz, 1 channel", 44100, 1),
    ("48000 Hz, 1 channel", 48000, 1),
    ("44100 Hz, 2 channels", 44100, 2),
    ("48000 Hz, 2 channels", 48000, 2),
]

for name, sample_rate, channels in configs:
    print(f"Testing: {name}...", end=" ")
    try:
        # Generate 440 Hz tone (A note)
        duration = 0.5  # seconds
        t = np.linspace(0, duration, int(sample_rate * duration))
        tone = 0.3 * np.sin(2 * np.pi * 440 * t)

        # Reshape for channels
        if channels == 2:
            tone = np.column_stack([tone, tone])

        sd.play(tone, samplerate=sample_rate, device=0)
        sd.wait()
        print("✓ SUCCESS")
    except Exception as e:
        print(f"✗ FAILED: {str(e)[:60]}")

print("\n=== Test Complete ===")
