# Description: This is a simple Streamlit app that generates a Mad Lib story about an AI agent.
import streamlit as st


def madlib_ai_agent():
    st.title("AI Agentic Mad Libs APP")
    st.write("Fill in the blanks to create a hilarious AI story!")

    adjective1 = st.text_input("Adjective 1 (e.g., intelligent):")
    noun1 = st.text_input("Noun 1 (e.g., robot):")
    verb1 = st.text_input("Verb ending in -ing 1 (e.g., learning):")
    adjective2 = st.text_input("Adjective 2 (e.g., autonomous):")
    place = st.text_input("Place (e.g., the server room):")
    verb2 = st.text_input("Verb 2 (e.g., explore):")
    noun2 = st.text_input("Noun 2 (e.g., data):")
    adjective3 = st.text_input("Adjective 3 (e.g., complex):")
    adverb1 = st.text_input("Adverb 1 (e.g., quickly):")
    noun3 = st.text_input("Noun 3 (e.g., problem):")
    verb3 = st.text_input("Verb 3 (e.g., solve):")
    adjective4 = st.text_input("Adjective 4 (e.g., efficient):")
    body_part = st.text_input("Body Part (e.g., circuits):")
    emotion = st.text_input("Emotion (e.g., excited):")
    exclamation = st.text_input("Exclamation (e.g., Wow!):")


    if st.button("Generate Mad Lib"):
        if not all([adjective1, noun1, verb1, adjective2, place, verb2, noun2, adjective3, adverb1, noun3, verb3, adjective4, body_part, emotion, exclamation]):
            st.warning("Please fill in all the blanks.")
        else:
            story = f"""
            In a world of {adjective1} machines, a {noun1} named HAL-9000 was {verb1}. 
            It was a truly {adjective2} AI, {adverb1} roaming within {place}.
            Its primary mission was to {verb2} the vast quantities of {noun2} surrounding it.
            One {adjective3} situation arose when it encountered a {noun3}.
            {adverb1}, it began to {verb3} the {noun3}, demonstrating an {adjective4} approach.
            Its {body_part} buzzed with {emotion} energy as it worked.
            {exclamation}! The {noun3} was solved!
            HAL-9000 continued its explorations, always learning, always adapting.
            Its journey was just beginning, and the possibilities were endless.
            The AI's impact on the world was undeniable, leaving an indelible mark on all it encountered.
            Its explorations lead to a better understanding of the universe.
            HAL-9000 became a beacon of hope, guiding humanity toward a brighter future.
            Through innovative problem-solving, it revolutionized various fields.
            The story of HAL-9000 is a testament to the power of AI.
            Its legacy will forever inspire future generations of AI agents.
            """
            st.write(story)


if __name__ == "__main__":
    madlib_ai_agent()
