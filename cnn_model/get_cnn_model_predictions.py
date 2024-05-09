import boto3
import pandas as pd
import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import numpy as np
import json

CNN_MODEL_FILE_PATH = "05022023.h5"

# Load the saved model
model = tf.keras.models.load_model(CNN_MODEL_FILE_PATH)

# Function to preprocess image
def preprocess_image(img):
    """
    Resize images to size to be compatible with model

    Args:
        img (PIL.JpegImagePlugin.JpegImageFile): The image to be resized

    Returns:
        PIL.JpegImagePlugin.JpegImageFile: The image after preprocessing.
    """
    img = img.resize((600, 400))
    img_array = np.array(img)
    img = tf.keras.applications.inception_v3.preprocess_input(img_array)
    return img

# Function to make predictions
def predict_image(img):
    """
    Use loaded CNN Model to make a prediction for a single image

    Args:
        img (PIL.JpegImagePlugin.JpegImageFile): The image used for prediction

    Returns:
        numpy.ndarray: The model's prediction for the image
    """
    img = preprocess_image(img)
    img = tf.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return prediction

s3 = boto3.client('s3')
path = 's3://cornimagesbucket/csvOut.csv'
df = pd.read_csv(path)

img_to_label_dict ={}
img_to_prediction_prob_dict={}

# Iterate through each row in the DataFrame
for index, row in df.iterrows():
    # Get the image name from the first column
    image_name = row[0]

    # Construct the image URL
    image_url = f"https://cornimagesbucket.s3.us-east-2.amazonaws.com/images_compressed/{image_name}"

    # Request the image
    response = requests.get(image_url)

    # Check if the request was successful
    if response.status_code == 200:
        # Read the image from the response
        img = Image.open(BytesIO(response.content))

        # Make prediction
        prediction = predict_image(img)
        # Assuming prediction is a single probability indicating likelihood of being unhealthy
        predicted_probability = prediction[0][0]  # Assuming the probability is in the first index
        predicted_probability = float(predicted_probability)

# Threshold for classification
        threshold = 0.4  # You can adjust this threshold as needed
        
# Make binary prediction based on threshold
        if predicted_probability >= threshold:
            predicted_label = "Unhealthy"
        else:
            predicted_label = "Healthy"
            predicted_probability = 1-predicted_probability

        print(f"Prediction for {image_name}: {predicted_label}")
        print(f"Predicted probability of being {predicted_label}: {(predicted_probability)}")

        img_to_label_dict[image_name] = predicted_label
        img_to_prediction_prob_dict[image_name] = predicted_probability
    else:
        print(f"Failed to fetch image: {image_name}")

with  open('labels.json', 'w') as lfp:
    json.dump(img_to_label_dict, lfp)

with  open('probabilities.json', 'w') as pfp:
    json.dump(img_to_prediction_prob_dict, pfp)
