FROM python:3.6-slim

# Install system dependencies + Postgres
RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev \
    postgresql \
    postgresql-contrib \
    build-essential \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Create non-root user "postgresuser"
RUN useradd -ms /bin/bash postgresuser
USER postgresuser
ENV PATH="/home/postgresuser/.local/bin:${PATH}"
WORKDIR /home/postgresuser/app

# Copy app code
COPY --chown=postgresuser:postgresuser . /home/postgresuser/app

# Install Python dependencies
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Add to Dockerfile after pip install requirements.txt
# RUN pip install gunicorn

# Expose Flask port
EXPOSE 10000

# Copy entrypoint script
COPY --chown=postgresuser:postgresuser entrypoint.sh /home/postgresuser/app/entrypoint.sh
RUN chmod +x /home/postgresuser/app/entrypoint.sh

# Start everything
CMD ["/home/postgresuser/app/entrypoint.sh"]