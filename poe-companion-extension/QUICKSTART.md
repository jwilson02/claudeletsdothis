# Quick Start Guide - PoE Companion Extension

Get up and running in 5 minutes!

## Step 1: Install Node.js

Download and install from: https://nodejs.org/
- Choose the LTS (Long Term Support) version
- Use default installation options

## Step 2: Install Dependencies

Open Command Prompt in this folder and run:

```bash
npm install
```

This downloads all required packages (~100MB, one-time setup).

## Step 3: Start Backend + Companion

### Option A: Use Startup Script (Recommended)

Double-click `start.bat` - this will:
1. Start the Flask backend server
2. Wait a few seconds
3. Launch the companion overlay

### Option B: Manual Start

**Terminal 1 - Backend:**
```bash
cd ..\poe-build-guide
python app.py
```

**Terminal 2 - Companion:**
```bash
npm start
```

## Step 4: Import a Build

1. In the overlay, paste your Path of Building code
2. Click "Import"
3. Or click "Load Demo Build" to try it out

## Step 5: Set Your Progress

1. Enter your current level
2. Select your current act
3. See quest objectives appear!

## Step 6: Use In-Game

- **F9**: Hide/show overlay while playing
- **F10**: Toggle compact mode (small, always-visible)
- Drag the window to your preferred position
- Check off quests as you complete them

## That's It!

You're ready to use the companion while playing Path of Exile.

## Hotkeys Reference

| Key | Action |
|-----|--------|
| F9 | Toggle overlay visibility |
| F10 | Toggle compact/full mode |
| Ctrl+Shift+R | Reload overlay |

## Tips

1. **Windowed Fullscreen**: Works best with PoE in windowed fullscreen mode
2. **Position**: Drag to corner of screen, resize as needed
3. **Compact Mode**: Use F10 for minimal space usage while playing
4. **Auto-Save**: Your progress saves automatically

## Need Help?

- Check the main README.md for detailed documentation
- Make sure Flask backend is running (localhost:5000)
- Try restarting both backend and companion

Enjoy your PoE journey! 🎮⚔️
