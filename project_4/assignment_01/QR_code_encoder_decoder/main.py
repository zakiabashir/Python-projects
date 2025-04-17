def main():
    # Import required libraries
    import streamlit as st
    import qrcode
    from PIL import Image
    import numpy as np
    import io
    import cv2  # Using OpenCV instead of pyzbar
    
    # Set page configuration and title
    st.set_page_config(page_title="QR Code Generator/Decoder", layout="wide")
    
    # Create a multicolor linear gradient background
    def set_bg_gradient():
        st.markdown(
            f"""
            <style>
            .stApp {{
                background: linear-gradient(45deg, #ff6b6b, #4ecdc4, #45b7d1);
                background-size: 200% 200%;
                animation: gradient 10s ease infinite;
            }}
            @keyframes gradient {{
                0% {{background-position: 0% 50%;}}
                50% {{background-position: 100% 50%;}}
                100% {{background-position: 0% 50%;}}
            }}
            </style>
            """,
            unsafe_allow_html=True
        )
    
    # Apply the gradient background
    set_bg_gradient()
    
    # Create main title with custom styling
    st.title("QR Code Generator and Decoder")
    
    # Create tabs for encoder and decoder
    tab1, tab2 = st.tabs(["Generate QR Code", "Decode QR Code"])
    
    # QR Code Generator Tab
    with tab1:
        # Input field for text/URL to encode
        data = st.text_input("Enter text or URL to generate QR Code")
        
        if st.button("Generate QR Code"):
            if data:
                try:
                    # Create QR code instance
                    qr = qrcode.QRCode(version=1, box_size=10, border=5)
                    # Add data to QR code
                    qr.add_data(data)
                    qr.make(fit=True)
                    # Create QR code image with custom colors
                    qr_image = qr.make_image(fill_color="black", back_color="white")
                    
                    # Convert PIL image to bytes
                    img_byte_arr = io.BytesIO()
                    qr_image.save(img_byte_arr, format='PNG')
                    img_byte_arr = img_byte_arr.getvalue()
                    
                    # Display the generated QR code
                    st.image(img_byte_arr, caption="Generated QR Code", use_container_width=False)
                    
                    # Add download button
                    st.download_button(
                        label="Download QR Code",
                        data=img_byte_arr,
                        file_name="qr_code.png",
                        mime="image/png"
                    )
                except Exception as e:
                    st.error(f"Error generating QR code: {str(e)}")
            else:
                st.warning("Please enter some text or URL")
    
    # QR Code Decoder Tab
    with tab2:
        # File uploader for QR code image
        uploaded_file = st.file_uploader("Upload QR Code Image", type=['jpg', 'png', 'jpeg'])
        
        if uploaded_file is not None:
            try:
                # Convert uploaded file to image
                file_bytes = np.asarray(bytearray(uploaded_file.read()), dtype=np.uint8)
                image = cv2.imdecode(file_bytes, cv2.IMREAD_COLOR)
                
                # Initialize QR code detector
                qr_detector = cv2.QRCodeDetector()
                
                # Detect and decode QR code
                data, bbox, _ = qr_detector.detectAndDecode(image)
                
                if data:
                    # Display decoded text
                    st.success(f"Decoded Content: {data}")
                    # Display uploaded image
                    st.image(uploaded_file, caption="Uploaded QR Code", use_container_width=False)
                else:
                    st.error("No QR Code found in the image")
            except Exception as e:
                st.error(f"Error decoding QR code: {str(e)}")

if __name__ == "__main__":
    # Run the Streamlit application
    main()
