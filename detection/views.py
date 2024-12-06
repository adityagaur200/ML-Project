from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import cv2
import numpy as np
import os
import tensorflow as tf
from django.core.files.storage import FileSystemStorage
from .utils import crop_brain_contour


MODEL_PATH = 'D:\Brain\detection\cnn_model.keras'

model = tf.keras.models.load_model(MODEL_PATH)

IMG_WIDTH, IMG_HEIGHT = 240, 240


def predict_image(image_path):

    image = cv2.imread(image_path)

    if image is None:
        return "Error: Image could not be loaded. Please check the file path."

    image = crop_brain_contour(image, plot=False)
    image = cv2.resize(image, (IMG_WIDTH, IMG_HEIGHT))
    image = image / 255.0
    image = np.expand_dims(image, axis=0)

    prediction = model.predict(image)

    if prediction > 0.5:
        return "Brain Tumor Detected"
    else:
        return "No Brain Tumor Detected"


@csrf_exempt
def predict(request):
    if request.method == 'POST' and request.FILES['image']:
        uploaded_file = request.FILES['image']
        fs = FileSystemStorage()
        filename = fs.save(uploaded_file.name, uploaded_file)
        file_url = fs.url(filename)

        image_path = os.path.join(os.getcwd(), 'media', filename)

        result = predict_image(image_path)
        return JsonResponse({'prediction': result, 'image_url': file_url})
    else:
        return JsonResponse({'error': 'No image provided'}, status=400)


def index(request):
    return render(request, 'index.html')
