import os
from flask import Flask, render_template, flash, redirect, url_for, request
from flask_bootstrap import Bootstrap
from werkzeug.utils import secure_filename
from PIL import Image
import numpy as np


app = Flask(__name__)
Bootstrap(app)

UPLOAD_FOLDER = "static/uploads/"
app.secret_key = "YOUR-SECRET-KEY"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])


def allowed_file(filename):
    return '-' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/")
def first_page():
    return render_template("index.html")


@app.route("/", methods=["POST"])
def upload_image():
    if 'file' not in request.files:
        flash('No file part')
        return redirect(request.url)
    file = request.files['file']
    if file.filename == "":
        flash('No image selected for uploading')
        return redirect(request.url)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        print("upload image filename: " + filename)
        flash('Image successfully uploaded and displayed below')
        image = Image.open(f"static/uploads/{filename}")
        print(np.array(image))
        colours = 255 - np.array(image)
        unique_rows = np.unique(colours[0], axis=0)
        unique_colors = np.random.choice(unique_rows[0], size=(10,3))
        result = tuple(map(tuple, unique_colors))
        return render_template("index.html", colours=result, filename=filename)
    else:
        flash('Allowed image types are -> png, jpg, jpeg, gif')
        return redirect(request.url)


@app.route("/display/<filename>")
def display_image(filename):
    print("display_image filename: " + filename)
    return redirect(url_for("static", filename="uploads/" + filename), code=301)


if __name__ == "__main__":
    app.run(debug=True)


