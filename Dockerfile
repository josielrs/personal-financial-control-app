# Use an official ubuntu image
FROM ubuntu:24.04

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file into the container at /app
COPY requirements.txt .

# Install important packages to use
RUN apt-get update && \
    apt-get install -y --no-install-recommends \
    python3-dev python3 python3-pip python3.12-venv build-essential libcairo2-dev pkg-config python3-wheel \
    libgirepository-2.0-dev && \
    rm -rf /var/lib/apt/lists/*

# Copy the rest of the application code into the container at /app
COPY . .    

# Install any needed packages specified in requirements.txt
RUN pip install --break-system-packages -r requirements.txt

# Expose the port that Flask will run on
EXPOSE 5000

# Define environment variable for Flask
ENV FLASK_APP=app.py

# environment commands
CMD ["flask", "run", "--host=0.0.0.0", "--port=5000"]