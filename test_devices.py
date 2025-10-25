import sounddevice as sd

print("=== AUDIO DEVICES ===\n")
devices = sd.query_devices()

for i, dev in enumerate(devices):
    device_type = []
    if dev['max_input_channels'] > 0:
        device_type.append("INPUT")
    if dev['max_output_channels'] > 0:
        device_type.append("OUTPUT")

    print(f"[{i}] {dev['name']}")
    print(f"    Type: {' & '.join(device_type)}")
    print(f"    Channels: In={dev['max_input_channels']}, Out={dev['max_output_channels']}")
    print(f"    Sample Rate: {dev['default_samplerate']} Hz")
    print()

print(f"\nDefault Input: {sd.default.device[0]}")
print(f"Default Output: {sd.default.device[1]}")
