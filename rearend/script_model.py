import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import replicate
import os
from rag import rag
from finetuned_llm import ask

# put your token into tokens.py
from tokens import REPLICATE_TOKEN

def run(image):

    torch.jit.load('mojdel.pt', map_location='cpu')
    
    img = Image.open(image)
    preprocess = transforms.Compose([
        transforms.Resize((256, 256)),
        transforms.ToTensor(),
    ])
    train = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 
             'Peach___Leaf_curl', 'Peaches___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
    print([i for i in range(len(train)) if train[i] == 'Peach___Leaf_curl'])
    input_image = preprocess(img).unsqueeze(0)  # Add batch dimension
    
    with torch.no_grad():
        model = torch.jit.load('mojdel.pt', map_location=torch.device('cpu'))
        output = model(input_image)
    predicted_class = torch.argmax(output, dim=1).item()
    
    print(train[predicted_class])

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN
    
    # input = {
    #     "top_p": 1,
    #     "prompt": "given this context:" + rag[predicted_class] + "Using your knowledge in combination with that context" + "You will provide a diagnosis and a treatment recommendation with a product for" + train[predicted_class] + "disease in plant",
    #     "temperature": 0.5,
    #     "system_prompt": "This is in response to an app that a user uploaded an image to a classifier for disease. You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
    #     "max_new_tokens": 500
    # }

    # result = ""
    
    # for event in replicate.stream("meta/llama-2-70b-chat", input=input):
    #     result += event.data

    result = ask("\n\n " + rag[predicted_class] + " 4 facts about this plant disease are: ")
    
    return result
