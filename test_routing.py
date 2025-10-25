"""
Test Android audio routing with Bluetooth and wired headset
This script will help us understand how Android routes audio
"""
import sounddevice as sd
import numpy as np
import subprocess
import json

print("=== Android Audio Routing Test ===\n")

# Get current audio state
try:
    audio_info = subprocess.check_output(['termux-audio-info'])
    info = json.loads(audio_info)
    print("Current Audio Configuration:")
    print(f"  Bluetooth A2DP: {'ON' if info.get('BLUETOOTH_A2DP_IS_ON') else 'OFF'}")
    print(f"  Wired Headset: {'CONNECTED' if info.get('WIREDHEADSET_IS_CONNECTED') else 'DISCONNECTED'}")
    print()
except Exception as e:
    print(f"Could not get audio info: {e}\n")

print("This test will:")
print("1. Record audio from your microphone (should use wired headset mic)")
print("2. Play it back (routing depends on Android system settings)")
print("\nAndroid usually routes:")
print("  - Input: Wired headset mic (if connected)")
print("  - Output: Wired headset OR Bluetooth (based on system priority)")
print()

input("Press Enter to start test...")

# Test parameters
SAMPLE_RATE = 48000
DURATION = 3  # seconds
CHANNELS = 1

print(f"\nRecording for {DURATION} seconds from microphone...")

# Record audio
recording = sd.rec(
    int(DURATION * SAMPLE_RATE),
    samplerate=SAMPLE_RATE,
    channels=CHANNELS,
    dtype='float32',
    device=0
)
sd.wait()
print("Recording complete!")

print("\nNow playing back the recording...")
print("Listen carefully - which device is playing?")
print("  - If you hear it in wired headphones: Android is routing to wired")
print("  - If you hear it in Bluetooth speaker: Android is routing to Bluetooth")
print()

input("Press Enter to play back...")

sd.play(recording, samplerate=SAMPLE_RATE, device=0)
sd.wait()

print("\nPlayback complete!")
print("\nWhere did you hear the playback?")
print("This will help us understand Android's routing behavior.")
