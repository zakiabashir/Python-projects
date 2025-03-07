import streamlit as st
import pandas as pd
import numpy as np
import io
import json
import xml.etree.ElementTree as ET
import csv
from PIL import Image

st.set_page_config(page_title="DataSweeper - File Converter", layout="wide")

st.title("DataSweeper - Universal File Converter")
st.write("Convert between multiple file formats easily!")

# Supported formats
input_formats = ["CSV", "Excel", "JSON", "XML", "TXT"]
output_formats = ["CSV", "Excel", "JSON", "XML", "TXT"]

# Sidebar
st.sidebar.title("Settings")
input_format = st.sidebar.selectbox("Select Input Format", input_formats)
output_format = st.sidebar.selectbox("Select Output Format", output_formats)

# File uploader
uploaded_file = st.file_uploader(f"Upload your {input_format} file", type=[format.lower() for format in input_formats])

if uploaded_file is not None:
    try:
        # Read input file based on format
        if input_format == "CSV":
            df = pd.read_csv(uploaded_file)
        elif input_format == "Excel":
            df = pd.read_excel(uploaded_file)
        elif input_format == "JSON":
            df = pd.read_json(uploaded_file)
        elif input_format == "XML":
            xml_data = ET.parse(uploaded_file)
            root = xml_data.getroot()
            data = []
            for child in root:
                data.append({subchild.tag: subchild.text for subchild in child})
            df = pd.DataFrame(data)
        elif input_format == "TXT":
            df = pd.read_csv(uploaded_file, sep="\t")

        # Display preview
        st.subheader("Preview of uploaded data")
        st.dataframe(df.head())

        # Convert and download
        if st.button("Convert"):
            st.subheader("Converted File")
            
            if output_format == "CSV":
                output = df.to_csv(index=False)
                mime = "text/csv"
                ext = "csv"
            elif output_format == "Excel":
                output = io.BytesIO()
                df.to_excel(output, index=False)
                mime = "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
                ext = "xlsx"
            elif output_format == "JSON":
                output = df.to_json(orient="records")
                mime = "application/json"
                ext = "json"
            elif output_format == "XML":
                output = df.to_xml(index=False)
                mime = "application/xml"
                ext = "xml"
            elif output_format == "TXT":
                output = df.to_csv(sep="\t", index=False)
                mime = "text/plain"
                ext = "txt"

            # Create download button
            if output_format == "Excel":
                output.seek(0)
                st.download_button(
                    label="Download converted file",
                    data=output.read(),
                    file_name=f"converted.{ext}",
                    mime=mime
                )
            else:
                st.download_button(
                    label="Download converted file",
                    data=output,
                    file_name=f"converted.{ext}",
                    mime=mime
                )

    except Exception as e:
        st.error(f"An error occurred: {str(e)}")
        st.write("Please make sure you've selected the correct input format and the file is valid.")

# Add some helpful information
st.sidebar.markdown("---")
st.sidebar.subheader("Supported Operations")
st.sidebar.write("• CSV ↔ Excel")
st.sidebar.write("• JSON ↔ XML")
st.sidebar.write("• TXT ↔ CSV")

# Footer
st.markdown("---")
st.markdown("Made with ❤️ by Zakia Bashir")
