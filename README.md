# CSI 4160 Group Project

## Project Structure Outline:
- The serverfiles folder contains everything capable to bridge our connections between our sql database and the game statistics. This folder also contains app.py, which helps to manage our CPU opponent bots boardstate and difficulty.
- The static and templates folders both work together to handle the front-end view of our game. This includes HTML, javascript, and CSS files to ensure the homepage of our tictacetoe game works properly for both the player and bot.
- stateofplayout.py file tracks and logs key information from the users local Pi system onto the GCP storage and bucket areas.
- manager.py is used to manage our sql database information, along with monitoring system resources and such.
- winout.py is another file used to send out information to Google Cloud Storage.
- tictactoe.py is the very baseline of our entire project and its the first file we began development upon. This file holds all the logic for handling the tictactoe game via the Raspberry Pi sensehat boardstate.