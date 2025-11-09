# PoE Companion Extension

An Electron-based overlay companion app for Path of Exile that provides in-game build guidance, quest tracking, and progression help.

## Features

- 🎮 **In-Game Overlay**: Always-on-top transparent window that works while playing PoE
- 🎯 **Quest Objectives**: Prioritized quest list for your current act
- 💎 **Skill Tracking**: See which gems to acquire and when
- 🛡️ **Gear Requirements**: Know what gear your build needs
- 🗺️ **Act Tips**: Helpful leveling tips and strategies for each act
- 🏛️ **Lab Tracking**: Track labyrinth trials and ascendancy progress
- ✅ **Milestone Checklist**: Never miss important progression points
- ⌨️ **Hotkeys**: Quick toggle with F9, compact mode with F10
- 💾 **Auto-Save**: Your progress is automatically saved

## Requirements

- Windows 10/11
- Node.js 16+ and npm (for development)
- Python 3.10+ with Flask backend running (from `poe-build-guide` folder)

## Quick Start

### 1. Start the Backend Server

First, ensure the Flask backend is running:

```bash
cd ../poe-build-guide
python app.py
```

The backend should be running on `http://localhost:5000`

### 2. Install Dependencies

```bash
npm install
```

### 3. Run the Companion

```bash
npm start
```

## Hotkeys

- **F9**: Toggle overlay visibility (show/hide)
- **F10**: Toggle compact mode (minimal view)
- **Ctrl+Shift+R**: Reload overlay (for development)

## Usage

### Importing a Build

1. **From Path of Building**:
   - In PoB, click "Generate" → "Share with Pastebin" (or copy code)
   - Paste the code into the companion's input field
   - Click "Import"

2. **Demo Build**:
   - Click "Load Demo Build" to try a pre-configured Lightning Arrow Deadeye

### Tracking Progress

1. Set your current level and act using the controls
2. Check off quests as you complete them
3. Mark milestones when reached
4. Track lab trials and ascendancy completions

### Compact Mode

Press **F10** to toggle compact mode, which shows:
- Current build name, level, and act
- Active quests for your current act
- Minimal screen space usage

Perfect for keeping visible while playing!

## Window Management

- **Drag**: Click and drag the header bar to move the window
- **Resize**: Drag window edges to resize
- **Position**: Window position is saved and restored on restart

## Building for Distribution

### Create Windows Executable

```bash
npm run build:win
```

This creates a standalone `.exe` installer in the `dist/` folder.

### Package Contents

The installer includes:
- Electron runtime
- Companion app files
- Auto-updater (optional)

**Note**: The Flask backend must still be installed and running separately.

## Project Structure

```
poe-companion-extension/
├── main.js              # Electron main process (window, hotkeys)
├── overlay.html         # UI structure
├── overlay.css          # Styling (dark theme, PoE colors)
├── overlay.js           # Renderer process (logic, API calls)
├── package.json         # Dependencies and build config
└── README.md           # This file
```

## API Integration

The companion communicates with the Flask backend on `http://localhost:5000`:

- `POST /api/builds` - Import PoB code
- `GET /api/builds/:id` - Get build data
- `POST /api/builds/demo` - Load demo build
- `GET/POST /api/progress/:id` - Get/update progress
- `GET /api/game-data/quests/:act` - Get quest data
- `GET /api/game-data/tips/:act` - Get act tips
- `GET /api/game-data/labs` - Get labyrinth data

## Troubleshooting

### "Backend not running" error

Make sure the Flask server is running:

```bash
cd ../poe-build-guide
python app.py
```

### Overlay not showing in-game

- Try running in windowed fullscreen mode (not fullscreen)
- Some games block overlays - PoE should work fine
- Check if F9 accidentally toggled visibility off

### Hotkeys not working

- Make sure the companion has focus at least once
- Check Windows focus assist settings
- Try restarting the companion

## Development

### Debug Mode

Uncomment this line in `main.js` to open DevTools:

```javascript
overlayWindow.webContents.openDevTools();
```

### Hot Reload

Press **Ctrl+Shift+R** to reload the overlay without restarting.

## Customization

### Change Hotkeys

Edit `main.js` and modify the `globalShortcut.register()` calls:

```javascript
globalShortcut.register('F9', () => { ... });  // Change 'F9' to your preferred key
```

### Styling

Edit `overlay.css` to customize:
- Colors (search for `#d97706` for orange accent)
- Transparency (adjust `rgba` values)
- Font sizes
- Layout spacing

## Tech Stack

- **Electron 28**: Cross-platform desktop framework
- **electron-store**: Persistent settings storage
- **electron-builder**: Packaging and distribution
- **Vanilla JS**: No frontend framework dependencies

## License

MIT

## Contributing

This companion works alongside the main PoE Build Guide tool. To contribute:

1. Fork the repository
2. Make your changes
3. Test with the Flask backend running
4. Submit a pull request

## Roadmap

- [ ] Auto-detect PoE process and show/hide automatically
- [ ] Multiple build profiles with quick switching
- [ ] Import from PoE.ninja builds
- [ ] Custom milestone creation
- [ ] Audio notifications for quest rewards
- [ ] Integration with trade APIs for gear checking

## Credits

Built for Path of Exile players who want seamless build guidance while playing.

Path of Exile is a trademark of Grinding Gear Games.
