#!/usr/bin/env python3
# backend/app.py
# Unified Flask backend – Full PDF Suite - PRODUCTION READY
# Fixes: Auto-detection, duplicate downloads, cross-platform support

import os
import uuid
import zipfile
import subprocess
import logging
import threading
import time
import mimetypes
import platform
import shutil
from pathlib import Path
from flask import Flask, request, send_file, jsonify, send_from_directory, make_response
from werkzeug.utils import secure_filename
from pdf2docx import Converter
from PyPDF2 import PdfReader, PdfWriter
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import io

# ---------------- CONFIG ----------------
BASE_DIR = Path(__file__).resolve().parent.parent
BACKEND_DIR = BASE_DIR / "backend"
FRONTEND_DIR = BASE_DIR / "frontend"
UPLOADS_DIR = BACKEND_DIR / "uploads"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)

ALLOWED_EXT = {'.doc', '.docx', '.pdf', '.odt', '.rtf', '.txt', '.xls', '.xlsx'}
MAX_CONTENT_LENGTH = 200 * 1024 * 1024  # 200 MB

# Auto-detect LibreOffice and Poppler paths
def find_libreoffice():
    """Find LibreOffice executable across different platforms"""
    system = platform.system()
    
    if system == "Windows":
        possible_paths = [
            r"C:\Program Files\LibreOffice\program\soffice.exe",
            r"C:\Program Files (x86)\LibreOffice\program\soffice.exe",
            os.path.expanduser(r"~\AppData\Local\Programs\LibreOffice\program\soffice.exe")
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    elif system == "Linux":
        # Try common Linux paths
        possible_paths = [
            "/usr/bin/libreoffice",
            "/usr/bin/soffice",
            "/usr/local/bin/libreoffice",
            "/opt/libreoffice/program/soffice"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
        # Try which command
        try:
            result = subprocess.run(['which', 'libreoffice'], capture_output=True, text=True)
            if result.returncode == 0:
                return result.stdout.strip()
        except:
            pass
    elif system == "Darwin":  # macOS
        possible_paths = [
            "/Applications/LibreOffice.app/Contents/MacOS/soffice",
            "/usr/local/bin/soffice"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    
    return None

def find_poppler():
    """Find Poppler binaries"""
    system = platform.system()
    
    if system == "Windows":
        possible_paths = [
            r"D:\poppler\Library\bin",
            r"C:\Program Files\poppler\bin",
            r"C:\poppler\bin"
        ]
        for path in possible_paths:
            if os.path.exists(path):
                return path
    else:
        # On Linux/Mac, pdftoppm should be in PATH
        if shutil.which('pdftoppm'):
            return None  # Use system PATH
    
    return None

LIBREOFFICE_CMD = find_libreoffice()
POPPLER_PATH = find_poppler()

# Logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("pdf-tools")

# Log configuration status
if LIBREOFFICE_CMD:
    logger.info(f"LibreOffice found at: {LIBREOFFICE_CMD}")
else:
    logger.warning("LibreOffice NOT FOUND - Word/Excel conversions will fail!")

if POPPLER_PATH:
    logger.info(f"Poppler found at: {POPPLER_PATH}")
else:
    logger.info("Using system Poppler (if available)")

app = Flask(__name__, static_folder=str(FRONTEND_DIR))
app.config['MAX_CONTENT_LENGTH'] = MAX_CONTENT_LENGTH


# ---------------- CORS ----------------
@app.after_request
def add_cors_headers(resp):
    resp.headers['Access-Control-Allow-Origin'] = '*'
    resp.headers['Access-Control-Allow-Methods'] = 'GET,POST,OPTIONS'
    resp.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    resp.headers['Access-Control-Expose-Headers'] = 'Content-Disposition'
    return resp


@app.route('/convert', methods=['OPTIONS'])
@app.route('/extract-images', methods=['OPTIONS'])
@app.route('/lock-pdf', methods=['OPTIONS'])
@app.route('/unlock-pdf', methods=['OPTIONS'])
@app.route('/add-page-numbers', methods=['OPTIONS'])
def handle_options():
    response = make_response()
    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'
    return response, 200


# ---------------- Serve Frontend ----------------
@app.route('/')
def serve_index():
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    return send_from_directory(str(BASE_DIR), 'index.html')
=======
    return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
=======
    return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
=======
    return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe

@app.route('/<path:path>')
def serve_static_files(path):
    full_path = FRONTEND_DIR / path
    if full_path.exists():
        return send_from_directory(FRONTEND_DIR, path)
    else:
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
        return send_from_directory(str(BASE_DIR), 'index.html')
=======
        return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
=======
        return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe
=======
        return send_from_directory(FRONTEND_DIR, 'index.html')
>>>>>>> 6f483ce856cce007036ca9bdb94c84f227f68abe


# ---------------- Utilities ----------------
def allowed_filename(fname):
    return Path(fname).suffix.lower() in ALLOWED_EXT


def libreoffice_convert(input_path: Path, output_dir: Path, target_ext: str):
    """Convert document using LibreOffice with error handling"""
    if not LIBREOFFICE_CMD:
        raise Exception("LibreOffice not installed or not found. Please install LibreOffice.")
    
    if not os.path.exists(LIBREOFFICE_CMD):
        raise Exception(f"LibreOffice not found at: {LIBREOFFICE_CMD}")
    
    filters = {
        'pdf': 'pdf:writer_pdf_Export',
        'docx': 'docx:"MS Word 2007 XML"',
        'odt': 'odt:"OpenDocument Text"',
        'txt': 'txt:Text',
        'rtf': 'rtf:Rich Text Format'
    }
    filter_opt = filters.get(target_ext, target_ext)
    cmd = [
        LIBREOFFICE_CMD,
        '--headless',
        '--convert-to', filter_opt,
        '--outdir', str(output_dir),
        str(input_path)
    ]
    logger.info("Running LibreOffice: %s", " ".join(cmd))
    
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=300)
    except subprocess.TimeoutExpired:
        raise Exception("Conversion timeout - file too large or complex")
    except Exception as e:
        raise Exception(f"LibreOffice conversion failed: {str(e)}")


def pdf_to_image(input_path: Path, output_dir: Path):
    """Convert PDF to images using Poppler"""
    out_prefix = output_dir / input_path.stem
    
    if platform.system() == "Windows" and POPPLER_PATH:
        cmd = [f"{POPPLER_PATH}\\pdftoppm.exe", "-png", str(input_path), str(out_prefix)]
    else:
        # Linux/Mac - use system pdftoppm
        cmd = ["pdftoppm", "-png", str(input_path), str(out_prefix)]
    
    logger.info("Running Poppler: %s", " ".join(cmd))
    
    try:
        return subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, timeout=180)
    except FileNotFoundError:
        raise Exception("Poppler not installed. Please install poppler-utils.")
    except subprocess.TimeoutExpired:
        raise Exception("PDF to image conversion timeout")
    except Exception as e:
        raise Exception(f"PDF to image conversion failed: {str(e)}")


def pdf_to_docx(input_path: Path, output_path: Path):
    try:
        logger.info("Converting PDF to DOCX using pdf2docx...")
        cv = Converter(str(input_path))
        cv.convert(str(output_path), start=0, end=None)
        cv.close()
        return True
    except Exception as e:
        logger.error("pdf2docx conversion failed: %s", e)
        return False


# ---------------- PDF ENCRYPTION/DECRYPTION ----------------
def lock_pdf(input_path: Path, output_path: Path, password: str, permissions: dict):
    try:
        logger.info("Encrypting PDF with password...")
        reader = PdfReader(str(input_path))
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        writer.encrypt(
            user_password=password,
            owner_password=password + "_owner",
            use_128bit=True,
            permissions_flag=(
                (1 << 2 if permissions.get('allow_printing', True) else 0) |
                (1 << 3 if permissions.get('allow_modifying', False) else 0) |
                (1 << 4 if permissions.get('allow_copying', True) else 0)
            )
        )
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info("PDF encrypted successfully")
        return True
    except Exception as e:
        logger.error("PDF encryption failed: %s", e)
        return False


def unlock_pdf(input_path: Path, output_path: Path, password: str):
    try:
        logger.info("Decrypting PDF...")
        reader = PdfReader(str(input_path))
        
        if reader.is_encrypted:
            if not reader.decrypt(password):
                logger.error("Incorrect password")
                return False, "Incorrect password"
        
        writer = PdfWriter()
        
        for page in reader.pages:
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info("PDF decrypted successfully")
        return True, "Success"
    except Exception as e:
        logger.error("PDF decryption failed: %s", e)
        return False, str(e)


# ---------------- EXTRACT IMAGES FROM PDF (ENHANCED) ----------------
def extract_images_from_pdf(input_path: Path, output_dir: Path):
    """Extract all images from PDF in their original format when possible"""
    try:
        logger.info("Extracting images from PDF...")
        reader = PdfReader(str(input_path))
        image_files = []
        
        for page_num, page in enumerate(reader.pages):
            try:
                if '/Resources' not in page or '/XObject' not in page['/Resources']:
                    continue
                    
                xObject = page['/Resources']['/XObject']
                
                for obj_name in xObject:
                    try:
                        obj = xObject[obj_name]
                        
                        if obj['/Subtype'] != '/Image':
                            continue
                        
                        # Get image dimensions
                        width = obj['/Width']
                        height = obj['/Height']
                        
                        # Get raw image data
                        data = obj.get_data()
                        
                        # Determine image format and extension
                        extension = 'png'
                        save_raw = False
                        
                        if '/Filter' in obj:
                            filter_type = obj['/Filter']
                            if isinstance(filter_type, list):
                                filter_type = filter_type[0]
                            
                            # JPEG images
                            if filter_type == '/DCTDecode':
                                extension = 'jpg'
                                save_raw = True
                                logger.info(f"Found JPEG image on page {page_num + 1}")
                            
                            # JPEG2000 images
                            elif filter_type == '/JPXDecode':
                                extension = 'jp2'
                                save_raw = True
                                logger.info(f"Found JPEG2000 image on page {page_num + 1}")
                            
                            # JBIG2 images (black and white)
                            elif filter_type == '/JBIG2Decode':
                                extension = 'jbig2'
                                save_raw = True
                                logger.info(f"Found JBIG2 image on page {page_num + 1}")
                            
                            # Flate/ZIP compressed images
                            elif filter_type in ['/FlateDecode', '/Fl']:
                                extension = 'png'
                                save_raw = False
                                logger.info(f"Found Flate compressed image on page {page_num + 1}")
                            
                            # LZW compressed images
                            elif filter_type == '/LZWDecode':
                                extension = 'png'
                                save_raw = False
                                logger.info(f"Found LZW compressed image on page {page_num + 1}")
                            
                            # CCITTFax (black and white fax)
                            elif filter_type in ['/CCITTFaxDecode', '/CCF']:
                                extension = 'tiff'
                                save_raw = True
                                logger.info(f"Found CCITT Fax image on page {page_num + 1}")
                        
                        image_filename = output_dir / f"page_{page_num + 1}_img_{len(image_files) + 1}.{extension}"
                        
                        # Try to save raw data first (preserves original format)
                        if save_raw:
                            try:
                                with open(image_filename, 'wb') as img_file:
                                    img_file.write(data)
                                image_files.append(image_filename)
                                logger.info(f"Extracted raw {extension.upper()}: {image_filename}")
                                continue
                            except Exception as raw_error:
                                logger.warning(f"Failed to save raw image, trying PIL: {raw_error}")
                        
                        # Use PIL to decode and save
                        try:
                            # Determine color mode
                            mode = "RGB"
                            if '/ColorSpace' in obj:
                                color_space = obj['/ColorSpace']
                                if isinstance(color_space, list):
                                    color_space = color_space[0]
                                
                                if color_space == '/DeviceRGB':
                                    mode = "RGB"
                                elif color_space == '/DeviceGray':
                                    mode = "L"
                                elif color_space == '/DeviceCMYK':
                                    mode = "CMYK"
                                elif color_space in ['/Indexed', '/ICCBased']:
                                    mode = "P"  # Palette mode
                            
                            # Create image from bytes
                            if mode == "CMYK":
                                img = Image.frombytes(mode, (width, height), data)
                                img = img.convert("RGB")
                                image_filename = output_dir / f"page_{page_num + 1}_img_{len(image_files) + 1}.png"
                            elif mode == "P":
                                # For palette/indexed images, save as PNG
                                img = Image.frombytes("RGB", (width, height), data)
                                image_filename = output_dir / f"page_{page_num + 1}_img_{len(image_files) + 1}.png"
                            else:
                                img = Image.frombytes(mode, (width, height), data)
                            
                            # Save with appropriate format
                            if extension == 'jpg':
                                img.save(image_filename, "JPEG", quality=95)
                            elif extension == 'tiff':
                                img.save(image_filename, "TIFF")
                            else:
                                img.save(image_filename, "PNG")
                            
                            image_files.append(image_filename)
                            logger.info(f"Extracted image using PIL: {image_filename}")
                        
                        except Exception as pil_error:
                            logger.warning(f"PIL extraction failed: {pil_error}")
                            
                            # Last resort: try to save as PNG with basic decoding
                            try:
                                # Try to interpret as RGB
                                if len(data) == width * height * 3:
                                    img = Image.frombytes("RGB", (width, height), data)
                                elif len(data) == width * height:
                                    img = Image.frombytes("L", (width, height), data)
                                else:
                                    # Calculate bytes per pixel
                                    bpp = len(data) // (width * height)
                                    if bpp == 4:
                                        img = Image.frombytes("RGBA", (width, height), data)
                                    else:
                                        raise ValueError(f"Cannot determine image format: {bpp} bytes per pixel")
                                
                                fallback_filename = output_dir / f"page_{page_num + 1}_img_{len(image_files) + 1}.png"
                                img.save(fallback_filename, "PNG")
                                image_files.append(fallback_filename)
                                logger.info(f"Extracted using fallback method: {fallback_filename}")
                            
                            except Exception as fallback_error:
                                logger.error(f"All extraction methods failed: {fallback_error}")
                                continue
                    
                    except Exception as obj_error:
                        logger.warning(f"Error processing image object '{obj_name}': {obj_error}")
                        continue
            
            except Exception as page_error:
                logger.warning(f"Error processing page {page_num + 1}: {page_error}")
                continue
        
        if not image_files:
            logger.warning("No images found in PDF")
        else:
            logger.info(f"Successfully extracted {len(image_files)} images")
        
        return image_files
        
    except Exception as e:
        logger.error(f"Image extraction failed: {e}", exc_info=True)
        return []


# ---------------- ADD PAGE NUMBERS ----------------
def add_page_numbers(input_path: Path, output_path: Path, position: str, start_number: int):
    try:
        logger.info("Adding page numbers to PDF...")
        reader = PdfReader(str(input_path))
        writer = PdfWriter()
        
        for page_num, page in enumerate(reader.pages):
            packet = io.BytesIO()
            can = canvas.Canvas(packet, pagesize=letter)
            
            page_width = float(page.mediabox.width)
            page_height = float(page.mediabox.height)
            
            if position == "bottom-center":
                x, y = page_width / 2, 30
            elif position == "bottom-right":
                x, y = page_width - 50, 30
            elif position == "bottom-left":
                x, y = 50, 30
            elif position == "top-center":
                x, y = page_width / 2, page_height - 30
            elif position == "top-right":
                x, y = page_width - 50, page_height - 30
            else:
                x, y = 50, page_height - 30
            
            can.setFont("Helvetica", 12)
            can.drawCentredString(x, y, str(page_num + start_number))
            can.save()
            
            packet.seek(0)
            overlay_pdf = PdfReader(packet)
            overlay_page = overlay_pdf.pages[0]
            page.merge_page(overlay_page)
            writer.add_page(page)
        
        with open(output_path, 'wb') as output_file:
            writer.write(output_file)
        
        logger.info("Page numbers added successfully")
        return True
    except Exception as e:
        logger.error(f"Adding page numbers failed: {e}")
        return False


# ---------------- CLEANUP HELPER ----------------
def schedule_cleanup(file_paths, delay=120):
    """Schedule file cleanup after a delay - increased to 2 minutes for slow downloads"""
    def cleanup():
        time.sleep(delay)
        for path in file_paths:
            try:
                if path.exists():
                    if path.is_file():
                        path.unlink()
                        logger.info(f"Deleted: {path}")
            except Exception as e:
                logger.warning(f"Cleanup failed for {path}: {e}")
    
    threading.Thread(target=cleanup, daemon=True).start()


# ---------------- HELPER FOR SENDING FILES ----------------
def send_file_with_headers(file_path, download_name=None):
    """Send file with proper headers for download - prevents duplicate dialog"""
    if not download_name:
        download_name = file_path.name
    
    # Detect mime type
    mime_type, _ = mimetypes.guess_type(str(file_path))
    if not mime_type:
        mime_type = 'application/octet-stream'
    
    # Use simple filename - let client handle it
    response = make_response(send_file(
        file_path,
        mimetype=mime_type,
        as_attachment=True,
        download_name=download_name
    ))
    
    # Minimal headers to prevent duplicate download dialog
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    
    return response


# ---------------- API ENDPOINTS ----------------
@app.route('/convert', methods=['POST'])
def convert():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error="Empty filename"), 400

    filename = secure_filename(file.filename)
    if not allowed_filename(filename):
        return jsonify(error="File type not allowed. Supported: DOCX, DOC, ODT, RTF, PDF, XLS, XLSX"), 400

    uid = uuid.uuid4().hex
    in_path = UPLOADS_DIR / f"{uid}_{filename}"
    
    try:
        file.save(str(in_path))
        logger.info(f"File saved: {in_path} ({in_path.stat().st_size} bytes)")
    except Exception as e:
        logger.error(f"Failed to save file: {e}")
        return jsonify(error=f"Failed to save file: {str(e)}"), 500

    target = request.form.get("target", "").lower()
    src_ext = in_path.suffix.lower()

    try:
        if target == "image":
            logger.info("Converting PDF to image...")
            result = pdf_to_image(in_path, UPLOADS_DIR)
            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8", errors="ignore")
                raise Exception(f"PDF to Image conversion failed: {error_msg}")
            
            images = list(UPLOADS_DIR.glob(f"{in_path.stem}*.png"))
            if not images:
                raise Exception("No images were generated")
            
            logger.info(f"Generated {len(images)} images")
            
            if len(images) > 1:
                zip_path = UPLOADS_DIR / f"{uid}_images.zip"
                with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    for img in images:
                        zipf.write(img, img.name)
                
                schedule_cleanup([in_path] + images + [zip_path])
                return send_file_with_headers(zip_path, f"{Path(filename).stem}_images.zip")
            
            schedule_cleanup([in_path] + images)
            return send_file_with_headers(images[0], f"{Path(filename).stem}.png")

        elif src_ext == ".pdf" and target == "docx":
            out_path = UPLOADS_DIR / f"{uid}_output.docx"
            logger.info(f"Converting PDF to DOCX: {in_path} -> {out_path}")
            
            if not pdf_to_docx(in_path, out_path):
                raise Exception("PDF to DOCX conversion failed")
            
            if not out_path.exists():
                raise Exception("Output DOCX file was not created")
            
            schedule_cleanup([in_path, out_path])
            return send_file_with_headers(out_path, f"{Path(filename).stem}.docx")

        else:
            # Word to PDF or other LibreOffice conversions
            if not LIBREOFFICE_CMD:
                raise Exception("LibreOffice not installed. Word/Excel conversion requires LibreOffice.")
            
            target_ext = "pdf" if src_ext != ".pdf" else "docx"
            logger.info(f"LibreOffice conversion: {in_path} -> {target_ext}")
            
            result = libreoffice_convert(in_path, UPLOADS_DIR, target_ext)
            if result.returncode != 0:
                error_msg = result.stderr.decode("utf-8", errors="ignore")
                raise Exception(f"LibreOffice conversion failed: {error_msg}")
            
            # Find output file
            possible_outputs = list(UPLOADS_DIR.glob(f"{in_path.stem}*.{target_ext}"))
            if not possible_outputs:
                # LibreOffice might use original filename
                possible_outputs = list(UPLOADS_DIR.glob(f"*{uid}*.{target_ext}"))
            
            if not possible_outputs:
                raise Exception(f"No output file found. LibreOffice may have failed silently.")
            
            out_file = possible_outputs[0]
            logger.info(f"Output file: {out_file} ({out_file.stat().st_size} bytes)")
            
            schedule_cleanup([in_path, out_file])
            return send_file_with_headers(out_file, f"{Path(filename).stem}.{target_ext}")

    except Exception as e:
        logger.error(f"Conversion failed: {e}", exc_info=True)
        schedule_cleanup([in_path])
        return jsonify(error=str(e)), 500


@app.route('/lock-pdf', methods=['POST'])
def lock_pdf_endpoint():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error="Empty filename"), 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith('.pdf'):
        return jsonify(error="Only PDF files allowed"), 400

    password = request.form.get("password", "")
    if not password or len(password) < 4:
        return jsonify(error="Password must be at least 4 characters"), 400

    permissions = {
        'allow_printing': request.form.get("allow_printing", "true").lower() == "true",
        'allow_modifying': request.form.get("allow_modifying", "false").lower() == "true",
        'allow_copying': request.form.get("allow_copying", "true").lower() == "true"
    }

    uid = uuid.uuid4().hex
    in_path = UPLOADS_DIR / f"{uid}_{filename}"
    out_path = UPLOADS_DIR / f"{uid}_locked.pdf"
    
    try:
        file.save(str(in_path))
        
        if not lock_pdf(in_path, out_path, password, permissions):
            return jsonify(error="Failed to encrypt PDF"), 500
        
        schedule_cleanup([in_path, out_path])
        return send_file_with_headers(out_path, filename.replace('.pdf', '_locked.pdf'))

    except Exception as e:
        logger.error("Lock PDF failed: %s", e)
        schedule_cleanup([in_path, out_path])
        return jsonify(error=f"Encryption failed: {str(e)}"), 500


@app.route('/unlock-pdf', methods=['POST'])
def unlock_pdf_endpoint():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error="Empty filename"), 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith('.pdf'):
        return jsonify(error="Only PDF files allowed"), 400

    password = request.form.get("password", "")
    if not password:
        return jsonify(error="Password is required"), 400

    uid = uuid.uuid4().hex
    in_path = UPLOADS_DIR / f"{uid}_{filename}"
    out_path = UPLOADS_DIR / f"{uid}_unlocked.pdf"
    
    try:
        file.save(str(in_path))
        
        success, message = unlock_pdf(in_path, out_path, password)
        if not success:
            schedule_cleanup([in_path])
            return jsonify(error=message), 400
        
        schedule_cleanup([in_path, out_path])
        return send_file_with_headers(out_path, filename.replace('.pdf', '_unlocked.pdf'))

    except Exception as e:
        logger.error("Unlock PDF failed: %s", e)
        schedule_cleanup([in_path, out_path])
        return jsonify(error=f"Decryption failed: {str(e)}"), 500


@app.route('/extract-images', methods=['POST'])
def extract_images_endpoint():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error="Empty filename"), 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith('.pdf'):
        return jsonify(error="Only PDF files allowed"), 400

    uid = uuid.uuid4().hex
    in_path = UPLOADS_DIR / f"{uid}_{filename}"
    
    try:
        file.save(str(in_path))
        logger.info(f"Saved PDF file: {in_path} ({in_path.stat().st_size} bytes)")
        
        # Extract images
        images = extract_images_from_pdf(in_path, UPLOADS_DIR)
        
        if not images:
            schedule_cleanup([in_path])
            return jsonify(error="No images found in PDF or extraction failed"), 404
        
        logger.info(f"Extracted {len(images)} images")
        
        if len(images) == 1:
            # Single image - return directly
            schedule_cleanup([in_path] + images)
            return send_file_with_headers(
                images[0], 
                f"{Path(filename).stem}_{images[0].stem}.{images[0].suffix[1:]}"
            )
        else:
            # Multiple images - create zip
            zip_path = UPLOADS_DIR / f"{uid}_images.zip"
            with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
                for idx, img in enumerate(images, 1):
                    # Rename for clarity
                    new_name = f"{Path(filename).stem}_image_{idx}{img.suffix}"
                    zipf.write(img, new_name)
                    logger.info(f"Added to zip: {new_name}")
            
            schedule_cleanup([in_path] + images + [zip_path])
            return send_file_with_headers(
                zip_path, 
                f"{Path(filename).stem}_images.zip"
            )

    except Exception as e:
        logger.error(f"Extract images failed: {e}", exc_info=True)
        if in_path.exists():
            schedule_cleanup([in_path])
        return jsonify(error=f"Extraction failed: {str(e)}"), 500


@app.route('/add-page-numbers', methods=['POST'])
def add_page_numbers_endpoint():
    if 'file' not in request.files:
        return jsonify(error="No file provided"), 400

    file = request.files['file']
    if not file.filename:
        return jsonify(error="Empty filename"), 400

    filename = secure_filename(file.filename)
    if not filename.lower().endswith('.pdf'):
        return jsonify(error="Only PDF files allowed"), 400

    position = request.form.get("position", "bottom-center")
    start_number = int(request.form.get("start_number", 1))

    uid = uuid.uuid4().hex
    in_path = UPLOADS_DIR / f"{uid}_{filename}"
    out_path = UPLOADS_DIR / f"{uid}_numbered.pdf"
    
    try:
        file.save(str(in_path))
        
        if not add_page_numbers(in_path, out_path, position, start_number):
            schedule_cleanup([in_path])
            return jsonify(error="Failed to add page numbers"), 500
        
        schedule_cleanup([in_path, out_path])
        return send_file_with_headers(out_path, filename.replace('.pdf', '_numbered.pdf'))

    except Exception as e:
        logger.error("Add page numbers failed: %s", e)
        schedule_cleanup([in_path, out_path])
        return jsonify(error=f"Failed to add page numbers: {str(e)}"), 500


@app.route('/status')
def status():
    """Status endpoint with detailed configuration info"""
    libreoffice_status = "✅ Installed" if LIBREOFFICE_CMD and os.path.exists(LIBREOFFICE_CMD) else "❌ Not Found"
    poppler_status = "✅ Available" if POPPLER_PATH or shutil.which('pdftoppm') else "❌ Not Found"
    
    return jsonify(
        status="ok",
        platform=platform.system(),
        libreoffice={
            "status": libreoffice_status,
            "path": LIBREOFFICE_CMD if LIBREOFFICE_CMD else "Not found"
        },
        poppler={
            "status": poppler_status,
            "path": POPPLER_PATH if POPPLER_PATH else "System PATH"
        },
        features={
            "word_to_pdf": "✅" if LIBREOFFICE_CMD else "❌",
            "pdf_to_word": "✅ PyPDF2 + pdf2docx",
            "pdf_to_image": "✅" if (POPPLER_PATH or shutil.which('pdftoppm')) else "❌",
            "excel_to_pdf": "✅" if LIBREOFFICE_CMD else "❌",
            "encryption": "✅ PyPDF2",
            "image_extraction": "✅ PyPDF2 + Pillow",
            "page_numbers": "✅ ReportLab"
        },
        upload_limit="200 MB",
        cleanup_delay="120 seconds"
    )


if __name__ == "__main__":
    logger.info("="*60)
    logger.info("Starting PDF Suite Tools Backend")
    logger.info("="*60)
    logger.info(f"Platform: {platform.system()}")
    logger.info(f"LibreOffice: {LIBREOFFICE_CMD if LIBREOFFICE_CMD else '❌ NOT FOUND'}")
    logger.info(f"Poppler: {POPPLER_PATH if POPPLER_PATH else 'System PATH' if shutil.which('pdftoppm') else '❌ NOT FOUND'}")
    logger.info("="*60)
    
    if not LIBREOFFICE_CMD:
        logger.warning("⚠️  LibreOffice NOT FOUND - Install LibreOffice for Word/Excel conversion")
    
    logger.info("Backend running at http://127.0.0.1:5000")
    logger.info("All PDF tools enabled")
    logger.info("Check /status endpoint for configuration details")
    app.run(host="0.0.0.0", port=5000, debug=True)