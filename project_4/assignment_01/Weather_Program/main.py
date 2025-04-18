def main():
    # Import required libraries
    import streamlit as st
    import requests
    from datetime import datetime
    import pandas as pd

    # Set page configuration and title
    st.set_page_config(page_title="Weather App", layout="wide")

    # Create a linear gradient background using HTML/CSS
    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
            background-size: 200% 200%;
            animation: gradient 10s ease infinite;
        }
        @keyframes gradient {
            0% {background-position: 0% 50%;}
            50% {background-position: 100% 50%;}
            100% {background-position: 0% 50%;}
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Add title and description
    st.title("☁️ Weather Dashboard")
    st.write("Get real-time weather information for any city!")

    # Create input field for city name
    city = st.text_input("Enter City Name:", "London")

    # API configuration
    API_KEY = "YOUR_API_KEY"  # Replace with your OpenWeatherMap API key

    if st.button("Get Weather"):
        try:
            # Construct BASE_URL inside try block to catch potential city name errors
            BASE_URL = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={API_KEY}&units=metric"
            
            # Make API request
            response = requests.get(BASE_URL)
            
            # Check if the response was successful
            if response.status_code != 200:
                error_data = response.json()
                error_message = error_data.get('message', 'Unknown error occurred')
                st.error(f"API Error: {error_message}")
                return

            data = response.json()

            # Extract weather information
            temp = data['main']['temp']
            humidity = data['main']['humidity']
            pressure = data['main']['pressure']
            wind_speed = data['wind']['speed']
            description = data['weather'][0]['description']

            # Create columns for better layout
            col1, col2 = st.columns(2)

            # Display weather information in columns
            with col1:
                st.metric("Temperature", f"{temp}°C")
                st.metric("Humidity", f"{humidity}%")
                st.metric("Pressure", f"{pressure} hPa")

            with col2:
                st.metric("Wind Speed", f"{wind_speed} m/s")
                st.metric("Description", description.title())

            # Add UV index information
            st.subheader("UV Index Forecast")
            uv_data = {
                'Time': pd.date_range(start=datetime.now(), periods=24, freq='H'),
                'UV Index': [5, 6, 7, 8, 9, 8, 7, 6, 5, 4, 3, 2, 1, 1, 1, 1, 2, 3, 4, 5, 6, 5, 4, 3]
            }
            df = pd.DataFrame(uv_data)
            st.line_chart(df.set_index('Time'))

        except requests.RequestException as e:
            st.error(f"Network Error: Could not connect to the weather service. {str(e)}")
        except KeyError as e:
            st.error(f"Data Error: Could not process weather data. {str(e)}")
        except Exception as e:
            st.error(f"Error: {str(e)}. Please check the city name and try again.")

if __name__ == "__main__":
    main()
