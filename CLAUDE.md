# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time voice changer application in Python that applies pitch-shifting effects to audio input.

## Dependencies

```bash
pip install sounddevice numpy scipy
```

## Key Commands

**Run the voice changer (with interactive device selection):**
```bash
python voice_changer.py
```
The app will:
1. List all available audio devices
2. Prompt you to select input device
3. Prompt you to select output device
4. Prompt you to select voice effect
5. Start real-time voice changing

**List audio devices (for debugging):**
```bash
python test_devices.py
```

**Test Android audio compatibility:**
```bash
python test_android.py
```
This script tests various sample rate and channel configurations to find what works on your Android device.

## Architecture

The application uses:
- **sounddevice** for real-time audio streaming with callback-based processing
- **numpy** for signal processing and pitch shifting via resampling
- Configurable sample rate and block size (affects latency vs CPU usage)

Main implementation is in `voice_changer.py` with interactive effect selection. Other Python files are testing/development utilities.

## Development Notes

- Codebase is currently in active development
- Pitch shifting is achieved through simple resampling (higher factor = higher pitch)
- Audio callback must remain lightweight to avoid buffer underruns
- **Cross-platform support**:
  - On Mac/desktop: Select different devices for input (mic) and output (speakers)
  - On Android: Can select the same "default" device for both input and output (common with wired headphones)
  - The app auto-detects whether to use separate or unified device configuration
- **Android troubleshooting**:
  - If you get "OpenSLES" errors, ensure Termux has RECORD_AUDIO permission
  - Close other apps using audio (music players, voice recorders, etc.)
  - Use `test_android.py` to find the optimal sample rate and channel configuration for your device
  - Some devices work better with specific sample rates (44100 or 48000 Hz)
