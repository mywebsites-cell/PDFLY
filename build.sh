#!/bin/bash
set -e

echo "==> Installing system dependencies..."
apt-get update
apt-get install -y libreoffice poppler-utils

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Build complete!"
