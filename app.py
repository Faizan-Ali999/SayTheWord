from flask import Flask, render_template, request
import pytesseract
from PIL import Image
import os
import json

pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

app = Flask(__name__)
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def index():
    text = ""
    boxes = []
    filename = ""
    if request.method == 'POST':
        image = request.files['image']
        filename = image.filename
        path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        image.save(path)

        img = Image.open(path)

        # Extract text and word-level box info
        data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)
        n_boxes = len(data['level'])
        for i in range(n_boxes):
            if int(data['conf'][i]) > 60:  # Confidence threshold
                word_info = {
                    'text': data['text'][i],
                    'left': data['left'][i],
                    'top': data['top'][i],
                    'width': data['width'][i],
                    'height': data['height'][i]
                }
                boxes.append(word_info)

    return render_template('index.html', filename=filename, boxes=json.dumps(boxes))

if __name__ == '__main__':
    app.run(debug=True)
