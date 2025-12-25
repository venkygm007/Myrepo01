# Use an official Python runtime as a parent image
FROM python:3.11-slim

# Set the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY . /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install gunicorn

# Make port 5000 available to the world outside this container
EXPOSE 5000

# Run gm_app.py using gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "gm_app:app"]
