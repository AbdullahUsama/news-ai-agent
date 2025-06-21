# Use a slim Python base image
FROM python:3.13.1

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application code
COPY . .

# Expose the port FastAPI will run on
EXPOSE 80

# Command to run the FastAPI application with Uvicorn
# Use Gunicorn with Uvicorn workers for production for better concurrency
# For simplicity, Uvicorn directly is fine for initial free deployments.
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]