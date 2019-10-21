'use strict';
const { BrowserWindow } = require('electron');

const localWindowOptions = {
    width: 800,
    height: 600,
    webPreferences: {
        nodeIntegration: true
    }
};

const remoteWindowOptions = {
    width: 800,
    height: 600,
    webPreferences: {
        nodeIntegration: false
    }
};

class Window extends BrowserWindow {
    constructor ({ file, ...windowSettings }) {
        super({ ...localWindowOptions, ...windowSettings });
        this.loadFile(file);
        this.once('ready-to-show', () => {
            this.show();
        });
    }
}

class WebWindow extends BrowserWindow {
    constructor ({ url, ...windowSettings }) {
        super({ ...remoteWindowOptions, ...windowSettings });
        this.loadURL(url);
        this.once('ready-to-show', () => {
            this.show();
        });
    }
}

module.exports = {
    Window: Window,
    WebWindow: WebWindow
};
