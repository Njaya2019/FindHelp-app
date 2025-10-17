# Use Python 3.6 official image
FROM python:3.6-slim

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
CMD ["gunicorn", "run:app", "--bind", "0.0.0.0:10000"]
