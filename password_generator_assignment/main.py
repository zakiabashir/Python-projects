def main():
    import streamlit as st
    import random
    import string

    st.title("Password Generator App")
    st.header("Generate strong and secure passwords")

    # Password length input
    length = st.number_input("Enter Password Length", min_value=0, max_value=32, value=12, step=1)

    # Password complexity options
    use_uppercase = st.checkbox("Include Uppercase Letters", value=True)
    use_lowercase = st.checkbox("Include Lowercase Letters", value=True)
    use_numbers = st.checkbox("Include Numbers", value=True)
    use_special = st.checkbox("Include Special Characters", value=True)

    if st.button("Generate Password"):
        # Check for zero or less than 6 length
        if length == 0:
            st.error("Password length cannot be 0. Please enter a length greater than 0.")
            return
        elif length < 6:
            st.error("Password length must be at least 6 characters for security. Please enter a longer length.")
            return

        # Create character pool based on selected options
        chars = ""
        if use_uppercase:
            chars += string.ascii_uppercase
        if use_lowercase:
            chars += string.ascii_lowercase
        if use_numbers:
            chars += string.digits
        if use_special:
            chars += string.punctuation

        if chars:  # Check if at least one option is selected
            password = ''.join(random.choice(chars) for _ in range(length))
            st.success("Generated Password:")
            st.code(password)
        else:
            st.error("Please select at least one character type")

        # Add password strength indicator
        
        if len(password) >= 24 and sum([use_uppercase, use_lowercase, use_numbers, use_special]) >= 4:
            st.write("Password Strength: too Strong Password!💪💪")
        elif len(password) >= 12 and sum([use_uppercase, use_lowercase, use_numbers, use_special]) >= 3:
            st.write("Password Strength: Strong Password! 💪")
        elif len(password) >= 8 and sum([use_uppercase, use_lowercase, use_numbers, use_special]) >= 2:
            st.write("Password Strength: ⚠️ Moderate Password - Consider adding more security features.")
        elif len(password) >= 5 and sum([use_uppercase, use_lowercase, use_numbers, use_special]) >= 2:
            st.write("Password Strength: ❌ Weak Password - Improve it using the suggestions above.")
        else:
            st.write("Password Strength: ❌ Very Weak Password - Please increase length and add more character types.")
            
if __name__ == "__main__":
    main()
