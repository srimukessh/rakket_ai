FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy requirements first for better caching
COPY requirements.txt .

# Install dependencies
RUN pip install -r requirements.txt

# Copy the application files
COPY youtube_summariser.py .
COPY youtube_summariser_app.py .

# Expose port 8080
EXPOSE 8080

# Command to run the application
CMD streamlit run youtube_summariser_app.py \
    --server.port 8080 \
    --server.address 0.0.0.0 