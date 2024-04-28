from flask import Flask, request, jsonify
from flask_cors import CORS
from rearend import script_model

app = Flask(__name__)
CORS(app)

@app.route('/run_model', methods=['POST'])
def run_model():
    image = request.files['image']  # Access the uploaded file
    result = script_model.run(image)  # Process the image using your script_model
    return jsonify({'result': "result"})

if __name__ == '__main__':
    app.run(debug=True)
