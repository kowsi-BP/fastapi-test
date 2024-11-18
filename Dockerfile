# Use an official Python runtime as a parent image
FROM python:3.9.6-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port that the app will run on
EXPOSE 80

# Command to run the application with Uvicorn
ENTRYPOINT ["uvicorn", "model_app:app", "--host", "0.0.0.0", "--port", "80"]



