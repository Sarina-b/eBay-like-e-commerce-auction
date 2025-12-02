# We use Python 3.10 because your pycache showed cpython-310
FROM python:3.10-slim

# Prevent Python from writing .pyc files and buffering stdout
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Set work directory
WORKDIR /app

# Install system dependencies required for Pillow (Image processing)
# libjpeg-dev and zlib1g-dev are crucial for image uploads in your auction site
RUN apt-get update && apt-get install -y \
    libjpeg-dev \
    zlib1g-dev \
    gcc \
    libc-dev \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copy the entire project into the container
COPY . /app/

# Expose the port Django runs on
EXPOSE 8000

# Start the server
# 0.0.0.0 is required to make it accessible outside the container
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
