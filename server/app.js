const express = require("express");
const app = express();
const path = require("path")
const {exec} = require("child_process");
const port = 8080;

app.use(express.static(path.join(__dirname, "../pages")));

app.get('/', (req, res) => {
  res.sendFile(path.join(__dirname, "../pages", "index.html"));
});

app.get('/api/start-hangman', (req, res) => {
    console.log('Attempting to launch the Python Hangman game...');
    exec('python ../game.py', (error, stdout, stderr) => {
        if (error) {
            console.error(`[LAUNCH FAILED] Could not execute script: ${error.message}`);
            return res.status(500).json({ error: 'Server failed to launch the game script.' });
        }
        
        if (stderr) {
            console.error(`[PYTHON ERROR] Script ran with errors: ${stderr}`);
            return res.status(500).json({ error: 'The game script encountered an error.' });
        }

        console.log('[LAUNCH SUCCESS] Hangman game started successfully!');
        res.json({ gameOutput: stdout });
    });
});

app.listen(port, () => {
});