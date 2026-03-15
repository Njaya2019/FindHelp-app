# Use Python 3.6 official image
FROM python:3.6-slim

# Install system dependencies required for building Python packages
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy code
COPY . /app

# Install dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Expose port for Render
EXPOSE 10000

# Run your Flask app
# At the end
COPY entrypoint.sh /app/entrypoint.sh

# Make it executable **inside the container**
RUN chmod +x /app/entrypoint.sh

CMD ["/app/entrypoint.sh"]
# CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:10000"]
