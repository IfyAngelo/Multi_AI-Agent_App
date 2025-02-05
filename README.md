# Multi AI-Agentic System from Scratch

This project provides a FastAPI multi ai-agentic tool for performing various tasks with AI agents. It was developed from scratch with pure python and zero framework. It is dockerized for easy deployment and scalability. The application provides endpoints for medical text summarization, article writing and refinement, sanitizing medical data (PHI removal), and more. This project is designed to run seamlessly with Docker.

Now, in addition to **OpenAI's GPT**, we have integrated **Groq LLM**, enabling more diverse AI-driven processing capabilities.

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

This project is a **Multi AI-Agentic** application designed to interact with AI agents to perform tasks such as:
- **Summarizing Medical Text**
- **Writing and Refining Research Articles**
- **Sanitizing Medical Data by Removing Protected Health Information (PHI)**

It uses **OpenAI's GPT** and **Groq** models to process and refine text for various use cases. The project is dockerized to make deployment easier and scalable.

---

## Technologies Used

- **FastAPI** - Web framework for building APIs
- **Docker** - Containerization for environment isolation and easier deployment
- **OpenAI** - For natural language processing tasks (summarization, writing, etc.)
- **Groq LLM** - Additional LLM for enchanced AI interactions
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
   OPEN_API_KEY="your-openai-key"
   GROQ_API_KEY="your-groq-key"
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
- **Description:** Summarize medical texts using the OpenAI or Groq LLM.
- **Input:**
```
{
  "text": "Enter medical text to summarize",
  "provider": "openai" // or "groq"
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
- **Description:** Write and refine research articles based on a provided topic and optional outline using OpenAI or Groq LLM.
- **Input:**
```
{
  "topic": "Research topic",
  "outline": "Optional outline for the article",
  "provider": "openai" // or "groq"
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
- **Description:** Sanitize medical data by removing Protected Health Information (PHI) using OpenAI or Groq LLM.
- **Input:**
```
{
  "medical_data": "Original medical data",
  "provider": "openai" // or "groq"
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
    "text": "Some medical text",
    "provider": "openai" // or "groq"
  }'
```

---

## Logging

The application uses the Loguru library for logging, which is configured to write logs to both the console and a log file. Logs are stored in the logs directory and can be useful for debugging.

---

## Error Handling

In case of errors, the system will return appropriate error messages with HTTP status codes. If there's an issue with the OpenAI API call, retries will be attempted based on the retry configuration. Any failures will be logged for review.

---

## Contributing

1. Fork the repository.
2. Clone your fork to your local machine.
3. Create a new branch for your feature or bug fix.
4. Commit your changes.
5. Push the branch to your forked repository.
6. Open a Pull Request to the main repository.

---

## License

This project is licensed under the MIT License. See the LICENSE file for details.

---