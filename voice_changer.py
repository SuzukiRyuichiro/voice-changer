import sounddevice as sd
import numpy as np
from scipy import signal

# Settings
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

        # Output to all channels
        for i in range(outdata.shape[1]):
            outdata[:, i] = shifted

    except Exception as e:
        print(f"Error: {e}")
        outdata.fill(0)

def list_devices():
    """List all audio devices and return input/output capable devices"""
    devices = sd.query_devices()

    input_devices = []
    output_devices = []

    print("\n=== AVAILABLE AUDIO DEVICES ===\n")

    for i, dev in enumerate(devices):
        device_type = []
        if dev['max_input_channels'] > 0:
            device_type.append("INPUT")
            input_devices.append(i)
        if dev['max_output_channels'] > 0:
            device_type.append("OUTPUT")
            output_devices.append(i)

        if device_type:  # Only show devices with input or output
            print(f"[{i}] {dev['name']}")
            print(f"    Type: {' & '.join(device_type)}")
            print(f"    Channels: In={dev['max_input_channels']}, Out={dev['max_output_channels']}")
            print(f"    Sample Rate: {int(dev['default_samplerate'])} Hz")
            print()

    return input_devices, output_devices, devices

def select_device(device_list, device_type):
    """Let user select a device from the list"""
    while True:
        choice = input(f"Select {device_type} device number: ").strip()
        try:
            device_num = int(choice)
            if device_num in device_list:
                return device_num
            else:
                print(f"❌ Device {device_num} is not a valid {device_type} device. Try again.")
        except ValueError:
            print("❌ Please enter a valid number.")

# Main
print("=== REAL-TIME VOICE CHANGER ===")

# Step 1: List devices and let user choose
input_devices, output_devices, devices = list_devices()

if not input_devices:
    print("❌ No input devices found!")
    exit(1)
if not output_devices:
    print("❌ No output devices found!")
    exit(1)

print("--- DEVICE SELECTION ---")
input_device = select_device(input_devices, "INPUT")
output_device = select_device(output_devices, "OUTPUT")

# Get device info
input_info = devices[input_device]
output_info = devices[output_device]

# Determine channels
input_channels = min(input_info['max_input_channels'], 2)  # Use mono or stereo
output_channels = min(output_info['max_output_channels'], 2)

# Use the sample rate from the input device (or take minimum if different)
sample_rate = int(input_info['default_samplerate'])

print(f"\n✓ Input: [{input_device}] {input_info['name']} ({input_channels} ch)")
print(f"✓ Output: [{output_device}] {output_info['name']} ({output_channels} ch)")
print(f"✓ Sample Rate: {sample_rate} Hz")

# Step 2: Select effect
print("\n--- EFFECT SELECTION ---")
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

# Step 3: Start streaming
print(f"\nLatency: ~{BLOCK_SIZE/sample_rate*1000:.1f}ms")
print("\n🎤 Starting voice changer...")
print("Press Enter or Ctrl+C to stop\n")

try:
    # Handle case where input and output are the same device (common on Android)
    if input_device == output_device:
        # Same device - use duplex mode with unified configuration
        print(f"\n⚠️  Using duplex mode (same device for input/output)")
        with sd.Stream(device=input_device,
                       samplerate=sample_rate,
                       blocksize=BLOCK_SIZE,
                       dtype='float32',
                       channels=max(input_channels, output_channels),
                       callback=callback):
            print("🔴 RECORDING... (voice changer active)\n")
            input("Press Enter to stop...\n")
    else:
        # Different devices - use separate input/output configuration
        with sd.Stream(device=(input_device, output_device),
                       samplerate=sample_rate,
                       blocksize=BLOCK_SIZE,
                       dtype='float32',
                       channels=(input_channels, output_channels),
                       callback=callback):
            print("🔴 RECORDING... (voice changer active)\n")
            input("Press Enter to stop...\n")

except KeyboardInterrupt:
    print("\n\n✓ Stopped")
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting tips:")

    # Android-specific tips
    if "OpenSLES" in str(e) or "android" in str(e).lower():
        print("\n🤖 Android-specific issues detected:")
        print("- Make sure Termux has RECORD_AUDIO permission")
        print("- Close any other apps using the microphone/speakers")
        print("- Try restarting Termux")
        print("- Some Android devices require specific sample rates (try 44100 or 48000)")
        print("- If using Bluetooth/USB audio, make sure it's fully connected")

    # General tips
    print("\n💡 General tips:")
    print("- Try different devices")
    print("- Check device permissions")
    print("- Make sure devices are properly connected")
    print("- Try reducing BLOCK_SIZE if you get buffer errors")
