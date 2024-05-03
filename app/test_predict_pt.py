import boto3
import pandas as pd
import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO

# Load the saved model
model = tf.keras.models.load_model("HH_only_inception_repeat_600by400with20patience.h5")

# Function to preprocess image
def preprocess_image(img):
    img = img.resize((600, 400))
    img = tf.keras.applications.inception_v3.preprocess_input(img)
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
        
        # Print the prediction
        print(f"Prediction for {image_name}: {prediction}")
    else:
        print(f"Failed to fetch image: {image_name}")

