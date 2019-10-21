'use strict';
const { app, ipcMain } = require('electron');
const Window = require('./static/js/window').Window;
const WebWindow = require('./static/js/window').WebWindow;
const fs = require('fs');

const configDir = './config/';
const configFilename = 'config.json';
const configPath = configDir + configFilename;
const configWindowPath = './static/html/config_window.html';

let mainWindow;

function createConfigWindow(path) {
    mainWindow = new Window({
        file: path
    });
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function createVisualizationWindow(url) {
    mainWindow = new WebWindow({
        url: url
    });
    mainWindow.on('closed', function () {
        mainWindow = null;
    });
}

function hasConfigFolder() {
        return fs.existsSync(configDir);
}

function hasConfig() {
    return fs.existsSync(configDir + configFilename);
}

function initializeApp() {
    if (!hasConfigFolder()) {
        fs.mkdirSync(configDir);
    }
    if (hasConfig()) {
        fs.readFile(configPath, (err, data) => {
            if (err) throw err;
            let configJson = JSON.parse(data.toString());
            let flaskAddress = configJson['flaskAddress'];
            createVisualizationWindow(flaskAddress);
        });
    } else {
        createConfigWindow(configWindowPath);
        ipcMain.on('config_submit', (event, data) => {
            fs.writeFile(configPath, JSON.stringify(data, null, 3), err => {
                if (err) {
                    throw err;
                }
            });
            mainWindow.close();
            let flaskAddress = data['flaskAddress'];
            createVisualizationWindow(flaskAddress);
        });
    }
}

app.on('ready', initializeApp);

app.on('window-all-closed', () => {
    if (process.platform !== 'darwin') {
        app.quit();
    }
});



