import random
import streamlit as st

def play_rock_paper_scissors():
    user_action = st.selectbox("Choose your action:", ["Rock", "Paper", "Scissors"])
    possible_actions = ["Rock", "Paper", "Scissors"]
    computer_action = random.choice(possible_actions)

    st.write(f"You chose {user_action}, computer chose {computer_action}.")

    if user_action == computer_action:
        st.write("It's a tie!")
    elif user_action == "Rock":
        if computer_action == "Scissors":
            st.write("Rock smashes scissors! You win!")
        else:
            st.write("Paper covers rock! You lose.")
    elif user_action == "Paper":
        if computer_action == "Rock":
            st.write("Paper covers rock! You win!")
        else:
            st.write("Scissors cuts paper! You lose.")
    elif user_action == "Scissors":
        if computer_action == "Paper":
            st.write("Scissors cuts paper! You win!")
        else:
            st.write("Rock smashes scissors! You lose.")

st.title("Rock, Paper, Scissors")
play_rock_paper_scissors()
