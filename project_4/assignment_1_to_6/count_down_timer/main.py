# Import required libraries
import streamlit as st
import datetime
import time

def main():
    # Set page config and background color
    st.markdown("""
        <style>
        .stApp {
            background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        }
        .timer-input {
            background-color: rgba(255, 255, 255, 0.8);
            padding: 20px;
            border-radius: 10px;
        }
        .countdown {
            background-color: rgba(144, 238, 144, 0.6);
            padding: 30px;
            border-radius: 15px;
            text-align: center;
        }
        </style>
    """, unsafe_allow_html=True)

    # Set the title of the Streamlit app
    st.title("⏰ Countdown Timer")
    
    # Create container with custom background for inputs
    with st.container():
        st.markdown('<div class="timer-input">', unsafe_allow_html=True)
        col1, col2, col3 = st.columns(3)
        with col1:
            hours = st.number_input("Hours", min_value=0, max_value=23, value=0)
        with col2:
            minutes = st.number_input("Minutes", min_value=0, max_value=59, value=0)
        with col3:
            seconds = st.number_input("Seconds", min_value=0, max_value=59, value=0)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Calculate total seconds from user input
    total_seconds = hours * 3600 + minutes * 60 + seconds
    
    # Create a start button
    if st.button("Start Timer"):
        # Create a placeholder for the countdown display
        countdown_placeholder = st.empty()
        
        # Loop until timer reaches zero
        while total_seconds > 0:
            # Calculate hours, minutes, seconds for display
            hrs = total_seconds // 3600
            mins = (total_seconds % 3600) // 60
            secs = total_seconds % 60
            
            # Display current time in countdown_placeholder with custom background
            countdown_placeholder.markdown(
                f'<div class="countdown"><h1>{hrs:02d}:{mins:02d}:{secs:02d}</h1></div>',
                unsafe_allow_html=True
            )
            
            # Wait for 1 second before updating
            time.sleep(1)
            total_seconds -= 1
        
        # Display completion message with animation
        countdown_placeholder.markdown(
            '<div class="countdown" style="background-color: rgba(255, 182, 193, 0.6);"><h1>Time\'s Up! ⏰</h1></div>',
            unsafe_allow_html=True
        )
        st.balloons()

if __name__ == "__main__":
    # Run the Streamlit app
    main()
