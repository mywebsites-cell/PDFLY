#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "==> Installing system dependencies..."
apt-get update
apt-get install -y libreoffice poppler-utils fonts-dejavu-core fonts-dejavu-extra

echo "==> Installing Python dependencies..."
pip install -r requirements.txt

echo "==> Verifying installations..."
if command -v libreoffice >/dev/null 2>&1; then
	echo "LibreOffice: $(libreoffice --version || true)"
else
	echo "LibreOffice not found in PATH"
fi
if command -v pdftoppm >/dev/null 2>&1; then
	echo "Poppler pdftoppm: $(pdftoppm -v 2>&1 | head -n 1)"
else
	echo "pdftoppm not found"
fi

echo "==> Build complete!"
