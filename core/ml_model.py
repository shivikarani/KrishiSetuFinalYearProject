import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

MODEL_PATH = "core/ml_models/crop_disease_model.h5"
model = load_model(MODEL_PATH)

classes = ['Apple Scab', 'Corn Blight', 'Healthy', 'Tomato Leaf Spot']

def predict_disease(img_path):
    img = image.load_img(img_path, target_size=(128,128))  # match training size
    img_array = image.img_to_array(img)
    img_array = img_array / 255.0
    img_array = np.expand_dims(img_array, axis=0)

    pred = model.predict(img_array)
    class_index = np.argmax(pred)

    return classes[class_index], float(np.max(pred))