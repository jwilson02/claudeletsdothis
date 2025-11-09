# Complete Setup Guide - PoE Build Guide + Companion Extension

This guide explains how to set up both the web-based build guide tool and the in-game overlay companion.

## Architecture Overview

The PoE Build Guide system consists of two components:

1. **Backend Server** (`poe-build-guide/`)
   - Flask API that handles PoB parsing, data storage, and game information
   - Runs on `http://localhost:5000`
   - Provides REST API for build management and progress tracking

2. **Companion Extension** (`poe-companion-extension/`)
   - Electron-based overlay window
   - Always-on-top in-game display
   - Communicates with the Flask backend
   - Hotkey support and auto-save

## Installation Steps

### Prerequisites

Install the following before starting:

1. **Python 3.10+**
   - Download from https://python.org/downloads/
   - Check "Add Python to PATH" during installation

2. **Node.js 16+**
   - Download from https://nodejs.org/
   - Choose LTS version
   - Includes npm automatically

### Step 1: Set Up Backend Server

```bash
# Navigate to backend folder
cd poe-build-guide

# Install Python dependencies
pip install -r requirements.txt

# Test the backend
python app.py
```

You should see:
```
* Running on http://localhost:5000
```

Keep this terminal open or minimize it. The backend must stay running.

### Step 2: Set Up Companion Extension

Open a NEW terminal/command prompt:

```bash
# Navigate to companion folder
cd poe-companion-extension

# Install Node dependencies (one-time, ~100MB)
npm install

# Start the companion
npm start
```

The overlay window should appear!

## Usage Workflow

### First Time Setup

1. **Start Backend**: Run `start.bat` in `poe-build-guide/` folder
2. **Start Companion**: Run `npm start` in `poe-companion-extension/` folder
3. **Import Build**:
   - Get your Path of Building code
   - Paste into companion overlay
   - Click "Import"
4. **Set Progress**:
   - Enter your current level
   - Select your current act
5. **Position Window**:
   - Drag to your preferred corner
   - Resize as needed
   - Position is saved automatically

### Daily Usage

**Quick Start:**

1. Run `start.bat` in `poe-companion-extension/` folder
   - This starts BOTH backend and companion automatically

2. Launch Path of Exile

3. Use hotkeys while playing:
   - **F9**: Toggle overlay visibility
   - **F10**: Toggle compact mode

### In-Game Usage

1. **Full Mode** (F10 off):
   - Shows all quest details
   - Displays tips, skills, gear
   - Good for planning and reference

2. **Compact Mode** (F10 on):
   - Minimal space usage
   - Shows current quests only
   - Perfect for active gameplay

3. **Hidden** (F9 twice):
   - Completely hidden
   - Use when you don't need guidance
   - Press F9 to bring back

## Building Standalone Executables

### Backend Executable (Optional)

```bash
cd poe-build-guide
pip install pyinstaller
python build_exe.py
```

Creates `dist/PoEBuildGuide.exe` (standalone, no Python needed)

### Companion Executable (Recommended)

```bash
cd poe-companion-extension
npm run build:win
```

Creates installer in `dist/` folder that includes:
- Electron runtime
- All companion files
- Auto-updater support

**Note**: Backend must still be running separately.

## Deployment Options

### Option 1: Development Mode (Current)

**Pros**: Easy to modify and debug
**Cons**: Requires Python and Node.js installed

**Run**:
- Terminal 1: `python app.py` (backend)
- Terminal 2: `npm start` (companion)

### Option 2: Hybrid (Recommended)

**Pros**: No Node.js needed for end users
**Cons**: Still need Python or backend exe

**Run**:
- Backend: `python app.py` OR `PoEBuildGuide.exe`
- Companion: Install from `PoE-Companion-Setup.exe`

### Option 3: Full Standalone (Future)

Package both backend and companion into single installer.

**Challenges**:
- Large file size (~200MB)
- Complex packaging
- Potential antivirus false positives

## Directory Structure

```
claudeletsdothis/
├── poe-build-guide/              # Backend server
│   ├── app.py                    # Flask API server
│   ├── pob_parser.py             # PoB code decoder
│   ├── game_data.py              # Quest/lab/tips data
│   ├── demo_build.py             # Demo build data
│   ├── requirements.txt          # Python dependencies
│   ├── start.bat                 # Backend launcher
│   ├── data/                     # Saved builds & progress
│   ├── templates/
│   │   └── index.html            # Web UI (optional)
│   └── static/
│       ├── css/
│       └── js/
│
└── poe-companion-extension/      # Overlay companion
    ├── main.js                   # Electron main process
    ├── overlay.html              # UI structure
    ├── overlay.css               # Styling
    ├── overlay.js                # Logic & API calls
    ├── package.json              # Node dependencies
    ├── start.bat                 # Combined launcher
    ├── README.md                 # Companion docs
    └── QUICKSTART.md             # Quick reference
```

## Troubleshooting

### Backend Issues

**"Port 5000 already in use"**
- Edit `app.py`, change `port=5000` to `port=5001`
- Update `API_BASE` in `overlay.js` to match

**"Module not found"**
- Run `pip install -r requirements.txt` again
- Check Python is in PATH

### Companion Issues

**"Backend not running"**
- Start Flask backend first
- Check `http://localhost:5000/api/builds` in browser
- Should see `{"builds": []}`

**Overlay not visible**
- Press F9 (might be hidden)
- Check Windows notifications area
- Restart companion

**Hotkeys not working**
- Give companion focus once after startup
- Check for conflicting hotkeys
- Try Ctrl+Shift+R to reload

### In-Game Issues

**Overlay not showing in PoE**
- Use Windowed Fullscreen mode (not fullscreen)
- Check if overlay is behind game window
- Try Alt+Tab to bring forward

**Performance problems**
- Use compact mode (F10)
- Close accordion sections you don't need
- Reduce overlay size

## Advanced Configuration

### Custom Hotkeys

Edit `main.js`:

```javascript
// Change F9 to F11
globalShortcut.register('F11', () => { ... });

// Change F10 to F12
globalShortcut.register('F12', () => { ... });
```

### Custom Port

**Backend** - Edit `app.py`:
```python
app.run(host='0.0.0.0', port=5001)  # Changed from 5000
```

**Companion** - Edit `overlay.js`:
```javascript
const API_BASE = 'http://localhost:5001/api';  // Changed from 5000
```

### Custom Styling

Edit `overlay.css` to change colors:

```css
/* Orange accent - change to blue */
#d97706 → #3b82f6

/* Transparency - more opaque */
rgba(15, 15, 20, 0.95) → rgba(15, 15, 20, 0.98)
```

## Tips & Best Practices

1. **Window Position**: Place in top-right corner of screen
2. **Compact Mode**: Use during active gameplay
3. **Full Mode**: Use during town/planning phases
4. **Quest Tracking**: Check them off as you complete
5. **Act Changes**: Update act selector when you progress
6. **Auto-Save**: Progress saves automatically, no manual save needed

## Getting Help

1. Check README files in each folder
2. Review troubleshooting sections
3. Verify both backend and companion are running
4. Test with demo build first
5. Check browser console (F12) for API errors

## Future Enhancements

Planned features:
- [ ] Auto-detect PoE process
- [ ] Multi-build quick switch
- [ ] PoE.ninja integration
- [ ] Trade API integration
- [ ] Voice notifications
- [ ] Custom milestone editor

---

**Ready to start?** Use the Quick Start section and you'll be up and running in 5 minutes!

Happy leveling, Exile! ⚔️
