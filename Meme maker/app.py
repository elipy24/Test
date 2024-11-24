from flask import Flask, render_template, request, send_file
from PIL import Image, ImageDraw, ImageFont
import os

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/customize', methods=['POST'])
def customize():
    # Get text and image from the form
    top_text = request.form['top_text']
    bottom_text = request.form['bottom_text']
    uploaded_file = request.files['image']

    # Open the uploaded image or default one
    if uploaded_file:
        img_path = os.path.join(UPLOAD_FOLDER, uploaded_file.filename)
        uploaded_file.save(img_path)
    else:
        img_path = 'static/meme.png'

    # Customize the image
    with Image.open(img_path) as img:
        draw = ImageDraw.Draw(img)
        font = ImageFont.truetype('arial.ttf', size=30)

        # Add text
        draw.text((10, 10), top_text, font=font, fill="white")
        draw.text((10, img.height - 40), bottom_text, font=font, fill="white")

        # Save the customized image
        output_path = os.path.join(UPLOAD_FOLDER, 'customized.png')
        img.save(output_path)

    return send_file(output_path, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)
    
