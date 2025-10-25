# Android Development Status

**Date:** 2025-10-25
**Current Issue:** OpenSLES error -9999 when trying to use duplex mode (device 0 for both input/output) on Android

## Problem Summary

When selecting device 0 on Android (which shows as "default" with both INPUT & OUTPUT capabilities), the app fails with:
```
Error opening Stream: Unanticipated host error [PaErrorCode -9999]: 'Initializing inputstream failed' [android OpenSLES error -9999]
```

## Changes Made (in this session)

### 1. Enhanced `voice_changer.py`
- **Split stream configuration** (lines 150-170): Separate code paths for duplex vs separate devices
- **Added explicit dtype='float32'**: More reliable with OpenSLES backend
- **Android-specific error handling** (lines 178-192): Helpful troubleshooting tips when OpenSLES errors occur

### 2. Created `test_android.py`
- Diagnostic tool that tests 4 configurations:
  - 44100 Hz, 1 channel
  - 48000 Hz, 1 channel
  - 44100 Hz, 2 channels
  - 48000 Hz, 2 channels
- Helps identify which config works on your device

### 3. Updated `CLAUDE.md`
- Added Android troubleshooting section
- Documented `test_android.py` usage

## Next Steps for Android Testing

1. **Run diagnostic first:**
   ```bash
   python test_android.py
   ```
   Select device 0 and see which configuration succeeds

2. **Check permissions:**
   - Ensure Termux has RECORD_AUDIO permission
   - Settings → Apps → Termux → Permissions

3. **Close other audio apps:**
   - Music players, voice recorders, etc.

4. **Try voice_changer.py:**
   - After confirming a working config, try the main app

## Technical Context

- **Platform:** Android with Termux
- **Audio backend:** OpenSLES (Android's low-latency audio API)
- **Device config:** Single "default" device (device 0) for both input and output
- **Common with:** Wired headphones, USB-C audio adapters

## Known Issues

OpenSLES error -9999 typically indicates:
- Permission issues (RECORD_AUDIO not granted)
- Audio session conflict (another app using audio)
- Unsupported sample rate/channel combination
- Device-specific compatibility issues

## Code References

- Duplex stream setup: `voice_changer.py:150-160`
- Separate device setup: `voice_changer.py:162-170`
- Android error handling: `voice_changer.py:178-192`
- Device selection logic: `voice_changer.py:84-95`
