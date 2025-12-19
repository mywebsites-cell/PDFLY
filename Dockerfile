# Base Python image
FROM python:3.11-slim

ENV DEBIAN_FRONTEND=noninteractive

# Install LibreOffice (lean set), Poppler, and fonts
RUN apt-get update && apt-get install -y --no-install-recommends \
    libreoffice-writer libreoffice-calc libreoffice-impress libreoffice-draw libreoffice-core libreoffice-common \
    poppler-utils \
    fonts-dejavu-core fonts-dejavu-extra \
    && rm -rf /var/lib/apt/lists/*

# Work in /app and copy requirements
WORKDIR /app
COPY backend/requirements.txt /app/backend/requirements.txt
RUN pip install --no-cache-dir -r /app/backend/requirements.txt

# Copy full project (frontend + backend)
COPY . /app

# Render sets $PORT; expose for local runs
EXPOSE 10000

# Start with gunicorn using backend.app:app
CMD ["gunicorn", "backend.app:app", "--bind", "0.0.0.0:$PORT"]
