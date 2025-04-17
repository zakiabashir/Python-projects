# Import required libraries
import streamlit as st
import os
from pathlib import Path
import time

def main():
    # Set page configuration and title
    st.set_page_config(page_title="Bulk File Renamer", layout="wide")
    
    # Create a gradient background effect using HTML/CSS
    st.markdown("""
        <style>
        .main {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            background-size: 300% 300%;
            animation: gradient 15s ease infinite;
        }
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        </style>
    """, unsafe_allow_html=True)

    # Display app title with styling
    st.title("🔄 Bulk File Renamer")
    
    # Create a file uploader that accepts multiple files
    uploaded_files = st.file_uploader("Choose files to rename", accept_multiple_files=True)
    
    if uploaded_files:
        # Display the number of selected files
        st.write(f"Selected {len(uploaded_files)} files")
        
        # Create input for prefix/suffix
        prefix = st.text_input("Add prefix to filenames", "")
        suffix = st.text_input("Add suffix to filenames (before extension)", "")
        
        # Create a preview of renamed files
        st.subheader("Preview of renamed files:")
        for file in uploaded_files:
            # Split filename and extension
            name, ext = os.path.splitext(file.name)
            # Create new filename with prefix and suffix
            new_name = f"{prefix}{name}{suffix}{ext}"
            st.text(f"{file.name} ➡️ {new_name}")
        
        # Add rename button
        if st.button("Rename Files"):
            with st.spinner("Renaming files..."):
                for file in uploaded_files:
                    # Get original filename and extension
                    name, ext = os.path.splitext(file.name)
                    # Create new filename
                    new_name = f"{prefix}{name}{suffix}{ext}"
                    
                    # Save the file with new name
                    with open(new_name, "wb") as f:
                        f.write(file.getbuffer())
                    
                    # Add small delay for better UX
                    time.sleep(0.1)
                
                # Show success message
                st.success("Files renamed successfully!")
                
    else:
        # Display instructions when no files are selected
        st.info("Please upload files to begin renaming")

if __name__ == "__main__":
    main()
