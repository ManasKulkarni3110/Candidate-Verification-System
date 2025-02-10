from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import sqlite3
import face_recognition
import numpy as np
import base64
import io
from PIL import Image
from typing import Optional
import uvicorn

# Initialize FastAPI app
app = FastAPI(title="Face Recognition API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Database configuration
DATABASE = 'candidates.db'

# Pydantic models for request validation
class CandidateRegister(BaseModel):
    name: str
    email: str
    image: str  # Base64 encoded image

class CandidateVerify(BaseModel):
    image: str  # Base64 encoded image

# Database connection helper
def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Helper function to process base64 image
def process_base64_image(base64_string: str) -> Optional[np.ndarray]:
    try:
        # Remove data URL prefix if present
        if ',' in base64_string:
            base64_string = base64_string.split(',')[1]
            
        # Decode base64 string
        image_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(image_data))
        
        # Convert to RGB
        image = image.convert('RGB')
        
        # Convert to numpy array
        return np.array(image)
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid image format: {str(e)}")

@app.post("/api/register")
async def register_candidate(candidate: CandidateRegister):
    try:
        # Process the image
        image_array = process_base64_image(candidate.image)
        
        # Get face encoding
        face_encoding = face_recognition.face_encodings(image_array)
        
        if len(face_encoding) == 0:
            raise HTTPException(status_code=400, detail="No face detected in the image")
        
        # Convert face encoding to bytes for storage
        face_encoding_bytes = face_encoding[0].tobytes()
        
        # Store in database
        conn = get_db_connection()
        cursor = conn.cursor()
        
        cursor.execute(
            'INSERT INTO candidates (name, email, face_encoding) VALUES (?, ?, ?)',
            (candidate.name, candidate.email, face_encoding_bytes)
        )
        
        conn.commit()
        conn.close()
        
        return {"message": "Candidate registered successfully"}
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/api/verify")
async def verify_candidate(verification: CandidateVerify):
    try:
        # Process the image
        image_array = process_base64_image(verification.image)
        
        # Get face encoding
        face_encoding = face_recognition.face_encodings(image_array)
        
        if len(face_encoding) == 0:
            raise HTTPException(status_code=400, detail="No face detected in the image")
        
        # Query database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM candidates')
        candidates = cursor.fetchall()
        conn.close()
        
        # Compare with stored encodings
        for candidate in candidates:
            stored_encoding = np.frombuffer(candidate['face_encoding'], dtype=np.float64)
            match = face_recognition.compare_faces([stored_encoding], face_encoding[0])[0]
            
            if match:
                return {
                    "message": "Candidate verified",
                    "name": candidate['name'],
                    "email": candidate['email']
                }
        
        raise HTTPException(status_code=404, detail="Candidate not found")
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)