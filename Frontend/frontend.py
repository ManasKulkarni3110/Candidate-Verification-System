import streamlit as st
import requests
import base64
from PIL import Image
import io

# Configure page settings
st.set_page_config(
    page_title="Face Recognition System",
    page_icon="👤",
    layout="centered"
)

# Update the API URL to match FastAPI's default port
API_URL = "http://localhost:8000"

def convert_image_to_base64(image):
    # Convert PIL Image to base64 string
    buffered = io.BytesIO()
    image.save(buffered, format="JPEG")
    img_str = base64.b64encode(buffered.getvalue()).decode()
    return f"data:image/jpeg;base64,{img_str}"

def main():
    st.title("Face Recognition System")
    
    # Create tabs for Register and Verify
    tab1, tab2 = st.tabs(["Register", "Verify"])
    
    # Registration Tab
    with tab1:
        st.header("Register New Candidate")
        
        # Input fields
        name = st.text_input("Full Name")
        email = st.text_input("Email Address")
        
        # File uploader for image
        uploaded_file = st.file_uploader("Upload Face Image", type=['jpg', 'jpeg', 'png'], key="register")
        
        if uploaded_file is not None:
            # Display the uploaded image
            image = Image.open(uploaded_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Register button
            if st.button("Register Candidate"):
                if name and email:
                    # Convert image to base64
                    img_base64 = convert_image_to_base64(image)
                    
                    # Prepare data for API
                    data = {
                        "name": name,
                        "email": email,
                        "image": img_base64
                    }
                    
                    try:
                        # Make API request
                        response = requests.post(f"{API_URL}/api/register", json=data)
                        
                        if response.status_code == 200:
                            st.success("Candidate registered successfully!")
                        else:
                            error_detail = response.json().get('detail', 'Registration failed')
                            st.error(f"Error: {error_detail}")
                    except requests.exceptions.ConnectionError:
                        st.error("Failed to connect to the server. Please ensure the backend is running.")
                else:
                    st.warning("Please fill in all fields")
    
    # Verification Tab
    with tab2:
        st.header("Verify Candidate")
        
        # File uploader for verification
        verify_file = st.file_uploader("Upload Face Image", type=['jpg', 'jpeg', 'png'], key="verify")
        
        if verify_file is not None:
            # Display the uploaded image
            image = Image.open(verify_file)
            st.image(image, caption="Uploaded Image", use_column_width=True)
            
            # Verify button
            if st.button("Verify Identity"):
                # Convert image to base64
                img_base64 = convert_image_to_base64(image)
                
                # Prepare data for API
                data = {
                    "image": img_base64
                }
                
                try:
                    # Make API request
                    response = requests.post(f"{API_URL}/api/verify", json=data)
                    
                    if response.status_code == 200:
                        result = response.json()
                        st.success("Candidate Verified!")
                        st.write(f"Name: {result['name']}")
                        st.write(f"Email: {result['email']}")
                    elif response.status_code == 404:
                        st.warning("Candidate not found in the database.")
                    else:
                        error_detail = response.json().get('detail', 'Verification failed')
                        st.error(f"Error: {error_detail}")
                except requests.exceptions.ConnectionError:
                    st.error("Failed to connect to the server. Please ensure the backend is running.")

if __name__ == "__main__":
    main()