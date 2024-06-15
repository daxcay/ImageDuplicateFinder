import threading
import json
import shutil
import urllib.parse
import time
import random
import string
import os
import webview
from glob import glob
from PIL import Image
import numpy as np
from threading import Thread
import multiprocessing
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
THREAD_COUNT = 8
base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input,outputs=base_model.get_layer('avg_pool').output)
images_folder_progress = 0
dupprogress = 0
processess = []

def copy_files(src_dir, dest_dir):
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)

def move_files(src_dir, dest_dir, delete_source=False):
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.move(item_path, dest_dir)

    if (delete_source):
        shutil.rmtree(src_dir)


def dhash(image, hash_size=8):

    image = image.convert('L').resize(
        (hash_size + 1, hash_size),
        Image.LANCZOS,
    )

    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = image.getpixel((col, row))
            pixel_right = image.getpixel((col + 1, row))
            difference.append(pixel_left > pixel_right)

    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2**(index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)


def extract_features(image_path):
    try:
        img = Image.open(image_path).resize((224, 224))
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        features = model.predict(img_array)
        img_hash = dhash(img)
        return features.flatten(), img_hash
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None, None


def find_duplicates(folder_path):

    global dupprogress

    if not os.path.exists(folder_path):
        print(f"The provided folder path {folder_path} does not exist.")
        return

    images = glob(os.path.join(folder_path, '*'))
    print(f'Found {len(images)} files in {folder_path}.')

    lock = threading.Lock()
    features_list = {}
    duplicates_dict = {}

    for idx, img_path in enumerate(images):
        features, img_hash = extract_features(img_path)
        if features is None:
            continue
        with lock:
            is_duplicate = False
            for original_img_path, (f, h) in features_list.items():
                esimilarity = euclidean_distances([features], [f])[0][0]
                csimilarity = cosine_similarity([features], [f])[0][0]
                if esimilarity < 0.5 or csimilarity > 0.95 or img_hash == h:
                    is_duplicate = True
                    duplicates_dict.setdefault(os.path.basename(
                        original_img_path), []).append(os.path.basename(img_path))
                    break
            if not is_duplicate:
                features_list[img_path] = (features, img_hash)
        dupprogress = (idx + 1) * 100 // len(images)

    print(f'Finished processing {folder_path}.')

    with open(os.path.join(folder_path, 'duplicates.json'), 'w') as json_file:
        json.dump(duplicates_dict, json_file, indent=4)


def load_image_data(work_folder):

    data_path = os.path.join(work_folder, 'duplicates.json')
    if not os.path.exists(data_path):
        return
    with open(data_path, 'r') as f:
        image_data = json.load(f)

    encoded_image_data = {}
    for original_image, duplicate_images in image_data.items():
        encoded_original_image = urllib.parse.quote(original_image)
        encoded_duplicate_images = [urllib.parse.quote(
            image_path) for image_path in duplicate_images]
        encoded_image_data[encoded_original_image] = encoded_duplicate_images
    return encoded_image_data


def prepare_files(images_folder, work_folder, backup_folder):
    global images_folder_progress
    files = []
    for item in os.listdir(images_folder):
        item_path = os.path.join(images_folder, item)
        if os.path.isfile(item_path):
            files.append(item)
    total_files = len(files)
    for idx, file in enumerate(files):
        source_path = os.path.join(images_folder, file)
        unique_name = f"{time.time_ns()}-{generate_random_string()}.jpg"
        shutil.copy(source_path, os.path.join(work_folder, unique_name))
        shutil.copy(source_path, os.path.join(backup_folder, file))
        os.remove(source_path)
        images_folder_progress = (idx + 1) * 100 // total_files


def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def open_folder(folder_path):
    try:
        if os.name == 'nt':
            os.startfile(folder_path)  # Opens folder in Windows
        elif os.name == 'posix':
            os.system(f'xdg-open "{folder_path}"')  # Opens folder in Linux
        elif os.name == 'darwin':
            os.system(f'open "{folder_path}"')  # Opens folder in macOS
        return jsonify({'status': 'success', 'message': 'Folder opened successfully.'})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)})

# assets directory setup


@app.route('/assets/<path:filename>')
def assets(filename):
    return send_from_directory('assets', filename)

# page routes


@app.route('/')
def page_main():
    return render_template('index.html')


@app.route('/result')
def page_result():
    images_folder = request.args.get('images_folder')
    images_work_folder = os.path.join(images_folder, 'work')
    image_data = load_image_data(images_work_folder)
    return render_template('result.html', image_data=image_data, images_work_folder=images_work_folder, images_folder=images_folder)


@app.route('/images/<path:filename>')
def serve_image(filename):
    images_work_folder = request.args.get('images_work_folder')
    return send_from_directory(images_work_folder, filename)


@app.route('/reset')
def page_reset():
    return render_template('reset.html')

# api routes


@app.route('/images_folder', methods=['POST'])
def api_submit_image_folder():
    images_folder = request.form['images_folder']
    if os.path.exists(images_folder) and os.path.isdir(images_folder):
        images_work_folder = os.path.join(images_folder, 'work')
        images_backup_folder = os.path.join(images_folder, 'backup')
        if os.path.exists(images_backup_folder):
            if os.path.exists(images_work_folder):
                global images_folder_progress
                images_folder_progress = 100
                return jsonify({'status': 'success', 'success': 'Reading folder'})
            else:
                files = []
                for item in os.listdir(images_folder):
                    item_path = os.path.join(images_folder, item)
                    if os.path.isfile(item_path):
                        files.append(item)
                copy_files(images_backup_folder, images_work_folder)
                return jsonify({'status': 'success', 'success': 'Reading folder'})
        else:
            os.makedirs(images_work_folder, exist_ok=True)
            os.makedirs(images_backup_folder, exist_ok=True)
            prepare_files(images_folder, images_work_folder, images_backup_folder)
            return jsonify({'status': 'success', 'success': 'Reading folder'})
    else:
        return jsonify({'status': 'error', 'error': 'Error in reading folder'})


@app.route('/images_folder')
def api_images_folder_progress():
    global images_folder_progress
    return jsonify({'progress': images_folder_progress})


@app.route('/find_duplicates', methods=['POST'])
def finddup():
    global dupprogress
    dupprogress = 0
    images_folder = request.form['images_folder']
    images_work_folder = os.path.join(images_folder, 'work')
    data_path = os.path.join(images_work_folder, 'duplicates.json')
    if os.path.exists(data_path):
        dupprogress = 100
        return jsonify({'status': 'success'})
    thread = Thread(target=find_duplicates, args=(images_work_folder,))
    thread.start()
    return jsonify({'status': 'success'})


@app.route('/find_duplicates')
def get_dup_progress():
    global dupprogress
    return jsonify({'progress': dupprogress})

@app.route('/delete_duplicates', methods=['POST'])
def delete_duplicates():
    images_folder = request.form['images_folder']
    images_work_folder = os.path.join(images_folder, 'work')
    duplicate_images = request.form.getlist('duplicate_images[]')
    for image in duplicate_images:
        image_path = os.path.join(images_work_folder, image)
        if os.path.exists(image_path):
            os.remove(image_path)
    data_path = os.path.join(images_work_folder, 'duplicates.json')
    if os.path.exists(data_path):
        os.remove(data_path)
    move_files(images_work_folder, images_folder, delete_source=True)
    return jsonify({'status': "success"})

@app.route('/open_folder', methods=['POST'])
def open_folder():
    images_folder = request.form['images_folder']
    open_folder(images_folder)
    return jsonify({'status': "success"})

def start_flask():
    app.run(debug=False, port=5501)

def on_closed():
    global app_window
    app_window.destroy()
    global processess
    for process in processess:
        process.terminate()

if __name__ == '__main__':
    
    process = multiprocessing.Process(target=start_flask)
    process.start()
    processess.append(process)

    app_window = webview.create_window("Image Duplicate Finder", "http://localhost:5501", width=1280, height=720, resizable=True, confirm_close=True)
    app_window.events.closed += on_closed
    webview.start(debug=False)
