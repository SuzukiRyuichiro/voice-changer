"""
Detailed audio device inspection for Android
Shows all available audio APIs and devices
"""
import sounddevice as sd

print("=== Detailed Audio Device Inspection ===\n")

# Get all host APIs
print("Available Host APIs:")
apis = sd.query_hostapis()
for i, api in enumerate(apis):
    print(f"\n[API {i}] {api['name']}")
    print(f"  Default Input Device: {api['default_input_device']}")
    print(f"  Default Output Device: {api['default_output_device']}")
    print(f"  Devices: {api['devices']}")

print("\n" + "="*50)
print("All Devices (Detailed):")
print("="*50 + "\n")

devices = sd.query_devices()
for i, dev in enumerate(devices):
    print(f"[{i}] {dev['name']}")
    print(f"    Host API: {dev['hostapi']} ({apis[dev['hostapi']]['name']})")
    print(f"    Max Input Channels: {dev['max_input_channels']}")
    print(f"    Max Output Channels: {dev['max_output_channels']}")
    print(f"    Default Sample Rate: {dev['default_samplerate']} Hz")
    print(f"    Default Low Input Latency: {dev['default_low_input_latency']}")
    print(f"    Default Low Output Latency: {dev['default_low_output_latency']}")
    print(f"    Default High Input Latency: {dev['default_high_input_latency']}")
    print(f"    Default High Output Latency: {dev['default_high_output_latency']}")
    print()

print("="*50)
print("Default Devices:")
print("="*50)
print(f"Default Input Device: {sd.default.device[0]}")
print(f"Default Output Device: {sd.default.device[1]}")
print()

# Try to get current default settings
try:
    default_settings = sd.default.settings
    print("Default Settings:")
    for key, value in default_settings.items():
        print(f"  {key}: {value}")
except:
    pass
