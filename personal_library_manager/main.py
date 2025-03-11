def main():
    # Initialize empty library list to store books
    # This will hold all our book records as dictionaries
    library = []
    try:
        # Try to load existing library from file
        # Opens library.txt in read mode to load previously saved books
        with open('library.txt', 'r') as f:
            import json
            # Convert JSON string from file back into Python list
            library = json.load(f)
    except FileNotFoundError:
        # If file doesn't exist, continue with empty library
        # This happens when program runs for first time
        pass

    while True:
        # Main program loop that keeps running until user chooses to exit
        # Display main menu options for user interaction
        print("\nWelcome to your Personal Library Manager!")
        print("1. Add a book")
        print("2. Remove a book") 
        print("3. Search for a book")
        print("4. Display all books")
        print("5. Display statistics")
        print("6. Exit")

        # Get user's menu choice
        choice = input("Enter your choice: ")

        if choice == "1":
            # Option 1: Adding a new book to library
            # Collect all necessary details about the book from user
            title = input("Enter the book title: ")
            author = input("Enter the author: ")
            
            # Loop to ensure valid year input
            # Keeps asking until user enters a valid integer
            while True:
                try:
                    year = int(input("Enter the publication year: "))
                    break
                except ValueError:
                    print("Please enter a valid year")
            
            genre = input("Enter the genre: ")
            # Convert yes/no answer to boolean for read status
            read = input("Have you read this book? (yes/no): ").lower() == "yes"

            # Create a dictionary containing all book information
            # This structure makes it easy to store and retrieve book details
            book = {
                "title": title,
                "author": author,
                "year": year,
                "genre": genre,
                "read": read
            }
            # Add the new book dictionary to library list
            library.append(book)
            print("Book added successfully!")

        elif choice == "2":
            # Option 2: Removing a book from library
            # Get book title to remove and store initial library size
            title = input("Enter the title of the book to remove: ")
            initial_len = len(library)
            # Create new list excluding the book with matching title (case insensitive)
            library = [book for book in library if book["title"].lower() != title.lower()]
            # Check if a book was actually removed by comparing lengths
            if len(library) < initial_len:
                print("Book removed successfully!")
            else:
                print("Book not found")

        elif choice == "3":
            # Option 3: Searching for books
            # Allows searching by either title or author
            print("Search by:")
            print("1. Title")
            print("2. Author")
            search_choice = input("Enter your choice: ")
            
            if search_choice == "1":
                # Search by title (case insensitive)
                # Finds partial matches too, not just exact matches
                search_term = input("Enter the title: ").lower()
                matches = [book for book in library if search_term in book["title"].lower()]
            else:
                # Search by author (case insensitive)
                # Also finds partial matches in author names
                search_term = input("Enter the author: ").lower()
                matches = [book for book in library if search_term in book["author"].lower()]

            # Display all matching books with full details
            if matches:
                print("\nMatching Books:")
                for i, book in enumerate(matches, 1):
                    # Convert boolean read status to user-friendly string
                    read_status = "Read" if book["read"] else "Unread"
                    print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
            else:
                print("No matching books found")

        elif choice == "4":
            # Option 4: Displaying all books
            # Shows complete library listing if not empty
            if library:
                print("\nYour Library:")
                for i, book in enumerate(library, 1):
                    # Format each book's information in a readable way
                    read_status = "Read" if book["read"] else "Unread"
                    print(f"{i}. {book['title']} by {book['author']} ({book['year']}) - {book['genre']} - {read_status}")
            else:
                print("Your library is empty")

        elif choice == "5":
            # Option 5: Library Statistics
            # Calculate and display reading progress
            total_books = len(library)
            if total_books > 0:
                # Count books marked as read
                read_books = len([book for book in library if book["read"]])
                # Calculate percentage of books read
                percent_read = (read_books / total_books) * 100
                print(f"\nTotal books: {total_books}")
                print(f"Percentage read: {percent_read:.1f}%")
            else:
                print("\nYour library is empty")

        elif choice == "6":
            # Option 6: Save and Exit
            # Save current library state to file before exiting
            with open('library.txt', 'w') as f:
                import json
                # Convert library list to JSON string and save to file
                json.dump(library, f)
            print("Library saved to file. Goodbye!")
            break

        else:
            # Handle invalid menu choices
            print("Invalid choice. Please try again.")

# Program entry point
# This ensures main() only runs if script is run directly (not imported)
if __name__ == "__main__":
    main()
