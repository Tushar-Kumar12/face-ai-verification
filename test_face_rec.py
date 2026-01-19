import face_recognition
import numpy as np
from PIL import Image

# Create a simple test image (RGB, uint8)
test_image = np.zeros((100, 100, 3), dtype=np.uint8)
test_image[:, :] = [255, 0, 0]  # Red image

print("Test image shape:", test_image.shape)
print("Test image dtype:", test_image.dtype)

try:
    encodings = face_recognition.face_encodings(test_image)
    print("Success! Found", len(encodings), "face(s)")
except Exception as e:
    print("Error:", e)
    
# Try with a real image if available
try:
    img = Image.open("test.jpg") if False else None
except:
    pass
