from flask import Flask, render_template, request, flash
from werkzeug.utils import secure_filename
from PIL import Image, UnidentifiedImageError
import pytesseract
import os
import json
from datetime import datetime
import io

app = Flask(__name__)
app.secret_key = 'your_secret_key'
app.config['UPLOAD_FOLDER'] = 'static/uploads'

# ✅ Set path to tesseract executable (update if different on your machine)
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

@app.route('/', methods=['GET', 'POST'])
def index():
    boxes = []
    filename = ""

    if request.method == 'POST':
        # Get the last non-empty uploaded file (in case both inputs use name="image")
        uploaded_files = request.files.getlist('image')
        uploaded_file = next((f for f in reversed(uploaded_files) if f and f.filename), None)

        if not uploaded_file:
            flash("❌ Error: No file selected.")
            return render_template('index.html', filename=None, boxes=None)

        # Use secure or fallback filename
        filename = secure_filename(uploaded_file.filename)
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"camera_upload_{timestamp}.jpg"

        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)

        try:
            image_bytes = uploaded_file.read()
            img = Image.open(io.BytesIO(image_bytes))
            img = img.convert("RGB")  # Ensure compatibility
            img.save(path)  # Save for rendering
        except UnidentifiedImageError:
            flash("❌ Error: The uploaded file is not a valid image or may be corrupted.")
            return render_template('index.html', filename=None, boxes=None)
        except Exception as e:
            flash(f"❌ Unexpected error while reading image: {str(e)}")
            return render_template('index.html', filename=None, boxes=None)

        # OCR with Tesseract
        try:
            data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        except pytesseract.TesseractNotFoundError:
            flash("❌ Error: Tesseract is not installed or not available in PATH.")
            return render_template('index.html', filename=None, boxes=None)

        n_boxes = len(data['level'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60 and data['text'][i].strip():
                boxes.append({
                    'text': data['text'][i],
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                })

    return render_template('index.html', filename=filename, boxes=json.dumps(boxes))


if __name__ == '__main__':
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    app.run(host='0.0.0.0', port=5000, debug=True)
