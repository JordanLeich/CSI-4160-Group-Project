function move(direction) {
    fetch('/move', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ direction: direction })
    }).then(response => response.json()).then(data => {
        location.reload();
    });
}
function set_difficulty(difficulty) {
    fetch('/set_difficulty', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
        body: JSON.stringify({ difficulty: difficulty })
    }).then(response => response.json()).then(data => {
        location.reload();
    });
}
function placeMarker() {
    fetch('/place_marker', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json()).then(data => {
        if (data.status === 'game_over') {
            alert(data.message);  // Show the winner message

            // Delay the reset after clicking "OK" in the alert
            setTimeout(() => {
                resetGame();  // Automatically reset game after message
            }, 500);  // Adjust delay as needed (500ms in this case)
        } else {
            location.reload();
        }
    });
}

function resetGame() {
    fetch('/reset_game', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        },
         body: JSON.stringify({ "resetGame": "resetGame" })
    }).then(response => response.json()).then(data => {
        if (data.status === 'game_reset') {
            location.reload();  // Reload the page to reset the game
        }
    });
}

function resetStats() {
    fetch('/reset_stats', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
        }
    }).then(response => response.json()).then(data => {
        updateStats(data.stats);
    });
}

function updateStats(stats) {
    document.getElementById('x_wins').innerText = stats.X_wins;
    document.getElementById('o_wins').innerText = stats.O_wins;
    document.getElementById('ties').innerText = stats.ties;
    document.getElementById('games_played').innerText = stats.games_played;
    document.getElementById('ai_wins').innerText = stats.AI_wins;  // Update AI wins
}