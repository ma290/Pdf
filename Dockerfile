FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Copy project files
COPY . .

# Create virtual environment inside the container
RUN python -m venv /opt/venv

# Activate the virtualenv and install dependencies
RUN . /opt/venv/bin/activate && pip install --upgrade pip && pip install -r requirements.txt

# Set environment variable to use the virtualenv's Python and pip
ENV PATH="/opt/venv/bin:$PATH"

# Expose Gradio port
EXPOSE 8000

# Run app
CMD ["python", "main.py"]
