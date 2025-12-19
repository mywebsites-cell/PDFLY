#!/bin/bash
set -e
export DEBIAN_FRONTEND=noninteractive

echo "==> Installing system dependencies (lean LibreOffice + Poppler)..."
mkdir -p /var/lib/apt/lists/partial || true
chmod 755 /var/lib/apt/lists/partial || true
apt-get clean
apt-get update
apt-get install -y --no-install-recommends \
	libreoffice-writer libreoffice-calc libreoffice-impress libreoffice-draw libreoffice-core libreoffice-common \
	fonts-dejavu-core fonts-dejavu-extra \
	poppler-utils
apt-get clean
rm -rf /var/lib/apt/lists/*

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
