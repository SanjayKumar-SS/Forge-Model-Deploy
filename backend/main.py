import os
import json
import google.generativeai as genai
from fastapi import FastAPI, File, UploadFile
from typing import Dict
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

# Enable CORS
origins = ["*"]  # Allow all origins for development; restrict in production

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Folders
UPLOAD_FOLDER = "uploads"
BACKEND_FOLDER = "backend2"
GENERATED_FOLDER = "generated_code"
PROMPT_FOLDER = "prompts"

# Ensure all folders exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(BACKEND_FOLDER, exist_ok=True)
os.makedirs(GENERATED_FOLDER, exist_ok=True)
os.makedirs(PROMPT_FOLDER, exist_ok=True)

# Gemini API Setup
GENAI_API_KEY = "AIzaSyAgIR2l5qrSJe0YrgsUqVJvxfxJp8HWi18"
genai.configure(api_key=GENAI_API_KEY)
model = genai.GenerativeModel("gemini-2.0-flash-thinking-exp-1219")

# Function to save uploaded files
async def save_uploaded_file(file: UploadFile):
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as f:
        f.write(await file.read())
    return file_path

# Function to move .pkl file to backend2
def move_pkl_to_backend():
    for file in os.listdir(UPLOAD_FOLDER):
        if file.endswith(".pkl"):
            src = os.path.join(UPLOAD_FOLDER, file)
            dst = os.path.join(BACKEND_FOLDER, file)
            os.rename(src, dst)
            return dst
    return None

# Function to read `.ipynb` and convert it to JSON
def read_ipynb(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        return json.load(f)

# Function to get the correct prompt
def get_prompt(file_type):
    prompt_path = os.path.join(PROMPT_FOLDER, f"{file_type}_prompt.txt")
    if os.path.exists(prompt_path):
        with open(prompt_path, "r") as file:
            return file.read()
    return None

# Function to generate code using GenAI
def generate_code(file_type, ipynb_data):
    prompt = get_prompt(file_type)
    if not prompt:
        return {"error": f"Prompt for {file_type} not found"}

    full_prompt = f"{prompt}\n\nJupyter Notebook Data:\n{json.dumps(ipynb_data, indent=2)}"
    
    # Call Gemini API
    response = model.generate_content(full_prompt)
    generated_code = response.text.strip()

    # Determine file path
    filename = "output.py" if file_type == "backend" else "output.jsx"
    target_folder = BACKEND_FOLDER if file_type == "backend" else GENERATED_FOLDER
    file_path = os.path.join(target_folder, filename)

    # Save generated code
    with open(file_path, "w") as f:
        f.write(generated_code)

    return {"message": f"Generated {filename} successfully", "file_path": file_path}

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Code Generation API!"}

# Upload API
@app.post("/upload/")
async def upload_files(ipynb: UploadFile = File(...), pkl: UploadFile = File(...), dataset: UploadFile = File(...)):
    files = {"ipynb": ipynb, "pkl": pkl, "dataset": dataset}
    stored_files: Dict[str, str] = {}

    # Save all files in uploads/
    for key, file in files.items():
        file_path = os.path.join(UPLOAD_FOLDER, file.filename)
        with open(file_path, "wb") as f:
            f.write(await file.read())
        stored_files[key] = file_path

    # Move model.pkl to backend2
    pkl_dest = os.path.join(BACKEND_FOLDER, pkl.filename)
    os.rename(stored_files["pkl"], pkl_dest)
    stored_files["pkl"] = pkl_dest  # Update path

    return {"message": "Files uploaded successfully", "stored_files": stored_files}

# Generate API
@app.post("/generate/")
async def generate_code_from_ipynb():
    # Find latest uploaded Jupyter notebook
    ipynb_files = [f for f in os.listdir(UPLOAD_FOLDER) if f.endswith(".ipynb")]
    if not ipynb_files:
        return {"error": "No Jupyter notebook found in uploads/"}

    ipynb_path = os.path.join(UPLOAD_FOLDER, ipynb_files[-1])  # Get the latest file
    ipynb_data = read_ipynb(ipynb_path)

    # Generate backend and frontend code
    backend_result = generate_code("backend", ipynb_data)
    frontend_result = generate_code("frontend", ipynb_data)

    return {"backend": backend_result, "frontend": frontend_result}
