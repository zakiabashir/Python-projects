
import streamlit as st  # For creating the web app.
import random  # For generating random numbers.

# Function to generate a random secret number.
def generate_secret_number():
    """
    This function generates a random 3-digit secret number with unique digits.
    """
    digits = list(range(10))  # Create a list of digits 0 to 9.
    random.shuffle(digits)  # Shuffle the list to randomize the order.
    return ''.join(map(str, digits[:3]))  # Return the first 3 digits as a string.

# Function to compare the guess with the secret number and provide feedback.
def get_feedback(secret, guess):
    """
    This function compares the guess with the secret number and provides feedback.

    Args:
        secret (str): The secret number.
        guess (str): The player's guess.

    Returns:
        tuple: Feedback string and a boolean indicating whether the guess is correct.
    """
    if secret == guess:  # If the guess matches the secret number, the player wins.
        return "👌👌👌", True
    feedback = []  # Initialize feedback list.
    for i in range(3):  # Iterate through each digit of the guess.
        if guess[i] == secret[i]:  # If the digit is in the correct position, add 👌.
            feedback.append("👌")
        elif guess[i] in secret:  # If the digit is present but in the wrong position, add 👍.
            feedback.append("👍")
        else:  # If the digit is not present, add ❌.
            feedback.append("❌")
    return ' '.join(feedback), False  # Return the feedback string and False for incorrect guess.

# Initialize session state variables to store the game data.
if 'secret_number' not in st.session_state:
    st.session_state.secret_number = generate_secret_number()  # Generate the secret number.
if 'attempts' not in st.session_state:
    st.session_state.attempts = 0  # Initialize the number of attempts.
if 'max_attempts' not in st.session_state:
    st.session_state.max_attempts = 10  # Set the maximum allowed attempts.
if 'game_over' not in st.session_state:
    st.session_state.game_over = False  # Set the game status to False (not over).

# Set up the Streamlit UI.
st.title("Guess the Secret Number")  # Display the game title.
st.write("I have generated a secret three-digit number. Can you guess what it is?")  # Display instructions.
st.write("Feedback legend: 👌 = Correct digit and position, 👍 = Correct digit but wrong position, ❌ = Incorrect digit")  # Explain feedback symbols.
st.write(f"You have {st.session_state.max_attempts - st.session_state.attempts} attempts remaining.")  # Display remaining attempts.

# Main game loop.
if not st.session_state.game_over:  # Check if the game is still ongoing.
    guess = st.text_input("Enter your 3-digit guess:", max_chars=3)  # Get player's guess.
    if st.button("Submit Guess"):  # Check if the "Submit Guess" button is clicked.
        if len(guess) == 3 and guess.isdigit():  # Validate the guess.
            st.session_state.attempts += 1  # Increment the number of attempts.
            feedback, correct = get_feedback(st.session_state.secret_number, guess)  # Get feedback.
            st.write(f"Feedback: {feedback}")  # Display feedback to the player.
            if correct:  # If the guess is correct.
                st.success(f"Congratulations! You've guessed the secret number: {st.session_state.secret_number}")  # Display success message.
                st.session_state.game_over = True  # Set game over to True.
            elif st.session_state.attempts >= st.session_state.max_attempts:  # If maximum attempts reached.
                st.error(f"Game over! The secret number was: {st.session_state.secret_number}")  # Display game over message and reveal the secret number.
                st.session_state.game_over = True  # Set game over to True.
        else:
            st.error("Please enter a valid 3-digit number.")  # Display error for invalid guess.

    # If the game is over, show the option to play again.
    if st.session_state.game_over:
        if st.button("Play Again"):
            st.session_state.secret_number = generate_secret_number()  # Reset the secret number.
            st.session_state.attempts = 0  # Reset attempts.
            st.session_state.game_over = False  # Reset game status.
            st.experimental_rerun()  # Rerun the app to start a new game.
else:  # If the game is not yet started, show the "Start New Game" button.
    if st.button("Start New Game"):
        st.session_state.secret_number = generate_secret_number()  # Reset the secret number.
        st.session_state.attempts = 0  # Reset attempts.
        st.session_state.game_over = False  # Reset game status.
        st.experimental_rerun()  # Rerun the app to start a new game.