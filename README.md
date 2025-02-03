# FastAPI Dockerized Application

This project provides a FastAPI web application for performing various tasks with AI agents. It is dockerized for easy deployment and scalability. The application provides endpoints for medical text summarization, article writing and refinement, sanitizing medical data (PHI removal), and more. This project is designed to run seamlessly with Docker.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Technologies Used](#technologies-used)
- [Setup Instructions](#setup-instructions)
  - [Prerequisites](#prerequisites)
  - [Installation](#installation)
  - [Running the Application](#running-the-application)
  - [Docker](#docker)
- [API Endpoints](#api-endpoints)
  - [Summarize Medical Text](#summarize-medical-text)
  - [Write and Refine Research Articles](#write-and-refine-research-articles)
  - [Sanitize Medical Data (PHI Removal)](#sanitize-medical-data-phi-removal)
- [Testing](#testing)
  - [Postman](#postman)
- [Logging](#logging)
- [Error Handling](#error-handling)
- [Contributing](#contributing)
- [License](#license)

---

## Project Overview

This project is a **FastAPI** application designed to interact with AI agents to perform tasks such as:
- **Summarizing Medical Text**
- **Writing and Refining Research Articles**
- **Sanitizing Medical Data by Removing Protected Health Information (PHI)**

It uses **OpenAI's GPT** models to process and refine text for various use cases. The project is dockerized to make deployment easier and scalable.

---

## Technologies Used

- **FastAPI** - Web framework for building APIs
- **Docker** - Containerization for environment isolation and easier deployment
- **OpenAI** - For natural language processing tasks (summarization, writing, etc.)
- **Python** - Programming language
- **Loguru** - Logging library
- **Uvicorn** - ASGI server for FastAPI

---

## Setup Instructions

### Prerequisites

Before you can run this project, make sure you have the following installed:

- **Python 3.10+** - Required to run the FastAPI application.
- **Docker** - For containerization.
- **Git** - To clone the repository.

### Installation

1. Clone the repository:

   ```
   git clone https://github.com/your-username/fastapi-dockerized.git
   cd fastapi-dockerized
2. Install Python dependencies in a virtual environment (optional, but recommended):
   ```
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
3. Create a .env file with the necessary environment variables (e.g., OpenAI API key):

   ```
   OPEN_API_KEY = "your key in string format"
---

## Running the Application

### Running Locally

To run the FastAPI application locally without Docker, use the following command:
```
uvicorn app:app --reload
```
The application will be accessible at http://127.0.0.1:8000.

### Running with Docker

To run the application using Docker:

1. Build the Docker image:
```
docker build -t fastapi-app .
```
NB: fastapi-app is the image app name
2. Run the Docker container:
```
docker run -d -p 8000:8000 --env-file .env --name fastapi-container fastapi-app
```
NB: fastapi-container is the container name which is changeable.

The FastAPI application will be accessible at http://localhost:8000.

---

## API Endpoints

### Summarize Medical Texts

- **Endpoint:** /summarize
- **Method:** POST
- **Description:** Summarize medical texts using the OpenAI API.
- **Input:**
```
{
  "text": "Enter medical text to summarize"
}
```
- **Output:**
```
{
  "summary": "Summarized medical text."
}
```

### Write and Refine Research Articles

- **Endpoint:** /write_and_refine
- **Method:** POST
- **Description:** Write and refine research articles based on a provided topic and optional outline.
- **Input:**
```
{
  "topic": "Research topic",
  "outline": "Optional outline for the article"
}
```
- **Output:**
```
{
  "draft": "Draft article content",
  "refined_article": "Refined article content"
}
```

### Sanitize Medical Data (PHI Removal)

- **Endpoint:** /sanitize
- "Method": POST
- **Description:** Sanitize medical data by removing Protected Health Information (PHI).
- **Input:**
```
{
  "medical_data": "Original medical data"
}
```
- **Output:**
```
{
  "sanitized_data": "Sanitized medical data"
}
```

---

### Testing

To test the FastAPI endpoints, you can use tools like Postman or curl. Here's how to test the /summarize endpoint:

1. Postman:
    - Set the request type to POST.
    - Set the endpoint to `http://localhost:8000/summarize`.
    - In the body, select "raw" and choose JSON.
    - Send the text parameter as a JSON object.
2. Curl:
```
curl -X 'POST' \
  'http://localhost:8000/summarize' \
  -H 'Content-Type: application/json' \
  -d '{
    "text": "Some medical text"
  }'
```

---

## Logging