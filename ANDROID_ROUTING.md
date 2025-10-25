# Android Audio Routing Guide

## The Challenge

On Android, `sounddevice` (via PortAudio/OpenSLES) only exposes a single "default" device. You cannot directly select between:
- Wired headset microphone
- Built-in microphone
- Bluetooth speaker
- Wired headset speaker

## How Android Handles Audio Routing

Android manages audio routing **at the system level** based on device priority:

### Priority Order (Highest to Lowest):
1. **Wired headset** - When plugged in, both input AND output route here
2. **Bluetooth A2DP** - Output only (audio playback)
3. **Bluetooth SCO/HFP** - Both input and output (phone calls, voice chat)
4. **Built-in speaker/mic** - Fallback when nothing else connected

## Solutions for Your Use Case

### Goal: Input from wired mic, Output to Bluetooth speaker

#### Option 1: Hot-Swap Method (RECOMMENDED)
1. Start the voice changer with wired headphones plugged in
2. Once running, **slowly unplug** the wired headphones
3. Android will re-route:
   - Input: Built-in mic OR Bluetooth mic (if BT supports it)
   - Output: Bluetooth speaker
4. **Then plug microphone only** into the wired jack (not headphones)

#### Option 2: Use Bluetooth SCO/HFP Profile
Some Bluetooth speakers support both playback (A2DP) and microphone (HFP/SCO):
1. Connect Bluetooth speaker
2. Enable "Phone audio" profile for the Bluetooth device in Android settings
3. Android will route both input and output to Bluetooth
4. Use wired mic by setting Bluetooth as output only (requires Android audio settings)

#### Option 3: Use a USB Audio Interface (If available)
1. Get a USB-C audio adapter that supports separate input/output
2. Connect via OTG adapter
3. This may expose as separate devices in Android

#### Option 4: Use Audio Router Apps
Install Android apps like:
- **SoundAbout** (requires root on newer Android versions)
- **Lesser AudioSwitch** (limited functionality)
- **Bluetooth Audio Router**

These apps can force specific routing, but may require root access.

## Testing Your Setup

Run `python test_routing.py` to test where audio is being routed.

## Workaround in Code

Unfortunately, there's **no reliable Python/sounddevice way** to control Android audio routing without root access or system-level changes. The routing is handled by Android's AudioFlinger service.

## Recommended Approach

Use the hot-swap method with `voice_changer_android.py`:
1. Start with wired headphones plugged in
2. Unplug headphones while running
3. Audio output routes to Bluetooth
4. Plug in just the microphone (3.5mm mic only, or use built-in mic)

This is the most reliable method without requiring root or additional apps.
