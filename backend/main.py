from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel
from typing import Dict
from PIL import Image
import random
import io
import time
import os
# The following lines are for a real model. Uncomment them when you have one.
# import tensorflow as tf
# import numpy as np

# Initialize FastAPI app
app = FastAPI(title="PlantAI Backend API")

# --- REAL AI MODEL INTEGRATION ---
# This is where you will load your real model.
# In a real project, you would place your model file (e.g., plant_disease_model.h5)
# in the backend directory.
#
# try:
#     # Load the model from the backend directory
#     model = tf.keras.models.load_model("plant_disease_model.h5")
#     CLASS_NAMES = ["Healthy", "Leaf Rust", "Powdery Mildew", "Leaf Spot Disease"]
#     print("AI model loaded successfully!")
# except Exception as e:
#     print(f"Error loading AI model: {e}")
#     model = None


class PredictionResponse(BaseModel):
    disease: str
    confidence: float
    treatment: str

# --- Mock AI Model for the Backend ---
def mock_predict_plant_disease(image_bytes: bytes) -> Dict:
    # This is the mock function you are currently using.
    # It returns a random diagnosis and treatment plan for demonstration.
    diagnoses = [
        {
            "disease": "Leaf Spot Disease",
            "confidence": random.uniform(90.0, 99.9),
            "treatment": """
I see the leaf in the picture is affected by a fungal or bacterial disease – the brown spots with yellowish edges are common symptoms of leaf spot disease (often caused by fungi like Alternaria, Cercospora, or Colletotrichum).
Here are some simple solutions you can try:

### 🌱 Natural/Home Remedies:
- **Neem Spray:** Mix neem oil ($5$ ml) in $1$ liter of water with a few drops of soap. Spray on both sides of the leaves every $7$ days.
- **Baking Soda Spray:** Mix $1$ teaspoon baking soda + $1$ liter water + few drops of liquid soap. Spray on infected leaves to reduce fungal growth.
- **Garlic Extract:** Crush garlic, mix with water, filter, and spray on the plants. It acts as a natural antifungal.

### 🌿 Good Gardening Practices:
- Remove and destroy infected leaves (don’t compost them).
- Water at the base of the plant, not on the leaves.
- Give plants good spacing for airflow.
- Rotate crops (don’t grow the same plant in the same soil every season).

### 💊 If Natural Methods Fail (Chemical Option):
- Use a fungicide like Mancozeb, Chlorothalonil, or Copper oxychloride (follow instructions on the pack).
"""
        },
        {
            "disease": "Powdery Mildew",
            "confidence": random.uniform(90.0, 99.9),
            "treatment": """
I see the leaf has a powdery white or grayish coating on its surface, which is a classic symptom of Powdery Mildew, a common fungal disease.
Here are some simple solutions you can try:

### 🌱 Natural/Home Remedies:
- **Milk Spray:** Mix milk with water in a 1:1 ratio. The milk proteins have antifungal properties that can fight the mildew.
- **Baking Soda Spray:** Mix 1 teaspoon baking soda + 1 liter water + few drops of liquid soap. This is effective for reducing fungal growth.
- **Pruning:** Prune away and dispose of the most heavily affected leaves and stems to prevent the disease from spreading.

### 🌿 Good Gardening Practices:
- Improve air circulation by spacing plants appropriately.
- Water at the base of the plant to keep leaves dry.
- Avoid over-fertilizing with nitrogen, which promotes soft new growth that is susceptible to mildew.

### 💊 If Natural Methods Fail (Chemical Option):
- Use a fungicide containing sulfur or potassium bicarbonate (follow instructions on the pack).
"""
        },
        {
            "disease": "Leaf Rust",
            "confidence": random.uniform(90.0, 99.9),
            "treatment": """
The leaf in the picture shows small, rusty-brown spots or pustules, which are characteristic signs of Leaf Rust. This is a fungal disease that can reduce a plant’s ability to photosynthesize.
Here are some simple solutions you can try:

### 🌱 Natural/Home Remedies:
- **Neem Spray:** Mix neem oil ($5$ ml) in $1$ liter of water with a few drops of soap. Spray on both sides of the leaves every $7$ days.
- **Horticultural Oil:** Apply horticultural oil to the leaves. It can smother fungal spores and prevent them from spreading.
- **Copper Fungicide:** Natural copper fungicides are available and can be effective.

### 🌿 Good Gardening Practices:
- Remove and destroy infected leaves (don’t compost them).
- Water in the morning to allow leaves to dry out during the day.
- Ensure good air circulation around the plants.

### 💊 If Natural Methods Fail (Chemical Option):
- Use a systemic fungicide containing chlorothalonil or myclobutanil (follow instructions on the pack).
"""
        },
        {
            "disease": "Healthy",
            "confidence": random.uniform(98.0, 99.9),
            "treatment": """
Your plant looks healthy! I see no signs of common diseases. Keep up the good work.
To maintain your plant's health, make sure to follow these best practices:

### 🌿 Good Gardening Practices:
- Water at the base of the plant, not on the leaves, to prevent fungal growth.
- Give plants good spacing for airflow.
- Provide the right amount of light for your plant species.
- Use a balanced fertilizer as needed.
"""
        }
    ]

    try:
        time.sleep(2)  # Simulate a prediction delay

        prediction = random.choice(diagnoses)

        return {
            "disease": prediction["disease"],
            "confidence": round(prediction["confidence"], 2),
            "treatment": prediction["treatment"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# --- REAL AI MODEL PREDICTION FUNCTION ---
# This is the function that will use your real model.
# You will replace the 'mock_predict_plant_disease' call below with this.
# def real_predict_plant_disease(image_bytes: bytes) -> Dict:
#     if not model:
#         raise HTTPException(status_code=500, detail="AI model is not loaded.")
#
#     try:
#         image = Image.open(io.BytesIO(image_bytes))
#         image = image.resize((224, 224)) # Resize to match your model's input size
#         image_array = np.asarray(image)
#         image_array = np.expand_dims(image_array, axis=0) # Add batch dimension
#         image_array = image_array / 255.0 # Normalize the image
#
#         predictions = model.predict(image_array)
#         predicted_class = CLASS_NAMES[np.argmax(predictions)]
#         confidence = np.max(predictions) * 100
#
#         # You would need to create detailed treatments for each real class
#         treatment_plan = "This is a placeholder for a real treatment plan." 
#
#         return {
#             "disease": predicted_class,
#             "confidence": round(confidence, 2),
#             "treatment": treatment_plan
#         }
#     except Exception as e:
#         raise HTTPException(status_code=500, detail=f"Prediction failed: {str(e)}")


# Root endpoint
@app.get("/")
def read_root():
    return {"message": "PlantAI Backend API is running!"}

# Prediction endpoint
@app.post("/predict/", response_model=PredictionResponse)
async def predict(file: UploadFile = File(...)):
    if not file.content_type or not file.content_type.startswith("image/"):
        raise HTTPException(
            status_code=400,
            detail="Invalid file type. Please upload an image file."
        )

    contents = await file.read()
    
    # FOR NOW, WE USE THE MOCK FUNCTION.
    # WHEN YOU HAVE A REAL MODEL, REPLACE THE LINE BELOW:
    prediction = mock_predict_plant_disease(contents)
    
    return prediction
