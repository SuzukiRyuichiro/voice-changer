"""
Android-optimized voice changer with audio routing control
Attempts to route input from wired mic and output to Bluetooth speaker
"""
import sounddevice as sd
import numpy as np
from scipy import signal
import subprocess
import json
import sys

print("=== Android Voice Changer with Routing ===\n")

# Check audio configuration
try:
    audio_info = subprocess.check_output(['termux-audio-info'])
    info = json.loads(audio_info)
    print("Current Audio Configuration:")
    print(f"  Bluetooth A2DP: {'ON' if info.get('BLUETOOTH_A2DP_IS_ON') else 'OFF'}")
    print(f"  Wired Headset: {'CONNECTED' if info.get('WIREDHEADSET_IS_CONNECTED') else 'DISCONNECTED'}")

    if not info.get('BLUETOOTH_A2DP_IS_ON'):
        print("\n⚠ WARNING: Bluetooth A2DP is OFF")
        print("  Please ensure your Bluetooth speaker is connected")

    if not info.get('WIREDHEADSET_IS_CONNECTED'):
        print("\n⚠ WARNING: Wired headset not detected")
        print("  For best results, connect wired headphones with mic")

    print()
except Exception as e:
    print(f"Could not get audio info: {e}\n")

# Voice effects
EFFECTS = {
    '1': ('Deep Voice (Low Pitch)', 0.75),
    '2': ('High Voice (Chipmunk)', 1.5),
    '3': ('Slight Deep', 0.9),
    '4': ('Slight High', 1.1),
    '5': ('Very Deep', 0.6),
    '6': ('Very High', 1.8),
}

print("Available Voice Effects:")
for key, (name, _) in EFFECTS.items():
    print(f"  [{key}] {name}")

choice = input("\nSelect effect (1-6): ").strip()
if choice not in EFFECTS:
    print("Invalid choice, using default (Deep Voice)")
    choice = '1'

effect_name, pitch_shift = EFFECTS[choice]
print(f"\nUsing effect: {effect_name}")

# Audio parameters
SAMPLE_RATE = 48000  # Standard Android sample rate
BLOCK_SIZE = 2048    # Larger block size for Android stability
CHANNELS = 1         # Mono for better Android compatibility

print(f"\nAudio Settings:")
print(f"  Sample Rate: {SAMPLE_RATE} Hz")
print(f"  Block Size: {BLOCK_SIZE} samples")
print(f"  Channels: {CHANNELS}")
print()

# Try to influence Android routing using termux-api
print("Attempting to configure audio routing...")
try:
    # This might help Android prioritize Bluetooth for output
    # Note: This is experimental and may not work on all devices
    subprocess.run(['termux-media-scan', '/dev/null'],
                   stderr=subprocess.DEVNULL,
                   stdout=subprocess.DEVNULL)
except:
    pass

print("\n⚠ ANDROID ROUTING NOTES:")
print("  - Input will use wired headset mic (if connected)")
print("  - Output routing depends on Android system settings")
print("  - To force Bluetooth output:")
print("    1. Disconnect wired headphones AFTER starting")
print("    2. Or adjust Android sound settings manually")
print("    3. Some Android versions let you choose in quick settings")
print()

# Pitch shift function
def pitch_shift_audio(audio_data, shift_factor):
    """Apply pitch shifting using resampling"""
    if len(audio_data) == 0:
        return audio_data

    # Resample to change pitch
    num_samples = int(len(audio_data) / shift_factor)
    resampled = signal.resample(audio_data, num_samples)

    # Pad or truncate to match block size
    if len(resampled) < len(audio_data):
        resampled = np.pad(resampled, (0, len(audio_data) - len(resampled)), 'constant')
    else:
        resampled = resampled[:len(audio_data)]

    return resampled.astype('float32')

# Audio callback
def callback(indata, outdata, frames, time, status):
    """Process audio in real-time"""
    if status:
        print(f"Status: {status}")

    # Apply pitch shifting
    shifted = pitch_shift_audio(indata[:, 0], pitch_shift)
    outdata[:, 0] = shifted

print("Starting voice changer...")
print("Press Ctrl+C to stop\n")

try:
    with sd.Stream(
        device=0,  # Default device (Android manages routing)
        samplerate=SAMPLE_RATE,
        blocksize=BLOCK_SIZE,
        dtype='float32',
        channels=CHANNELS,
        callback=callback
    ):
        print("✓ Voice changer is running!")
        print(f"✓ Effect: {effect_name}")
        print("\nTIP: If you want output on Bluetooth speaker:")
        print("  1. Keep this running")
        print("  2. Slowly unplug the wired headphones jack")
        print("  3. Android should route output to Bluetooth")
        print("  4. Input will still come from Bluetooth mic or built-in mic")
        print()
        print("Press Ctrl+C to stop...")

        # Keep running
        while True:
            sd.sleep(1000)

except KeyboardInterrupt:
    print("\n\nStopping voice changer...")
except Exception as e:
    print(f"\n\nError: {e}")
    print("\nTroubleshooting:")
    print("  - Ensure microphone permission is granted to Termux")
    print("  - Close other apps using audio")
    print("  - Try disconnecting and reconnecting audio devices")
    sys.exit(1)

print("Voice changer stopped.")
