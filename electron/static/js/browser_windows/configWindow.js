const { ipcRenderer } = require('electron');

document.querySelector('.configFormSubmit')
    .addEventListener('click', function () {
        let formData = {
            flaskAddress: document.getElementById('flaskAddress').value
        };
        ipcRenderer.send('config_submit', formData);
    });

