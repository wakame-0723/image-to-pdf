from flask import Flask, render_template, request, send_file
from PIL import Image
import os
import tempfile

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/convert', methods=['POST'])
def convert():
    files = request.files.getlist('images')

    if not files:
        return "画像がありません"

    images = []

    for file in files:
        img = Image.open(file.stream)

        if img.mode != "RGB":
            img = img.convert("RGB")

        images.append(img)

    # 一時PDF保存
    temp_pdf = os.path.join(tempfile.gettempdir(), "output.pdf")

    images[0].save(
        temp_pdf,
        save_all=True,
        append_images=images[1:]
    )

    return send_file(temp_pdf, as_attachment=True)

if __name__ == '__main__':
    app.run(debug=True)