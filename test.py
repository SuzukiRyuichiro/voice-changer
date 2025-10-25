import sounddevice as sd
import numpy as np

# List devices
devices = sd.query_devices()
for i, dev in enumerate(devices):
    print(f"{i}: {dev['name']} - In:{dev['max_input_channels']} Out:{dev['max_output_channels']}")

# Test with specific device IDs
INPUT_DEVICE = 0   # Change this after seeing the list
OUTPUT_DEVICE = 1  # Change this after seeing the list

def callback(indata, outdata, frames, time, status):
    outdata[:] = indata

with sd.Stream(device=(INPUT_DEVICE, OUTPUT_DEVICE),
               channels=2,
               callback=callback):
    print(f"Routing device {INPUT_DEVICE} → {OUTPUT_DEVICE}")
    print("Press Ctrl+C to stop")
    sd.sleep(10000)
