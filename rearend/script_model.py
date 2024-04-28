import torch
import torchvision
import torchvision.transforms as transforms
from PIL import Image
import replicate
import os

# put your token into tokens.py
from tokens import REPLICATE_TOKEN

def run(image):

    torch.load('mojdel.pt', map_location='cpu')
    
    img = Image.open(image)
    preprocess = transforms.Compose([
        transforms.ToTensor(),           # Convert to tensor
    ])
    train = ['Apple___Apple_scab', 'Apple___Black_rot', 'Apple___Cedar_apple_rust', 'Apple___healthy', 'Blueberry___healthy', 'Cherry_(including_sour)___Powdery_mildew', 'Cherry_(including_sour)___healthy', 'Corn_(maize)___Cercospora_leaf_spot Gray_leaf_spot', 'Corn_(maize)___Common_rust_', 'Corn_(maize)___Northern_Leaf_Blight', 'Corn_(maize)___healthy', 'Grape___Black_rot', 'Grape___Esca_(Black_Measles)', 'Grape___Leaf_blight_(Isariopsis_Leaf_Spot)', 'Grape___healthy', 'Orange___Haunglongbing_(Citrus_greening)', 'Peach___Bacterial_spot', 'Peach___healthy', 'Pepper,_bell___Bacterial_spot', 'Pepper,_bell___healthy', 'Potato___Early_blight', 'Potato___Late_blight', 'Potato___healthy', 'Raspberry___healthy', 'Soybean___healthy', 'Squash___Powdery_mildew', 'Strawberry___Leaf_scorch', 'Strawberry___healthy', 'Tomato___Bacterial_spot', 'Tomato___Early_blight', 'Tomato___Late_blight', 'Tomato___Leaf_Mold', 'Tomato___Septoria_leaf_spot', 'Tomato___Spider_mites Two-spotted_spider_mite', 'Tomato___Target_Spot', 'Tomato___Tomato_Yellow_Leaf_Curl_Virus', 'Tomato___Tomato_mosaic_virus', 'Tomato___healthy']
    input_image = preprocess(img).unsqueeze(0)  # Add batch dimension
    
    with torch.no_grad():
        model = torch.jit.load('mojdel.pt', map_location=torch.device('cpu'))
        output = model(input_image)
    predicted_class = torch.argmax(output, dim=1).item()
    print(train[predicted_class])
    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_TOKEN
    RAG = ['', '', 'Cedar-apple rust is a common disease of apple and flowering crabapple in Kansas. These rust fungi spend a portion of their life cycle on apple and flowering crabapple and the remaining portion on species of Juniperus (which includes eastern red cedar). This rust fungus can result in considerable damage to rosaceous plants by causing premature defoliation and fruit distortion and abortion. The effects of this diseases on junipers are minimal. Symptoms on Apple and Crabapple: Symptoms of cedar-apple rust on flowering crab and apple are easily identified. In late spring or early summer, bright, yellow-orange spots approximately 1/8 to 1/4 inch in diameter form on the upper surface of leaves. These spots gradually enlarge and turn orange. Small black fruiting structures (pycnia) of the fungus form in the center of the lesion on the bottom of the leaf. Leaves with numerous spots drop during the summer. Premature defoliation weakens the tree and reduces fruit set and yield the following year. Trees with severe defoliation also are susceptible to other diseases. Cedar-apple and cedar-quince rust may cause fruit lesions. Diseased fruits develop deep pits or become distorted and usually drop before harvest. The severity of rust infection on apple in the spring is highly dependent on weather conditions. It is also dependent on the amount of infection that occurred two years previously on juniper, since those infections eventually produce the active galls of the current year that in turn produce the spores which infect apple. A combination of a large number of active galls along with wet spring weather can result in serious infection of apple. Recommendations: Fungicide sprays during April and May are critical to preventing disease on susceptible varieties. The first spray should go down when leaves appear. A fungicide that is available to homeowners and very effective for control of apple scab and cedar apple rust is myclobutanil (Immunox, Fungi-Max and F-Stop Lawn & Garden Fungicide). There is more than one formulation of Immunox but only one is labeled for fruit. Check the label. Sprays should be done on a 7- to 10-day schedule to keep the protective chemical cover on the rapidly developing leaves and fruit. These diseases are usually only a problem during April and May. Although gardeners may continue to use myclobutanil after May, certain other fungicides are more effective on summer diseases such as sooty blotch and fly speck. Consider using Bonide Fruit Tree and Plant Guard after petal drop as it contains an insecticide(s) and fungicide(s). However, you are limited in the number of applications per year allowed. A spreader-sticker can be added to the fungicide mixture to improve the distribution and retention of the pest control chemicals over the leaves and fruit. Sprays are applied every 10 to 14 days. A hard, driving rain of about 1 inch or more will likely wash chemicals from the leaves and fruit. In such cases, another application should be made.']
    input = {
        "top_p": 1,
        "prompt": "given this context:" + RAG[predicted_class] + "Using your knowledge in combination with that context" + "You will provide a diagnosis and a treatment recommendation with a product for" + train[predicted_class] + "disease in plant",
        "temperature": 0.5,
        "system_prompt": "This is in response to an app that a user uploaded an image to a classifier for disease. You are a helpful, respectful and honest assistant. Always answer as helpfully as possible, while being safe. Your answers should not include any harmful, unethical, racist, sexist, toxic, dangerous, or illegal content. Please ensure that your responses are socially unbiased and positive in nature.\n\nIf a question does not make any sense, or is not factually coherent, explain why instead of answering something not correct. If you don't know the answer to a question, please don't share false information.",
        "max_new_tokens": 500
    }

    result = ""
    
    for event in replicate.stream("meta/llama-2-70b-chat", input=input):
        result += event
    
    return result
