# ⏰ Countdown Timer

A sleek and user-friendly countdown timer application built with Streamlit. This application provides a simple interface to set and run countdown timers with hours, minutes, and seconds.

## Features

- 🎨 Clean and modern gradient background
- ⚡ Real-time countdown display
- 🎯 Input validation for hours (0-23), minutes (0-59), and seconds (0-59)
- 🎉 Celebratory animation when timer completes
- 💫 Responsive design with custom styling

## Requirements

To run this application, you need to have the following installed:
- Python 3.x
- Streamlit

You can install the required package using uv:
```bash
uv add streamlit
```

## How to Run

1. Save the code in a file named `main.py`
2. Open your terminal/command prompt
3. Navigate to the directory containing the file
4. Run the application using:
```bash
streamlit run main.py
```

## Usage

1. Enter the desired time using the number input fields:
   - Hours (0-23)
   - Minutes (0-59)
   - Seconds (0-59)
2. Click the "Start Timer" button to begin the countdown
3. The timer will display in HH:MM:SS format
4. When the timer reaches zero, a "Time's Up!" message will appear with a celebration animation

## Features Explained

### Custom Styling
The application features a beautiful gradient background and custom-styled components:
- Main background: Gradient from light gray to blue-gray
- Timer input section: Semi-transparent white background
- Countdown display: Semi-transparent green background
- Completion message: Semi-transparent pink background

### Real-time Updates
The timer updates every second, providing a smooth countdown experience with clear, readable digits in a HH:MM:SS format.

### Completion Celebration
When the timer reaches zero, the application:
- Displays a "Time's Up!" message
- Changes the display background color
- Triggers a balloon animation

## Technical Implementation

The application is built using:
- `streamlit` for the web interface
- Python's built-in `time` module for countdown functionality
- Custom CSS for styling and visual effects

The code is structured with a main function that handles:
1. UI setup and styling
2. User input collection
3. Timer logic and display
4. Completion animations

## License

This project is open source and available for personal and commercial use.

## Contributing

Feel free to fork this project and submit pull requests for any improvements you'd like to add!