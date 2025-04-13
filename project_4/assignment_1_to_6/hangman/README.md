# Hangman Game

A web-based implementation of the classic Hangman game using Python and Streamlit.

## Features

- Interactive web interface using Streamlit
- Random word selection from a predefined list
- Visual ASCII art representation of the hangman
- Letter and word guessing functionality
- Game state persistence using Streamlit's session state
- Win/lose condition tracking
- Play Again and Reset Game options

## How to Play

1. The game randomly selects a word from a predefined list
2. You can guess either:
   - A single letter
   - The entire word
3. You have 6 attempts to guess the word correctly
4. Each incorrect guess adds a part to the hangman figure
5. The game ends when you either:
   - Guess the word correctly (win)
   - Run out of attempts (lose)

## Technical Details

### Dependencies
- Python 3.x
- Streamlit
- Random (Python standard library)

### Game Components

1. **Word Selection**
   - Uses a predefined list of programming-related words
   - Randomly selects a word for each game
   - Words are converted to uppercase for consistency

2. **Game State Management**
   - Uses Streamlit's session state to maintain game progress
   - Tracks:
     - Word completion status
     - Guessed letters
     - Guessed words
     - Number of remaining attempts
     - Win/lose status

3. **User Interface**
   - Clean, web-based interface
   - Real-time feedback on guesses
   - Visual representation of the hangman
   - Progress tracking
   - Reset and Play Again options

4. **Game Logic**
   - Validates input (single letters or complete words)
   - Checks for duplicate guesses
   - Updates word completion based on correct guesses
   - Manages attempt counter
   - Determines win/lose conditions

## Getting Started
create project by uv :
uv add .
1. Install the required dependencies:
   ```bash

   uv add streamlit
   .venv\Scripts\activate #activate virtual environment
   ```

2. Run the game:
   ```bash
   streamlit run main.py
   ```

3. Open your web browser and navigate to the provided local URL

## Game Controls

- **Guess Input**: Enter a letter or word in the text input field
- **Submit Guess**: Click the submit button to make your guess
- **Play Again**: Start a new game with a new random word
- **Reset Game**: Clear all game state and start fresh

## Word List
The game uses the following words:
- python
- javascript
- programming
- computer
- science
- algorithm
- data
