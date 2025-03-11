import streamlit as st  # Streamlit library for creating web applications
import json  # JSON library for reading and writing data files

# Set page background with gradient
# Purpose: Creates an animated gradient background for visual appeal
# Uses CSS to define gradient colors and animation
st.markdown(
    """
    <style>
    .stApp {
        background: linear-gradient(45deg, #ffb3b3, #b3ffec, #b3e6ff, #ccff99);
        background-size: 400% 400%;
        animation: gradient 15s ease infinite;
    }
    @keyframes gradient {
        0% {background-position: 0% 50%;}
        50% {background-position: 100% 50%;}
        100% {background-position: 0% 50%;}
    }
    </style>
    """,
    unsafe_allow_html=True  # Allows HTML/CSS to be rendered
)

# Load library data from file
# Purpose: Reads the saved book data from library.txt file when app starts
# Returns empty list if file doesn't exist yet
def load_library():
    try:
        with open('library.txt', 'r') as file:  # Opens file in read mode
            return json.load(file)  # Converts JSON string back to Python object
    except FileNotFoundError:
        return []  # Returns empty list if file not found

# Save library data to file 
# Purpose: Saves the current state of library to file whenever changes are made
# This ensures data persists between app sessions
def save_library(library):
    with open('library.txt', 'w') as file:  # Opens file in write mode
        json.dump(library, file)  # Converts Python object to JSON string

# Add a new book to the library with title, author, year, genre and read status
# Purpose: Collects book details from user through form inputs
# Adds new book to library list and saves updated data
def add_book(library):
    title = st.text_input("Enter the book title:")  # Text field for book title
    author = st.text_input("Enter the author:")  # Text field for author name
    year = st.number_input("Enter the publication year:", min_value=0, max_value=2024, value=2024)  # Number input for year with validation
    genre = st.text_input("Enter the genre:")  # Text field for book genre
    read = st.checkbox("Have you read this book?")  # Checkbox to mark if book is read
    
    if st.button("Add Book"):  # Button to submit the form
        book = {
            'title': title,
            'author': author, 
            'year': year,
            'genre': genre,
            'read': read
        }
        library.append(book)  # Add new book to library list
        st.success("Book added successfully!")  # Show success message
        save_library(library)  # Save updated library to file

# Remove a book from library by matching title
# Purpose: Allows user to remove books they no longer want to track
# Searches by exact title match (case-insensitive)
def remove_book(library):
    title = st.text_input("Enter the title of the book to remove:")  # Get title to remove
    if st.button("Remove Book"):  # Button to confirm removal
        for book in library[:]:  # Loop through copy of library to safely remove
            if book['title'].lower() == title.lower():  # Case-insensitive title match
                library.remove(book)  # Remove matching book
                st.success("Book removed successfully!")  # Show success message
                save_library(library)  # Save updated library
                return
        st.error("Book not found!")  # Show error if book not found

# Search for books by title or author
# Purpose: Helps user find specific books in their library
# Supports partial matches for both title and author searches
def search_book(library):
    st.write("Search by:")  # Search instructions
    search_option = st.radio("Select search criteria:", ["Title", "Author"])  # Radio buttons for search type
    search_term = st.text_input("Enter the search term:").lower()  # Search input field
    
    found_books = []  # List to store matching books
    if search_term:
        # Search by title or author based on selection
        if search_option == "Title":
            found_books = [book for book in library if search_term in book['title'].lower()]  # Filter books by title
        else:
            found_books = [book for book in library if search_term in book['author'].lower()]  # Filter books by author
    
        if found_books:
            st.write("\nMatching Books:")  # Display matching results header
            display_books(found_books)  # Show matching books
        else:
            st.warning("No matching books found!")  # Show warning if no matches

# Display list of books with their details
# Purpose: Shows formatted list of books with all their information
# Used by both search results and full library display
def display_books(books):
    for i, book in enumerate(books, 1):  # Loop through books with counter starting at 1
        read_status = "Read" if book['read'] else "Unread"  # Convert boolean to readable status
        st.write(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")  # Format and display book details

# Show statistics about the library like total books and percentage read
# Purpose: Provides overview of library size and reading progress
def display_statistics(library):
    total_books = len(library)  # Count total books
    if total_books == 0:
        st.warning("No books in library!")  # Show warning if library empty
        return
        
    read_books = sum(1 for book in library if book['read'])  # Count read books
    percent_read = (read_books / total_books) * 100  # Calculate percentage read
    
    st.write(f"\nTotal books: {total_books}")  # Display total count
    st.write(f"Percentage read: {percent_read:.1f}%")  # Display percentage with 1 decimal

# Main function to run the Streamlit app
# Purpose: Sets up the app interface and handles navigation between features
def main():
    st.title("Personal Library Manager App")  # App title
    
    # Add app description and creator info
    st.write("A simple and efficient way to manage your personal book collection. Keep track of your reading progress and organize your library.")
    st.write("Created by: Zakia Bashir")
    
    # Load existing library data
    library = load_library()  # Load saved books when app starts
    
    # Define menu options and their corresponding functions
    menu_options = {
        "Add a book": add_book,  # Function to add new books
        "Remove a book": remove_book,  # Function to remove books
        "Search for a book": search_book,  # Function to search books
        "Display all books": lambda x: display_books(x),  # Function to show all books
        "Display statistics": display_statistics  # Function to show library stats
    }
    
    # Create sidebar menu for selecting actions
    choice = st.sidebar.selectbox("Choose an action:", list(menu_options.keys()))  # Dropdown menu for navigation
    
    # Execute selected function
    if choice:
        menu_options[choice](library)  # Run selected feature with library data

if __name__ == "__main__":
    main()
