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
uvicorn main:app --host 0.0.0.0 --port 8000