# Import required libraries
import streamlit as st

def main():
    # Set page configuration and background
    st.markdown("""
        <style>
        .main {
            background-color: #f0f2f6;
        }
        .stButton>button {
            background-color: #4CAF50;
            color: white;
        }
        .stNumberInput>div>div>input {
            background-color: #ffffff;
        }
        </style>
        """, unsafe_allow_html=True)

    # Set the title of the Streamlit app with custom styling
    st.markdown("<h1 style='text-align: center; color: #2e4053;'>BMI Calculator</h1>", unsafe_allow_html=True)
    
    # Create input fields with custom container background
    with st.container():
        st.markdown("<div style='background-color: #e8f4f9; padding: 20px; border-radius: 10px;'>", unsafe_allow_html=True)
        st.write("Enter your height and weight to calculate BMI")
        height = st.number_input("Height (in meters)", min_value=0.1, max_value=3.0, value=1.7)
        weight = st.number_input("Weight (in kg)", min_value=1.0, max_value=500.0, value=70.0)
        st.markdown("</div>", unsafe_allow_html=True)
    
    # Calculate BMI when user clicks the button
    if st.button("Calculate BMI"):
        # BMI formula: weight / (height * height)
        bmi = weight / (height ** 2)
        
        # Display the calculated BMI in a colored container
        st.markdown(f"<div style='background-color: #dcdde1; padding: 10px; border-radius: 5px; text-align: center;'><h3>Your BMI is: {bmi:.2f}</h3></div>", unsafe_allow_html=True)
        
        # Provide BMI category based on calculated value with custom styling
        if bmi < 18.5:
            st.markdown("<div style='background-color: #fff3cd; padding: 10px; border-radius: 5px;'>You are Underweight</div>", unsafe_allow_html=True)
        elif 18.5 <= bmi < 25:
            st.markdown("<div style='background-color: #d4edda; padding: 10px; border-radius: 5px;'>You have a Normal weight</div>", unsafe_allow_html=True)
        elif 25 <= bmi < 30:
            st.markdown("<div style='background-color: #fff3cd; padding: 10px; border-radius: 5px;'>You are Overweight</div>", unsafe_allow_html=True)
        else:
            st.markdown("<div style='background-color: #f8d7da; padding: 10px; border-radius: 5px;'>You are Obese</div>", unsafe_allow_html=True)
        
        # Display BMI chart with custom styling
        st.markdown("""
        <div style='background-color: #e8f4f9; padding: 20px; border-radius: 10px; margin-top: 20px;'>
            <h4>BMI Categories:</h4>
            <ul>
                <li>Underweight: < 18.5</li>
                <li>Normal weight: 18.5 - 24.9</li>
                <li>Overweight: 25 - 29.9</li>
                <li>Obese: ≥ 30</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

if __name__ == "__main__":
    # Run the Streamlit app
    main()
