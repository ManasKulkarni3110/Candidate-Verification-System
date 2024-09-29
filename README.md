# Candidate-Verification-System

## Description
The Streamlit Face Verification App is a robust and user-friendly application designed for secure identity verification using facial recognition technology. This app combines the power of Streamlit for a seamless user interface, ChromaDB for efficient storage and retrieval of facial embeddings, and state-of-the-art facial recognition algorithms to provide a reliable verification system.

## Key Features
- **User Authentication**: Secure login system using user ID and password.
- **Real-time Facial Verification**: Captures and verifies user faces in real-time using webcam integration.
- **Vector Database Integration**: Utilizes ChromaDB for efficient storage and querying of facial embeddings.
- **User-Friendly Interface**: Built with Streamlit for an intuitive and responsive user experience.
- **Secure Password Handling**: Implements password hashing for enhanced security.

## Technologies Used
- **Python**: Core programming language
- **Streamlit**: Web application framework for the user interface
- **OpenCV**: For webcam image capture
- **face_recognition**: Library for facial recognition and encoding
- **ChromaDB**: Vector database for storing and querying facial embeddings
- **Pandas**: For handling user data
- **NumPy**: For numerical operations on arrays

## How It Works
1. **User Login**: Users authenticate using their unique user ID and password.
2. **Facial Capture**: Upon successful authentication, the app captures the user's face via webcam.
3. **Face Encoding**: The captured image is processed to extract facial features.
4. **Database Comparison**: The extracted facial features are compared against stored embeddings in ChromaDB.
5. **Verification Result**: The app provides immediate feedback on whether the verification was successful.

## Code Structure
- **ChromaDB Initialization**: Sets up the ChromaDB client and creates/gets the face embeddings collection.
- **User Authentication**: Includes functions for password hashing and user verification.
- **Facial Recognition**: Implements functions for capturing webcam images and extracting face encodings.
- **Main Application Flow**: Streamlit-based UI for user interaction and verification process.

## Installation and Setup
1. Clone the repository:
   ```
   git clone https://github.com/your-username/streamlit-face-verification.git
   ```
2. Install required dependencies:
   ```
   pip install streamlit opencv-python-headless numpy face_recognition Pillow chromadb pandas
   ```
3. Run the Streamlit app:
   ```
   streamlit run app.py
   ```

## Usage
1. Start the application using the command above.
2. Enter your user ID and password in the login form.
3. Upon successful authentication, click the "Capture Image" button.
4. The app will use your webcam to capture an image and verify it against stored embeddings.
5. The verification result will be displayed on the screen.

## Future Enhancements
- Multi-factor authentication support
- Integration with external identity verification services
- Support for multiple facial angles and expressions
- Admin panel for managing user data and system settings
