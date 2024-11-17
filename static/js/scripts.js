// This file should be included in your base templates like 'index.html' or 'join.html'

// Function to handle the game start when host clicks 'Start Game'
function startGame() {
    // Send a request to start the game via an API call to the server
    fetch('/start_game', { method: 'POST' })
        .then(response => response.json())
        .then(data => {
            // If the game started successfully, display questions
            if (data.status === 'success') {
                alert('Game Started!');
                window.location.href = '/game/' + data.game_id; // Redirect to the actual game page
            } else {
                alert('Failed to start the game. Please try again.');
            }
        });
}

// Function to handle when a player joins the game
function joinGame() {
    const gameId = document.getElementById('game_id').value; // Get the game ID from the input
    const playerName = document.getElementById('name').value; // Get the player name from the input

    // Ensure both fields are filled
    if (!gameId || !playerName) {
        alert("Please enter both the Game ID and your name.");
        return;
    }

    // Send the player data (gameId and playerName) to the server to join the game
    fetch('/join_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({
            game_id: gameId,
            name: playerName
        })
    })
    .then(response => response.json())
    .then(data => {
        // If the join request is successful, show the player the game page
        if (data.status === 'success') {
            alert("You have joined the game successfully!");
            window.location.href = '/game/' + gameId; // Redirect to the game page
        } else {
            alert("Failed to join the game. Make sure the Game ID is correct.");
        }
    })
    .catch(error => {
        console.error('Error joining game:', error);
        alert("An error occurred while joining the game.");
    });
}

// Handle the "Done" button and start the countdown
function startCountdown() {
    let countdown = 100;
    const countdownDisplay = document.getElementById("countdown");
    
    const interval = setInterval(function() {
        countdownDisplay.textContent = countdown;
        countdown--;
        
        if (countdown < 0) {
            clearInterval(interval);
            alert("Time's up!");
            // Here you could send a request to the server to lock answers and show results
        }
    }, 1000); // Update every second
}
