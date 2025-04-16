# Base Python image
FROM python:3.10-slim

# Set work directory
WORKDIR /app

# Copy code
COPY . .

# Install dependencies
RUN pip install --upgrade pip && pip install -r requirements.txt

# Expose port
EXPOSE 8000

# Run the app
CMD ["python", "main.py"]
