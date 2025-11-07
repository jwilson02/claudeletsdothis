# Path of Exile Build Guide Tool

A Windows application that helps you import and follow Path of Building (PoB) builds with step-by-step guidance through the leveling process.

## Features

- **Import PoB Builds**: Paste your Path of Building export code to import builds
- **Progress Tracking**: Track your current level, act, and completed milestones
- **Leveling Guide**: Step-by-step checklist through all acts and into maps
- **Skills & Gems**: View all skill gems and their setups from your build
- **Gear Tracking**: See recommended gear from your PoB build
- **Passive Tree**: View passive tree information
- **Build Notes**: Access any notes from your PoB build
- **Multiple Builds**: Import and manage multiple builds

## Quick Start (Windows)

### Option 1: Run from Python (Recommended for first-time setup)

1. **Install Python** (if not already installed)
   - Download Python 3.10 or newer from [python.org](https://www.python.org/downloads/)
   - During installation, check "Add Python to PATH"

2. **Download this project**
   - Download and extract the ZIP file to a folder (e.g., `C:\PoEBuildGuide`)

3. **Install dependencies**
   - Open Command Prompt in the project folder
   - Run: `pip install -r requirements.txt`

4. **Start the application**
   - Double-click `start.bat` or run in Command Prompt: `python app.py`
   - Your browser will open automatically to `http://localhost:5000`

### Option 2: Windows Executable (Coming Soon)

A standalone .exe file will be available for download that requires no Python installation.

## How to Use

### 1. Export from Path of Building

1. Open Path of Building
2. Select your build
3. Click "Import/Export Build"
4. Click "Generate" to create a build code
5. Click "Copy" to copy the code to clipboard

### 2. Import Build

1. Open the PoE Build Guide Tool in your browser
2. Paste your PoB code into the text area
3. Click "Import Build"
4. Your build will appear in the builds list

### 3. Track Your Progress

1. Click on a build to view details
2. Update your current level and act
3. Check off milestones as you complete them
4. Browse skills, gems, and gear recommendations
5. Your progress is saved automatically

## Project Structure

```
poe-build-guide/
├── app.py                 # Main Flask application
├── pob_parser.py          # Path of Building code parser
├── requirements.txt       # Python dependencies
├── start.bat             # Windows startup script
├── data/                 # Saved builds and progress (auto-created)
├── templates/
│   └── index.html        # Main web interface
└── static/
    ├── css/
    │   └── style.css     # Styling
    └── js/
        └── app.js        # Frontend JavaScript
```

## Tips

- **Import Multiple Builds**: You can import as many builds as you want
- **Delete Old Builds**: Click "Delete Build" when viewing a build you no longer need
- **Progress Tracking**: Milestones are based on typical progression speeds
- **Skill Gems**: The tool shows all gem setups from your PoB build
- **Passive Tree**: For detailed passive tree viewing, use Path of Building alongside this tool

## Troubleshooting

### "Module not found" errors
- Make sure you ran `pip install -r requirements.txt`
- Try: `pip install --upgrade -r requirements.txt`

### Port 5000 already in use
- Edit `app.py` and change `port=5000` to another port like `5001`
- Or close any other applications using port 5000

### Build import fails
- Make sure you copied the complete PoB code
- Verify the code is from a recent version of Path of Building
- Try exporting the build again from PoB

### Browser doesn't open automatically
- Manually navigate to `http://localhost:5000` in your browser

## Building Windows Executable

To create a standalone .exe file:

1. Install PyInstaller: `pip install pyinstaller`
2. Run: `python build_exe.py`
3. The executable will be in the `dist` folder

## Requirements

- Python 3.10 or newer
- Windows 10 or newer (Windows 7/8 may work but are untested)
- Modern web browser (Chrome, Firefox, Edge)

## Dependencies

- Flask 3.0.0 - Web framework
- Flask-CORS 4.0.0 - Cross-origin support
- lxml 5.1.0 - XML parsing
- requests 2.31.0 - HTTP library

## Credits

Created for the Path of Exile community. This tool is not affiliated with Grinding Gear Games.

Path of Building is created by Openarl and LocalIdentity.

## License

MIT License - Feel free to use, modify, and distribute.

## Support

For issues or feature requests, please create an issue on the project repository.

Happy Exile hunting!
