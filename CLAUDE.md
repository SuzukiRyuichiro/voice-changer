# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Real-time voice changer application in Python that applies pitch-shifting effects to audio input.

## Dependencies

```bash
pip install sounddevice numpy scipy
```

## Key Commands

**List audio devices:**
```bash
python test_devices.py
```

**Run the voice changer:**
```bash
python voice_changer.py
```

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
