
# prompt: create a unit converter app code which have run on streamlite and make this application on python 

import streamlit as st

def convert_temperature(value, from_unit, to_unit):
    """Converts temperature between Celsius, Fahrenheit, and Kelvin."""

    if from_unit == to_unit:
        return value

    if from_unit == "Celsius":
        if to_unit == "Fahrenheit":
            return (value * 9/5) + 32
        elif to_unit == "Kelvin":
            return value + 273.15
    elif from_unit == "Fahrenheit":
        if to_unit == "Celsius":
            return (value - 32) * 5/9
        elif to_unit == "Kelvin":
            return (value - 32) * 5/9 + 273.15
    elif from_unit == "Kelvin":
        if to_unit == "Celsius":
            return value - 273.15
        elif to_unit == "Fahrenheit":
            return (value - 273.15) * 9/5 + 32
    else:
        return "Invalid unit"


def convert_length(value, from_unit, to_unit):
    """Converts length between meters, feet, inches, and centimeters."""

    conversion_factors = {
      "meters": 1,
      "feet": 3.28084,
      "inches": 39.3701,
      "centimeters": 100,
    }
    if from_unit not in conversion_factors or to_unit not in conversion_factors:
      return "Invalid unit"
    return value * (conversion_factors[from_unit] / conversion_factors[to_unit])

st.title("Unit Converter")

st.sidebar.header("Conversion Type")
conversion_type = st.sidebar.selectbox("Select conversion type", ["Temperature", "Length"])


if conversion_type == "Temperature":
    st.header("Temperature Converter")
    value = st.number_input("Enter temperature value", value=0.0)
    from_unit = st.selectbox("From Unit", ["Celsius", "Fahrenheit", "Kelvin"])
    to_unit = st.selectbox("To Unit", ["Celsius", "Fahrenheit", "Kelvin"])
    
    if st.button("Convert"):
        converted_value = convert_temperature(value, from_unit, to_unit)
        st.write(f"{value} {from_unit} is equal to {converted_value} {to_unit}")


elif conversion_type == "Length":
    st.header("Length Converter")
    value = st.number_input("Enter length value", value=0.0)
    from_unit = st.selectbox("From Unit", ["meters", "feet", "inches", "centimeters"])
    to_unit = st.selectbox("To Unit", ["meters", "feet", "inches", "centimeters"])

    if st.button("Convert"):
        converted_value = convert_length(value, from_unit, to_unit)
        st.write(f"{value} {from_unit} is equal to {converted_value} {to_unit}")
