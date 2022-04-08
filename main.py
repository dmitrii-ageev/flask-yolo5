#!/usr/bin/env python3

# importing the sys module and adding path to yolo5 modules
import os
from flask import Flask, render_template, request, redirect, \
    url_for, abort, send_from_directory, jsonify
import imghdr
from werkzeug.utils import secure_filename
from PIL import Image
import torch
import cv2
import numpy as np
import base64

# Constants
YOLO_GIT_REPO = 'ultralytics/yolov5'
UPLOADS_PATH = 'uploads'
TEMPLATE_FILE = 'index.html'
# NOTE: Provide path to the model if you'd like to use the custom one.
# Like this: MODEL_PATH = './models/model.pt'
MODEL_PATH = ''
MAX_PAYLOAD = 4096*4096

# Flask application settings
app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = MAX_PAYLOAD
app.config['IMAGE_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = UPLOADS_PATH


def init_model(model):
    # load the model
    if MODEL_PATH == '':
        return torch.hub.load(YOLO_GIT_REPO, 'yolov5s')
    else:
        return torch.hub.load(YOLO_GIT_REPO, 'custom',
                              path=MODEL_PATH, force_reload=True)


def validate_image_header(header):
    format = imghdr.what(None, header[:512])
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')


def validate_image(stream):
    header = stream.read(512)  # 512 bytes should be enough for a header check
    stream.seek(0)  # reset stream pointer
    return(validate_image_header(header))


def process_image(image, save_file=False):
    results = MODEL([image])
    if save_file:
        results.render()  # updates results.imgs with boxes and labels
        result = Image.fromarray(results.imgs[0])
        result.save(image)
        return redirect(url_for('index'))
    else:
        data = results.pandas().xyxy[0].to_dict('dict')
        number_of_objects = len(data['class'])
        result = list(dict())
        for index in range(number_of_objects):
            result.append(dict())
            for key in data.keys():
                result[index][key] = data[key][index]
        return jsonify(result)


@app.route('/')
def index():
    files = os.listdir(app.config['UPLOAD_PATH'])
    images = list()
    for filename in files:
        file_ext = os.path.splitext(filename)[1]
        if file_ext in app.config['IMAGE_EXTENSIONS']:
            images.append(filename)
    return render_template(TEMPLATE_FILE, files=images)


@app.route('/', methods=['POST'])
def upload_files():
    uploaded_file = request.files['file']
    filename = secure_filename(uploaded_file.filename)
    if filename != '':
        file_ext = os.path.splitext(filename)[1]
        if file_ext not in app.config['IMAGE_EXTENSIONS'] or \
                file_ext != validate_image(uploaded_file.stream):
            abort(422)
        uploaded_file_path = os.path.join(app.config['UPLOAD_PATH'], filename)
        uploaded_file.save(uploaded_file_path)
        return process_image(uploaded_file_path, save_file=True)
    return redirect(url_for('index'))


@app.route('/' + UPLOADS_PATH + '/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


@app.route('/api/inspect_image', methods=['POST'])
def inspect_image():
    if request.is_json:
        content = request.json
        if 'body' in content.keys() and 'name' in content.keys():
            if len(content['body']) < 512 or \
               len(content['body']) > MAX_PAYLOAD:
                # Fail with 'Unprocessable entity'
                abort(422)

            # Trying to decode the image body
            try:
                image_body = base64.standard_b64decode(content['body'])
            except Exception:
                abort(422)

            image_name = content['name']
            image_ext = os.path.splitext(image_name)[1]
            if image_ext not in app.config['IMAGE_EXTENSIONS'] or \
                    image_ext != validate_image_header(image_body):
                abort(415)

            image = cv2.imdecode(np.asarray(bytearray(image_body), dtype="uint8"), cv2.IMREAD_COLOR)
            return process_image(image)
    # Fail with 'Unsupported Media Type' error
    abort(415)


if __name__ == '__main__':
    MODEL = init_model(MODEL_PATH)
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='0.0.0.0')