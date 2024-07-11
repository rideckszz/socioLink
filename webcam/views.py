from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import os
import cv2
import numpy as np
import base64
import json
from PIL import Image, ImageDraw, ImageFont
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout, Flatten, Conv2D, MaxPooling2D, Input
import requests
from django.shortcuts import render
from django.http import HttpResponse
import os
from django.conf import settings
import uuid


def index(request):
    return render(request, 'webcam/index.html')

def features(request):
    return render(request, 'webcam/features.html')

def escreveAI(request):
    return render(request, 'webcam/escreveAI.html')

def emocionAI(request):
    return render(request, 'webcam/emocionAI.html')

def sobre(request):
    return render(request, 'webcam/sobre.html')

def referencias(request):
    return render(request, 'webcam/referencias.html')

def custom_404(request, exception):
    return render(request, 'webcam/404.html', status=404)

def custom_500(request):
    return render(request, 'webcam/500.html', status=500)



def generate_image(prompt: str, output_file: str, api_key: str):
    print(f"Generating image with prompt: {prompt}")
    response = requests.post(
        "https://api.stability.ai/v2beta/stable-image/generate/ultra",
        headers={
            "authorization": f"Bearer {api_key}",
            "accept": "image/*"
        },
        files={"none": ''},
        data={
            "prompt": prompt,
            "output_format": "png", 
        },
    )

    if response.status_code == 200:
        with open(output_file, 'wb') as file:
            file.write(response.content)
        print(f"Image saved to {output_file}")
    else:
        raise Exception(str(response.json()))
    
@csrf_exempt
def escreve_ai(request):
    image_url = None
    if request.method == "POST":
        print("POST request received")
        character = request.POST.get("character")
        action = request.POST.get("action")
        card_text = request.POST.get("card_text")
        print(f"Character: {character}, Action: {action}, Card Text: {card_text}")
        if character and action and card_text:
            prompt = f"{character} {action} with a cartoon style"
            # Generate a unique filename
            unique_filename = f"generated_image_{uuid.uuid4()}.png"
            output_file = os.path.join(settings.MEDIA_ROOT, unique_filename)
            api_key = settings.API_KEY 
            print(f"Prompt: {prompt}, Output File: {output_file}")
            generate_image(prompt, output_file, api_key)
            print("Image generated")
            
            # Add text to the generated image
            image = Image.open(output_file)
            draw = ImageDraw.Draw(image)
            font_path = os.path.join(settings.STATIC_ROOT, 'fonts', 'Raleway-Black.ttf')  
            font = ImageFont.truetype(font_path, 114)
            bbox = draw.textbbox((0, 0), card_text, font=font)
            text_width, text_height = bbox[2] - bbox[0], bbox[3] - bbox[1]
            

            text_position = ((image.width - text_width) / 2, image.height - text_height - 70)
            draw.text(text_position, card_text, font=font, fill="white")
            image.save(output_file)
            
            image_url = settings.MEDIA_URL + unique_filename
            print(f"Image URL: {image_url}")
    else:
        print("Not a POST request")
    return render(request, "webcam/escreveAI.html", {"image_url": image_url})


model = Sequential([
    Input(shape=(48, 48, 1)),
    Conv2D(32, kernel_size=(3, 3), activation='relu'),
    Conv2D(64, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Conv2D(128, kernel_size=(3, 3), activation='relu'),
    MaxPooling2D(pool_size=(2, 2)),
    Dropout(0.25),
    Flatten(),
    Dense(1024, activation='relu'),
    Dropout(0.5),
    Dense(7, activation='softmax')
])


model_weights_path = os.path.join(settings.BASE_DIR, 'model.weights.h5')
model.load_weights(model_weights_path)


emotion_dict = {0: "Angry", 1: "Disgusted", 2: "Fearful", 3: "Happy", 4: "Neutral", 5: "Sad", 6: "Surprised"}

@csrf_exempt
def detect_emotion(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        image_data = data['image'].split(',')[1]
        img_data = base64.b64decode(image_data)
        np_arr = np.frombuffer(img_data, np.uint8)
        img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        facecasc_path = os.path.join(settings.STATIC_ROOT, 'haarcascade_frontalface_default.xml')
        facecasc = cv2.CascadeClassifier(facecasc_path)
        faces = facecasc.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        if len(faces) > 0:
            (x, y, w, h) = faces[0]
            roi_gray = gray[y:y + h, x:x + w]
            cropped_img = np.expand_dims(np.expand_dims(cv2.resize(roi_gray, (48, 48)), -1), 0)
            prediction = model.predict(cropped_img)
            maxindex = int(np.argmax(prediction))
            emotion = emotion_dict[maxindex]
        else:
            emotion = "No face detected"
            print("No face")

        return JsonResponse({'emotion': emotion})
