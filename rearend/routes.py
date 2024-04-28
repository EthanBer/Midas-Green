from flask import Blueprint, request, jsonify
from script_model import run

routes = Blueprint("routes", __name__)

@routes.route('/upload', methods=['POST'])
def run_model():

    print("file sent")

    if 'file' not in request.files:
        print('no file')
        return 'no file', 400

    file = request.files['file']
    if file.filename == '':
        return 'No selected file', 400

    result = run(file)

    return jsonify({'body': result})
