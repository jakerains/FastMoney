# Fast Money Game

Fast Money is a Python-based implementation of the popular game show segment "Fast Money" from Family Feud. This application provides a control panel for the game host and a separate game board display for contestants and audience.

## Features

- Load custom questions and answers
- Support for two players
- Full-screen game board display
- Control panel for game management
- Custom answer input
- Score tracking and reveal
- Player switching functionality
- Game reset option

## Requirements

- Python 3.x (with Tkinter, which is included in standard Python distributions)

## Installation

1. Ensure you have Python 3.x installed on your system.
2. Clone this repository or download the `FastMoney.py` file.

## Usage

1. Run the script:
   ```
   python FastMoney.py
   ```
2. The control panel and game board windows will appear.
3. Load questions and answers in the following format in the control panel:
   ```
   1. Question
   • Answer 1: Points
   • Answer 2: Points
   ...
   ```
4. Click "Load Questions" to start the game.
5. Use the control panel to manage the game flow, reveal answers, and switch players.

## Game Flow

1. Player 1 answers all questions.
2. Reveal Player 1's answers and scores.
3. Switch to Player 2.
4. Player 2 answers all questions.
5. Reveal Player 2's answers and scores.
6. Game ends, displaying the total score.

## Controls

- Next Question: Move to the next question
- Skip: Skip the current question
- Custom Answer: Enter a custom answer not in the predefined list
- Reveal Answer/Score: Show the player's answer and score on the game board
- Switch Player: Change from Player 1 to Player 2
- Reset All: Start a new game

## Note

This game is designed for local play and requires a host to manage the control panel. It's ideal for educational or entertainment purposes in a group setting.

## License

MIT License

## Contributing

Contributions, issues, and feature requests are welcome. Feel free to check [issues page] if you want to contribute.

## Author

Jake Rains