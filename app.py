import threading
import json
import shutil
import urllib.parse
import time
import random
import string
import os
from glob import glob
from PIL import Image
import numpy as np
from threading import Thread
import webbrowser
from tensorflow.keras.applications.resnet50 import ResNet50, preprocess_input
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.models import Model
from sklearn.metrics.pairwise import euclidean_distances, cosine_similarity
from flask import Flask, render_template, request, jsonify, send_from_directory

app = Flask(__name__)
THREAD_COUNT = 8
base_model = ResNet50(weights='imagenet')
model = Model(inputs=base_model.input, outputs=base_model.get_layer('avg_pool').output)
images_folder_progress = 0
dupprogress = 0
dupprogresstext = "0/0"
errors = []
stop_thread = False

def copy_files(src_dir, dest_dir, delete_source=False):
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        if os.path.isfile(item_path):
            shutil.copy(item_path, dest_dir)
            if delete_source:
                os.remove(item_path)

def move_files(src_dir, dest_dir, delete_source=False):
    for item in os.listdir(src_dir):
        item_path = os.path.join(src_dir, item)
        dest_path = os.path.join(dest_dir, item)
        if os.path.isfile(item_path):
            if os.path.exists(dest_path):
                os.remove(dest_path)
            shutil.move(item_path, dest_dir)

    if delete_source:
        shutil.rmtree(src_dir)

def clean_folder(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path):
                os.remove(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")

def dhash(image, hash_size=8):
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.LANCZOS)
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
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0

    return ''.join(hex_string)

def extract_features(image_path):
    try:
        img = Image.open(image_path).resize((224, 224))
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img_array = img_to_array(img)
        img_array = np.expand_dims(img_array, axis=0)
        img_array = preprocess_input(img_array)
        features = model.predict(img_array)
        img_hash = dhash(img)
        return features.flatten(), img_hash
    except Exception as e:
        print(f"Error processing image {image_path}: {e}")
        return None, None

def find_duplicates(folder_path, esimilarity_threshold=0.5, csimilarity_threshold=0.9):
    global dupprogress
    global dupprogresstext
    global errors
    global stop_thread

    stop_thread = False  # Reset the stop flag at the beginning

    if not os.path.exists(folder_path):
        print(f"The provided folder path {folder_path} does not exist.")
        return

    image_extensions = ['.jpg', '.jpeg', '.png']
    images = [img_path for img_path in glob(os.path.join(folder_path, '*')) if os.path.splitext(img_path)[1].lower() in image_extensions]
    
    print(f'Found {len(images)} files in {folder_path}.')

    lock = threading.Lock()
    features_list = {}
    duplicates_dict = {}

    for idx, img_path in enumerate(images):
        if stop_thread:  # Check the stop flag
            print("Stopping thread as requested.")
            break

        try:
            features, img_hash = extract_features(img_path)
            if features is None:
                dupprogress = (idx + 1) * 100 // len(images)
                dupprogresstext = f'{(idx + 1)}/{len(images)}'
                continue

            with lock:
                is_duplicate = False
                for original_img_path, (f, h) in features_list.items():
                    esimilarity = euclidean_distances([features], [f])[0][0]
                    csimilarity = cosine_similarity([features], [f])[0][0]
                    if esimilarity < esimilarity_threshold or csimilarity > csimilarity_threshold or img_hash == h:
                        is_duplicate = True
                        duplicates_dict.setdefault(os.path.basename(original_img_path), []).append(os.path.basename(img_path))
                        break

                if not is_duplicate:
                    features_list[img_path] = (features, img_hash)

            dupprogress = (idx + 1) * 100 // len(images)
            dupprogresstext = f'{(idx + 1)}/{len(images)}'

        except Exception as e:
            print(f"Error processing image {img_path}")
            errors.append(img_path)
            dupprogress = (idx + 1) * 100 // len(images)
            dupprogresstext = f'{(idx + 1)}/{len(images)}'

    print(f'Finished processing {folder_path}.')
    os.makedirs(os.path.dirname(os.path.join(folder_path, 'duplicates.json')), exist_ok=True)
    with open(os.path.join(folder_path, 'duplicates.json'), 'w') as json_file:
        json.dump(duplicates_dict, json_file, indent=4)

def load_image_data(folder_path):
    data_path = os.path.join(folder_path, 'duplicates.json')
    if not os.path.exists(data_path):
        return {}
    with open(data_path, 'r') as f:
        image_data = json.load(f)

    encoded_image_data = {}
    for original_image, duplicate_images in image_data.items():
        encoded_original_image = urllib.parse.quote(original_image)
        encoded_duplicate_images = [urllib.parse.quote(image_path) for image_path in duplicate_images]
        encoded_image_data[encoded_original_image] = encoded_duplicate_images
    return encoded_image_data

def generate_random_string(length=10):
    return ''.join(random.choices(string.ascii_letters + string.digits, k=length))

def prepare_files(images_folder, backup_folder):
    global images_folder_progress

    image_extensions = ['.jpg', '.jpeg', '.png']

    files = [f for f in os.listdir(images_folder) if os.path.isfile(os.path.join(images_folder, f)) and os.path.splitext(f)[1].lower() in image_extensions]
    total_files = len(files)

    if total_files == 0: 
        total_backup_files = len([f for f in os.listdir(backup_folder) if os.path.isfile(os.path.join(backup_folder, f))])
        if total_backup_files == 0:
            images_folder_progress = -1
        else:
            copy_files(backup_folder, images_folder)
            images_folder_progress = 100
    else:    
        for idx, file in enumerate(files):
            source_path = os.path.join(images_folder, file)
            # file_name, file_extension = os.path.splitext(file)
            # # unique_name = f"{time.time_ns()}-{generate_random_string()}{file_extension}"
            # shutil.copy(source_path, os.path.join(images_folder, file_name))
            # shutil.copy(source_path, os.path.join(backup_folder, file_name))
            shutil.copy(source_path, backup_folder)
            # os.remove(source_path)
            images_folder_progress = (idx + 1) * 100 // total_files

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
    image_data = load_image_data(images_folder)
    return render_template('result.html', image_data=image_data, images_folder=images_folder)

@app.route('/images/<path:filename>')
def serve_image(filename):
    images_folder = request.args.get('images_folder')
    return send_from_directory(images_folder, filename)

@app.route('/reset')
def page_reset():
    return render_template('reset.html')

# api routes
@app.route('/images_folder', methods=['POST'])
def api_submit_image_folder():
    global images_folder_progress

    images_folder = request.form.get('images_folder')

    if not images_folder:
        return jsonify({'status': 'error', 'error': 'No folder path provided'})

    if not os.path.exists(images_folder) or not os.path.isdir(images_folder):
        return jsonify({'status': 'error', 'error': 'Invalid folder path'})

    images_backup_folder = os.path.join(images_folder, 'backup')

    os.makedirs(images_backup_folder, exist_ok=True)
    prepare_files(images_folder, images_backup_folder)
    return jsonify({'status': 'success', 'success': 'Reading folder'})
    
@app.route('/images_folder')
def api_images_folder_progress():
    global images_folder_progress
    return jsonify({'progress': images_folder_progress})

@app.route('/find_duplicates', methods=['POST'])
def finddup():
    global dupprogress
    global dupprogresstext
    global errors
    errors = []
    dupprogresstext = "0/0"
    dupprogress = 0
    images_folder = request.form['images_folder']
    esimilarity_threshold = float(request.form.get('esimilarity_threshold', 0.5))
    csimilarity_threshold = float(request.form.get('csimilarity_threshold', 0.9))
    data_path = os.path.join(images_folder, 'duplicates.json')
    if os.path.exists(data_path):
        os.remove(data_path)
    thread = Thread(target=find_duplicates, args=(images_folder, esimilarity_threshold, csimilarity_threshold))
    thread.start()
    return jsonify({'status': 'success'})

@app.route('/find_duplicates')
def get_dup_progress():
    global dupprogress
    global dupprogresstext
    return jsonify({'progress': dupprogress, 'text': dupprogresstext})

@app.route('/find_duplicates_errors')
def get_dup_progress_errors():
    global errors
    return jsonify({'errors': errors})

@app.route('/delete_duplicates', methods=['POST'])
def delete_duplicates():
    images_folder = request.form['images_folder']
    duplicate_images = request.form.getlist('duplicate_images[]')
    for image in duplicate_images:
        image_path = os.path.join(images_folder, image)
        if os.path.exists(image_path):
            os.remove(image_path)
    data_path = os.path.join(images_folder, 'duplicates.json')
    if os.path.exists(data_path):
        os.remove(data_path)
    return jsonify({'status': "success"})

@app.route('/stop_duplicates', methods=['POST'])
def stop_duplicates():
    global stop_thread
    stop_thread = True
    return jsonify({'status': 'success', 'message': 'Stopping duplicate finding process'})

@app.route('/open_folder', methods=['POST'])
def open_folder():
    return jsonify({'status': "success"})

def start_flask():
    app.run(debug=False, port=5501)

if __name__ == '__main__':
    webbrowser.open('http://127.0.0.1:5501')
    start_flask()
