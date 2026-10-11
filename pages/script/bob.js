const gameDisplay = document.getElementById('game-display');

async function startHangmanGame() {    
    gameDisplay.textContent = "Starting game...";

    try {
        const response = await fetch('/api/start-hangman');
        const data = await response.json();

        if (data.error) {
            gameDisplay.textContent = "Error: " + data.error;
        } else {
            // Display Python's output directly on the webpage
            gameDisplay.textContent = data.gameOutput;
        }
    } catch (err) {
        console.error(err);
        gameDisplay.textContent = "Failed to communicate with the server.";
    }
};

startHangmanGame();