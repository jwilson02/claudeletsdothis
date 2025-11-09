const { app, BrowserWindow, globalShortcut, ipcMain, screen } = require('electron');
const path = require('path');
const Store = require('electron-store');

const store = new Store();

let overlayWindow = null;
let isOverlayVisible = true;
let isCompactMode = false;

function createOverlayWindow() {
  const { width, height } = screen.getPrimaryDisplay().workAreaSize;

  // Get saved position or use default
  const savedBounds = store.get('windowBounds', {
    x: width - 420,
    y: 20,
    width: 400,
    height: height - 40
  });

  overlayWindow = new BrowserWindow({
    x: savedBounds.x,
    y: savedBounds.y,
    width: savedBounds.width,
    height: savedBounds.height,
    frame: false,
    transparent: true,
    alwaysOnTop: true,
    resizable: true,
    skipTaskbar: false,
    webPreferences: {
      nodeIntegration: true,
      contextIsolation: false,
      enableRemoteModule: true
    }
  });

  overlayWindow.loadFile('overlay.html');

  // Save window position on move/resize
  const saveBounds = () => {
    store.set('windowBounds', overlayWindow.getBounds());
  };

  overlayWindow.on('moved', saveBounds);
  overlayWindow.on('resized', saveBounds);

  overlayWindow.on('closed', () => {
    overlayWindow = null;
  });

  // Open DevTools in development
  // overlayWindow.webContents.openDevTools();

  return overlayWindow;
}

app.whenReady().then(() => {
  createOverlayWindow();

  // Global hotkey: F9 - Toggle overlay visibility
  globalShortcut.register('F9', () => {
    if (overlayWindow) {
      if (isOverlayVisible) {
        overlayWindow.hide();
        isOverlayVisible = false;
      } else {
        overlayWindow.show();
        isOverlayVisible = true;
      }
    }
  });

  // Global hotkey: F10 - Toggle compact mode
  globalShortcut.register('F10', () => {
    if (overlayWindow) {
      isCompactMode = !isCompactMode;
      overlayWindow.webContents.send('toggle-compact-mode', isCompactMode);
    }
  });

  // Global hotkey: Ctrl+Shift+R - Reload overlay
  globalShortcut.register('CommandOrControl+Shift+R', () => {
    if (overlayWindow) {
      overlayWindow.reload();
    }
  });

  app.on('activate', () => {
    if (BrowserWindow.getAllWindows().length === 0) {
      createOverlayWindow();
    }
  });
});

app.on('window-all-closed', () => {
  if (process.platform !== 'darwin') {
    app.quit();
  }
});

app.on('will-quit', () => {
  // Unregister all shortcuts
  globalShortcut.unregisterAll();
});

// IPC handlers
ipcMain.on('minimize-window', () => {
  if (overlayWindow) {
    overlayWindow.minimize();
  }
});

ipcMain.on('close-window', () => {
  if (overlayWindow) {
    overlayWindow.close();
  }
});

ipcMain.on('toggle-clickthrough', (event, enabled) => {
  if (overlayWindow) {
    overlayWindow.setIgnoreMouseEvents(enabled, { forward: true });
  }
});

// Save and restore app state
ipcMain.on('save-state', (event, state) => {
  store.set('appState', state);
});

ipcMain.handle('load-state', () => {
  return store.get('appState', null);
});
