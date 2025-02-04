# Use official Python image as base
FROM python:3.10

# Set working directory inside container
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy FastAPI application files
COPY . .

# Copy the .env file into the container
COPY .env .env

# Check if the .env file is copied correctly
RUN cat .env

# Expose the port FastAPI runs on
EXPOSE 8000

# Start FastAPI using Gunicorn with Uvicorn workers
CMD ["gunicorn", "-k", "uvicorn.workers.UvicornWorker", "-w", "4", "-b", "0.0.0.0:8000", "main:app"]
