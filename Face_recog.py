import streamlit as st
import cv2
import numpy as np
import face_recognition
from PIL import Image

def main():
    """
    Main function to run the Candidate Verification System.
    
    This function creates a Streamlit web application that allows users to:
    1. Upload an image of a candidate
    2. Capture an image from the webcam
    3. Compare the two images to verify the candidate's identity
    
    The application uses face recognition to compare the faces in both images.
    """
    st.title("Candidate Verification System")

    # File uploader for candidate's image
    uploaded_file = st.file_uploader("Upload candidate's image", type=["jpg", "png", "jpeg"])

    if uploaded_file is not None:
        # Display uploaded image
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", use_column_width=True)

        # Convert image to numpy array
        image_array = np.array(image)
        
        # Find face encodings for the uploaded image
        face_locations = face_recognition.face_locations(image_array)
        if len(face_locations) == 0:
            st.error("No face detected in the uploaded image. Please upload a clear image with a face.")
            return
        
        uploaded_face_encoding = face_recognition.face_encodings(image_array, face_locations)[0]

        # Webcam capture
        st.write("Click on 'Verify' when ready to capture from webcam")
        if st.button("Verify"):
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            cap.release()

            if ret:
                st.image(frame, channels="BGR", caption="Captured Image", use_column_width=True)
                
                # Find face encodings for the captured image
                face_locations = face_recognition.face_locations(frame)
                if len(face_locations) == 0:
                    st.error("No face detected in the captured image. Please try again.")
                    return
                
                captured_face_encoding = face_recognition.face_encodings(frame, face_locations)[0]

                # Compare face encodings
                results = face_recognition.compare_faces([uploaded_face_encoding], captured_face_encoding)

                if results[0]:
                    st.success("Verification Successful! The candidate's identity is confirmed.")
                else:
                    st.error("Verification Failed! The captured image does not match the uploaded candidate image.")
            else:
                st.error("Failed to capture image from webcam. Please check your camera and try again.")

def load_image(image_file):
    """
    Load an image file and convert it to a numpy array.
    
    Args:
    image_file (UploadedFile): The uploaded image file.
    
    Returns:
    numpy.ndarray: The image as a numpy array.
    """
    img = Image.open(image_file)
    return np.array(img)

def get_face_encoding(image):
    """
    Get the face encoding from an image.
    
    Args:
    image (numpy.ndarray): The input image as a numpy array.
    
    Returns:
    numpy.ndarray: The face encoding if a face is detected, None otherwise.
    """
    face_locations = face_recognition.face_locations(image)
    if len(face_locations) == 0:
        return None
    return face_recognition.face_encodings(image, face_locations)[0]

def capture_webcam_image():
    """
    Capture an image from the webcam.
    
    Returns:
    tuple: A tuple containing a boolean indicating success and the captured image (if successful).
    """
    cap = cv2.VideoCapture(0)
    ret, frame = cap.read()
    cap.release()
    return ret, frame

def compare_faces(known_face_encoding, unknown_face_encoding):
    """
    Compare two face encodings.
    
    Args:
    known_face_encoding (numpy.ndarray): The face encoding of the known person.
    unknown_face_encoding (numpy.ndarray): The face encoding of the person to verify.
    
    Returns:
    bool: True if the faces match, False otherwise.
    """
    results = face_recognition.compare_faces([known_face_encoding], unknown_face_encoding)
    return results[0]

if __name__ == "__main__":
    main()