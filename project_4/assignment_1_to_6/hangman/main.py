import random  # Import random module to select random words
import streamlit as st  # Import streamlit for web app interface
from streamlit.runtime.scriptrunner import RerunException  # Import for handling page reruns

# Define the list of words for the game - these are the possible words that can be randomly selected
words = ["python", "javascript", "programming", "computer", "science", "algorithm", "data"]

# Function to randomly select and return a word in uppercase
def get_word():
    word = random.choice(words)  # Randomly select a word from the list
    return word.upper()  # Convert to uppercase for consistency

# Main game function that handles the game logic
def play(word):
    # Initialize game state variables in session state if not already present
    # Session state persists data between reruns
    if 'word_completion' not in st.session_state:
        st.session_state.word_completion = "_" * len(word)  # Create placeholder with underscores
        st.session_state.guessed = False  # Track if word is guessed
        st.session_state.guessed_letters = []  # Store guessed letters
        st.session_state.guessed_words = []  # Store guessed words
        st.session_state.tries = 6  # Number of attempts allowed

    # Display game status
    st.write("Let's play Hangman!")
    st.write(display_hangman(st.session_state.tries))  # Show hangman ASCII art
    st.write(st.session_state.word_completion)  # Show current word progress

    # Create input form for user guesses
    with st.form(key='guess_form'):
        guess = st.text_input("Please guess a letter or word: ").upper()  # Get user input
        submit_button = st.form_submit_button(label='Submit Guess')

        # Process the guess when form is submitted
        if submit_button and guess:
            # Handle single letter guess
            if len(guess) == 1 and guess.isalpha():
                if guess in st.session_state.guessed_letters:
                    st.write("You already guessed the letter", guess)
                elif guess not in word:
                    st.write(guess, "is not in the word.")
                    st.session_state.tries -= 1  # Decrease attempts
                    st.session_state.guessed_letters.append(guess)
                else:
                    st.write("Good job,", guess, "is in the word!")
                    st.session_state.guessed_letters.append(guess)
                    # Update word completion to show correctly guessed letters
                    word_as_list = list(st.session_state.word_completion)
                    indices = [i for i, letter in enumerate(word) if letter == guess]
                    for index in indices:
                        word_as_list[index] = guess
                    st.session_state.word_completion = "".join(word_as_list)
                    if "_" not in st.session_state.word_completion:
                        st.session_state.guessed = True
            # Handle full word guess
            elif len(guess) == len(word) and guess.isalpha():
                if guess in st.session_state.guessed_words:
                    st.write("You already guessed the word", guess)
                elif guess != word:
                    st.write(guess, "is not the word.")
                    st.session_state.tries -= 1
                    st.session_state.guessed_words.append(guess)
                else:
                    st.session_state.guessed = True
                    st.session_state.word_completion = word
            else:
                st.write("Not a valid guess.")

    # Update display after guess
    st.write(display_hangman(st.session_state.tries))
    st.write(st.session_state.word_completion)

    # Check win/lose conditions
    if st.session_state.guessed:
        st.success("Congrats, you guessed the word! You win!")  # Show win message
        if st.button('Play Again'):
            st.session_state.clear()  # Reset game state
            st.rerun()  # Reload page
    elif st.session_state.tries <= 0:
        st.error(f"Sorry, you ran out of tries. The word was {word}. Maybe next time!")  # Show lose message
        if st.button('Play Again'):
            st.session_state.clear()
            st.rerun()

# Function to display ASCII art of hangman based on remaining tries
def display_hangman(tries):
    stages = [  # List of hangman states from most complete to empty
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / \\
                   -
                """,
                # Each subsequent stage removes one body part
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |     / 
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|/
                   |      |
                   |      
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |     \\|
                   |      |
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |      |
                   |      |
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      O
                   |    
                   |      
                   |     
                   -
                """,
                """
                   --------
                   |      |
                   |      
                   |    
                   |      
                   |     
                   -
                """
    ]
    return stages[tries]  # Return ASCII art based on remaining tries

# Main Streamlit app function
def main():
    st.title("Hangman Game")  # Set page title
    
    # Initialize or get the word from session state
    if "word" not in st.session_state:
        st.session_state.word = get_word()  # Get new word if none exists
    
    play(st.session_state.word)  # Start game with current word

    # Add reset button to start new game
    if st.button('Reset Game'):
        st.session_state.clear()  # Clear all session state
        st.rerun()  # Reload page

# Run the app
if __name__ == "__main__":
    main()