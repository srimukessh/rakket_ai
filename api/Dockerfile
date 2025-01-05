# Use the official Python image
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy the app files
COPY . .

# Expose ports for both apps
EXPOSE 8000 8501

# Install a process manager (e.g., supervisor)
RUN apt-get update && apt-get install -y supervisor && apt-get clean

# Add Supervisor configuration
COPY supervisord.conf /etc/supervisor/conf.d/supervisord.conf

# Run Supervisor to manage both apps
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisor/conf.d/supervisord.conf"]