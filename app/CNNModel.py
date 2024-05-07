import pandas as pd
import tensorflow as tf
from PIL import Image
import requests
from io import BytesIO
import numpy as np

class CNNModel:
    def __init__(self, csv_file_path, model_file_path):
        self.csv_file_path = csv_file_path
        self.model_file_path = model_file_path
        self.img_to_label_dict = {}
        self.img_to_prediction_prob_dict = {}
        self.model = tf.keras.models.load_model(model_file_path)

    # Function to preprocess image
    def preprocess_image(self, img):
        img = img.resize((400, 600))
        img_array = np.array(img)
        img = tf.keras.applications.inception_v3.preprocess_input(img_array)
        return img

    # Function to make predictions
    def predict_image(self, img):
        img = self.preprocess_image(img)
        img = tf.expand_dims(img, axis=0)
        prediction = self.model.predict(img)
        return prediction

    def make_predictions(self):

        df = pd.read_csv(self.csv_file_path)
        count = 0

        # Iterate through each row in the DataFrame
        for index, row in df.iterrows():
            print(count)
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
                else:
                    predicted_label = "Healthy"
                    predicted_probability = 1-predicted_probability
                

                print(f"Prediction for {image_name}: {predicted_label}")
                print(f"Predicted probability of being {predicted_label}: {(predicted_probability)}")
                
                img_to_label_dict[image_name] = predicted_label
                img_to_prediction_prob_dict[image_name] = predicted_probability
            else:
                print(f"Failed to fetch image: {image_name}")
            count +=1
        return self.img_to_label_dict, self.img_to_prediction_prob_dict
