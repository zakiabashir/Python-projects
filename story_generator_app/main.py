import random
import streamlit as st
import openai

# Set your OpenAI API key
openai.api_key = "YOUR-API-KEY-HERE"

def get_story_input():
    st.title("AI Story Generator!")
    st.write("Please provide some inputs to create your unique AI-generated story:")
    
    story_name = st.text_input("Enter a name for your story:")
    character = st.text_input("Enter a main character name:")
    genre = st.selectbox("Select story genre:", ["Fantasy", "Adventure", "Mystery", "Romance", "Science Fiction"])
    setting = st.text_input("Enter the story setting/place:")
    theme = st.text_input("Enter a theme or moral:")
    
    return story_name, character, genre, setting, theme

def generate_ai_story(story_name, character, genre, setting, theme):
    prompt = f"""Create an engaging {genre} story with the following elements:
    Story Title: {story_name}
    Main Character: {character}
    Setting: {setting}
    Theme: {theme}
    
    The story should be 3-4 paragraphs long with a clear beginning, middle and end."""
    
    try:
        response = openai.Completion.create(
            engine="text-davinci-003",
            prompt=prompt,
            max_tokens=1000,
            temperature=0.7,
            top_p=1.0,
            frequency_penalty=0.0,
            presence_penalty=0.0
        )
        return response.choices[0].text.strip()
    except Exception as e:
        st.error(f"OpenAI API error: {str(e)}")
        # Fallback to template-based story if API fails
        templates = [
            f"Title: {story_name}\n\nIn the mystical {setting}, there lived a brave soul named {character}. "
            f"Their story began on an ordinary day that would soon turn extraordinary. "
            f"Little did they know that fate had special plans in store.\n\n"
            f"Through trials and tribulations, {character} discovered the true meaning of {theme}. "
            f"Each step of their journey brought new challenges and revelations.\n\n"
            f"In the end, {character}'s tale became a legend in {setting}, "
            f"teaching future generations about the power of {theme}.",
            
            f"Title: {story_name}\n\nThe {setting} had never seen anyone quite like {character}. "
            f"Their presence brought a unique energy that would change everything.\n\n"
            f"As days turned into weeks, {character} faced countless challenges that tested their resolve. "
            f"The journey to understand {theme} was not an easy one.\n\n"
            f"When all was said and done, {character}'s story became a testament to the enduring spirit of {theme}."
        ]
        return random.choice(templates)

def main():
    # Get user input
    story_name, character, genre, setting, theme = get_story_input()
    
    # Generate story button
    if st.button("Generate AI Story"):
        if story_name and character and genre and setting and theme:
            # Generate and display the story
            story = generate_ai_story(story_name, character, genre, setting, theme)
            
            st.write("\nHere's your AI-generated story:\n")
            st.write(story)
            st.markdown("---")
            
            # Add download button
            st.download_button(
                label="Download Story",
                data=story,
                file_name=f"{story_name}.txt",
                mime="text/plain"
            )
        else:
            st.warning("Please fill in all the fields!")

if __name__ == "__main__":
    main()
