import boto3
import pandas as pd
import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import numpy as np

# Load the saved model
model = tf.keras.models.load_model("HH_only_inception_repeat_600by400with20patience.h5")

# Function to preprocess image
def preprocess_image(img):
    img = img.resize((400, 600))
    img_array = np.array(img)
    img = tf.keras.applications.inception_v3.preprocess_input(img_array)
    return img

# Function to make predictions
def predict_image(img):
    img = preprocess_image(img)
    img = tf.expand_dims(img, axis=0)
    prediction = model.predict(img)
    return prediction

s3 = boto3.client('s3')
path = 's3://cornimagesbucket/csvOut.csv'
df = pd.read_csv(path)

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

# Threshold for classification
        threshold = 0.5  # You can adjust this threshold as needed

# Make binary prediction based on threshold
        if predicted_probability >= threshold:
            predicted_label = "Unhealthy"
            print(f"Prediction for {image_name}: {predicted_label}")
            print(f"Predicted probability of being unhealthy: {predicted_probability}")

        else:
            predicted_label = "Healthy"
            print(f"Prediction for {image_name}: {predicted_label}")
            print(f"Predicted probability of being healthy: {(1 - predicted_probability)}")

    else:
        print(f"Failed to fetch image: {image_name}")
