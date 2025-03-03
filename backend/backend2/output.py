from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import pickle

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load model and handle potential errors
try:
    with open("model.pkl", "rb") as model_file:
        model = pickle.load(model_file)
except FileNotFoundError:
    raise Exception("Model file 'model.pkl' not found. Please ensure it exists in the same directory.")
except Exception as e:
    raise Exception(f"Error loading the model: {e}")

# Define input data model using Pydantic
class PredictionRequest(BaseModel):
    Age: float
    Height: float
    Weight: float

@app.get("/")
async def root():
    return {"message": "Prediction API is running"}

@app.get("/metadata")
async def metadata():
    # Assuming the model expects 'Age', 'Height', 'Weight' as input features based on the notebook
    input_fields = ["Age", "Height", "Weight"]
    model_type = "Classification"  # RandomForestClassifier is a classification model
    return {"input_fields": input_fields, "model_type": model_type}

@app.post("/predict")
async def predict(request_data: PredictionRequest):
    try:
        # Prepare input features for prediction
        features = [[
            request_data.Age,
            request_data.Height,
            request_data.Weight
        ]]

        prediction_array = model.predict(features)
        prediction = prediction_array.tolist()

        # Assuming label encoder was used and we want to inverse transform to get original class name
        # If you need to inverse transform, you'd need to load the label encoder as well
        # and apply inverse_transform here. For now, we return the numerical prediction.

        return {"input": request_data.dict(), "prediction": prediction[0]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")