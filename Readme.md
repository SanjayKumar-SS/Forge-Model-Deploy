# Forge Model Deploy (FMD)

## Introduction
Forge Model Deploy (FMD) is an automated and no-code deployment platform for machine learning models. It simplifies the process of deploying models by generating both the backend and frontend automatically. Users can upload their Jupyter Notebook (`.ipynb`), model weights (`.pkl`), and dataset (`.csv` or `.xlsx`), and the system generates a complete deployment-ready environment.

## Features
- **Automated Backend & Frontend Generation**: Uses GenAI to create API endpoints and a UI for interaction.
- **No-Code Deployment**: Enables users to deploy ML models without writing any code.
- **File Upload Support**: Accepts `.ipynb`, `.pkl`, and dataset files for model deployment.
- **Localhost Hosting**: Runs the generated application locally for testing and validation.
- **AWS Integration** (Upcoming): Plans to extend support for cloud-based hosting.

## How It Works
1. **Upload Model Files**: Users upload their `.ipynb`, `.pkl`, and dataset files.
2. **Generation Process**: The system processes the files and generates:
   - `output.py` (backend)  
   - `output.jsx` (frontend)
3. **Local Deployment**: The generated application is hosted on a local server.
4. **User Interaction**: Users can interact with the deployed model via the UI.

## Installation
To run the project locally, follow these steps:

```bash
git clone https://github.com/your-username/forge-model-deploy.git
cd forge-model-deploy
