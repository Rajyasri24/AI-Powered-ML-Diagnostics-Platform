# AI-Powered ML Diagnostics Platform

## Live Demo

https://ai-powered-ml-diagnostics-platform.streamlit.app/

## Overview

AI-Powered ML Diagnostics Platform is a full-stack machine learning analysis and explainability platform that enables users to
- upload datasets,
- train multiple machine learning models,
-  compare performance,
-  generate explainability insights using SHAP,
-  and receive LLM-powered recommendations.
  
The platform combines FastAPI, Streamlit, Docker, Hugging Face LLMs, and cloud deployment to provide an end-to-end machine learning diagnostics workflow.

## Key Features

* User Authentication (Register/Login)
* Dataset Upload and Validation
* Automated ML Model Training
* Model Comparison Dashboard
* Performance Metrics Generation
* SHAP Explainability Visualizations
* Confusion Matrix Visualization
* LLM-Powered Diagnostic Recommendations
* Dockerized Architecture
* Cloud Deployment using Render and Streamlit Cloud

## Tech Stack

### Frontend
* Streamlit

### Backend
* FastAPI
* Uvicorn

### Machine Learning
* Scikit-Learn
* XGBoost
* SHAP

### Database
* SQLite

### AI Integration
* Hugging Face Inference API

### Deployment
* Docker
* Render
* Streamlit Community Cloud

## System Architecture
User Browser
→ Streamlit Frontend
→ FastAPI Backend
→ ML Engine + SHAP
→ Hugging Face LLM API
→ Results Returned

## Project Workflow
1. User uploads dataset.
2. Backend validates dataset.
3. ML models are trained.
4. Performance metrics are generated.
5. SHAP explainability is computed.
6. Confusion matrix is generated.
7. Hugging Face LLM provides diagnostic insights.
8. Results are displayed on dashboard.

## Deployment

Frontend:Streamlit Community Cloud
Backend: Render
Containerization: Docker

## Future Improvements

* PostgreSQL Integration
* MLflow Experiment Tracking
* DVC Dataset Versioning
* Model Registry
* CI/CD Pipelines
* Multi-user Project Management
* Cloud Object Storage
  
## Challenges Faced and Solutions

1. Frontend–Backend Communication in Docker : The application worked correctly on the local machine but failed when running inside Docker containers
   because the frontend attempted to access the backend using: http://127.0.0.1:8000
   Inside a container, localhost refers to the container itself rather than another service.

  *Solution* : Implemented environment-variable-based service discovery and used Docker networking to enable communication between frontend and backend containers.
  *Learning* : Understanding Docker networking and container-to-container communication.

2. SHAP and Confusion Matrix Images Not Displaying : Generated SHAP plots and confusion matrix images were visible locally but failed to appear consistently after containerization.

  *Solution* : Configured FastAPI static file serving and created static directories dynamically during runtime.
  *Learning* : Static asset management differs significantly between local development and containerized deployments.

3. Render Deployment Failure Due to Missing Static Folder : Backend deployment on Render failed because the Docker build attempted to execute :
   COPY static ./static
   However, Git does not track empty directories, causing the build to fail.

  *Solution* : Modified the Dockerfile to create the static directory dynamically using: 
               RUN mkdir -p static
              instead of copying generated files.
  *Learning* : Cloud deployments should generate runtime artifacts dynamically rather than relying on pre-generated assets.

4. Environment Variable Management : The application relied on Hugging Face API keys and secret keys stored in local `.env` files. These values are unavailable in cloud environments by default.

  *Solution* : Configured environment variables securely using Render and Streamlit Cloud settings.
  *Learning* : Production systems must separate secrets from source code and use secure environment configuration.

5. Missing Dependencies During Deployment : The deployed application failed due to missing libraries such as Plotly that were available locally but not installed in production.

  *Solution* : Reviewed runtime errors, updated requirements.txt, and rebuilt Docker images.
  *Key Learning* : A project should always have a complete and reproducible dependency specification.

6. Streamlit–Backend Connectivity Across Environments : The frontend needed to communicate with different backend URLs in local and production environments.

  *Solution* : Implemented configurable backend URLs using environment variables:
                BACKEND_URL = os.getenv(
                    "BACKEND_URL",
                    "http://127.0.0.1:8000"
                )
  *Learning* : Environment-specific configuration improves portability and deployment flexibility.

7. End-to-End Cloud Deployment : Deploying a multi-service architecture involving FastAPI, Streamlit, Docker, SHAP, SQLite, and Hugging Face APIs introduced integration challenges across multiple platforms.

  *Solution* : Successfully deployed the backend on Render and frontend on Streamlit Community Cloud while maintaining interoperability between services.
  *Key Learning* : Production deployment requires understanding networking, environment management, containerization, and cloud platform behavior beyond application development.

## Author
Rajyasri S
MSc Data Science | BE CSE
