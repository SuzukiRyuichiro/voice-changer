"""
Android-specific audio test script
Tests different configurations to find what works on your device
"""
import sounddevice as sd
import numpy as np

print("=== Android Audio Test ===\n")

# List devices
devices = sd.query_devices()
print("Available devices:")
for i, dev in enumerate(devices):
    print(f"[{i}] {dev['name']}")
    print(f"    In: {dev['max_input_channels']}, Out: {dev['max_output_channels']}")
    print(f"    Sample Rate: {dev['default_samplerate']} Hz\n")

# Auto-select default device (device 0)
device_id = 0
dev_info = devices[device_id]
print(f"Testing device: [{device_id}] {dev_info['name']}")

# Test configurations
configs = [
    ("44100 Hz, 1 channel", 44100, 1),
    ("48000 Hz, 1 channel", 48000, 1),
    ("44100 Hz, 2 channels", 44100, 2),
    ("48000 Hz, 2 channels", 48000, 2),
]

print("\n=== Testing Configurations ===\n")

def callback(indata, outdata, frames, time, status):
    """Simple passthrough"""
    if indata.ndim == 1:
        outdata.fill(0)
        outdata[:len(indata), 0] = indata
    else:
        outdata[:] = indata

for name, sample_rate, channels in configs:
    print(f"Testing: {name}...", end=" ")
    try:
        with sd.Stream(
            device=device_id,
            samplerate=sample_rate,
            blocksize=1024,
            dtype='float32',
            channels=channels,
            callback=callback
        ):
            sd.sleep(500)  # Test for 0.5 seconds
        print("✓ SUCCESS")
    except Exception as e:
        print(f"✗ FAILED: {str(e)[:60]}")

print("\n=== Test Complete ===")
