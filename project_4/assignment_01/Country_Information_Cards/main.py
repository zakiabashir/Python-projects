# Import required libraries
import streamlit as st
import pandas as pd
import random

def main():
    # Set page configuration and title
    st.set_page_config(page_title="Country Information Cards", layout="wide")
    
    # Add a title with custom styling
    st.markdown("<h1 style='text-align: center;'>Country Information Cards</h1>", unsafe_allow_html=True)

    # Create a list of background colors and patterns
    bg_colors = ['#FFB6C1', '#98FB98', '#87CEEB', '#DDA0DD', '#F0E68C', 
                 '#FFA07A', '#98FF98', '#87CEFA', '#DDA0DD', '#F0E68C']
    
    bg_patterns = [
        'linear-gradient(45deg, #FFB6C1, #98FB98)',
        'radial-gradient(circle, #87CEEB, #DDA0DD)',
        'linear-gradient(135deg, #F0E68C, #FFA07A)',
        'linear-gradient(90deg, #98FF98, #87CEFA)',
        'radial-gradient(circle, #DDA0DD, #FFB6C1)'
    ]
    
    # Expanded list of countries with more options
    countries = ["United States", "United Kingdom", "Canada", "Australia", "Germany", 
                "France", "Japan", "China", "India", "Brazil", "Mexico", "Spain",
                "Italy", "Russia", "South Africa", "Pakistan", "Saudi Arabia", 
                "Turkey", "Egypt", "Nigeria", "Kenya", "Thailand", "Vietnam",
                "Indonesia", "Malaysia", "Singapore"]
    
    # Create columns for better layout
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Create a selectbox for country selection
        selected_country = st.selectbox("Select a Country", countries)
        
        # Generate random background style
        bg_style = random.choice([random.choice(bg_colors), random.choice(bg_patterns)])
        
        # Display country information in a card format with enhanced styling
        st.markdown(
            f"""
            <div style="
                padding: 25px;
                border-radius: 15px;
                background: {bg_style};
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                margin: 10px 0;
                transition: transform 0.3s ease;
            ">
                <h2 style="color: #333; margin-bottom: 15px;">{selected_country}</h2>
                <div style="background: rgba(255,255,255,0.7); padding: 15px; border-radius: 8px;">
                    <p style="font-size: 18px;"><strong>Capital:</strong> {get_capital(selected_country)}</p>
                    <p style="font-size: 18px;"><strong>Population:</strong> {get_population(selected_country)}</p>
                    <p style="font-size: 18px;"><strong>Region:</strong> {get_region(selected_country)}</p>
                    <p style="font-size: 18px;"><strong>Language:</strong> {get_language(selected_country)}</p>
                    <p style="font-size: 18px;"><strong>Currency:</strong> {get_currency(selected_country)}</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True
        )

def get_capital(country):
    # This is a placeholder function - in real app, would fetch from an API
    capitals = {
        "United States": "Washington, D.C.",
        "United Kingdom": "London",
        "Pakistan": "Islamabad",
        "India": "New Delhi"
        # Add more capitals as needed
    }
    return capitals.get(country, "Capital City")

def get_population(country):
    # This is a placeholder function - in real app, would fetch from an API
    populations = {
        "United States": "331 million",
        "United Kingdom": "67 million",
        "Pakistan": "220 million",
        "India": "1.38 billion"
        # Add more population data as needed
    }
    return populations.get(country, "Population Data")

def get_region(country):
    # This is a placeholder function - in real app, would fetch from an API
    regions = {
        "United States": "North America",
        "United Kingdom": "Europe",
        "Pakistan": "South Asia",
        "India": "South Asia"
        # Add more regions as needed
    }
    return regions.get(country, "Region Data")

def get_language(country):
    # New function to get primary language
    languages = {
        "United States": "English",
        "United Kingdom": "English",
        "Pakistan": "Urdu",
        "India": "Hindi, English"
        # Add more languages as needed
    }
    return languages.get(country, "Language Data")

def get_currency(country):
    # New function to get currency
    currencies = {
        "United States": "US Dollar (USD)",
        "United Kingdom": "Pound Sterling (GBP)",
        "Pakistan": "Pakistani Rupee (PKR)",
        "India": "Indian Rupee (INR)"
        # Add more currencies as needed
    }
    return currencies.get(country, "Currency Data")

if __name__ == "__main__":
    main()
