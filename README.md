# Agro-AI-Capstone
2024 UNO Capstone Project Repository

This project aims to demonstrate the benfits of AI use in agriculture and educate those who may not be familiar with AI's interworkings. The app makes use of both a Random Forest and pre-trained Keras CNN model to highlight the difference between the two.

#Getting started
After ensuring the necessary keras model file is in the cnn_model folder, navigate to that folder and enable the model to make predictions using the following command:
'''bash
python3 get_cnn_model_predictions.py
'''
This will dump the model's predictions into labels.json and probabilities.json

Next navigate back one folder in order to run the flask application, which can be achieved with the following command:
'''bash
gunicorn -b 0.0.0.0:8000 wsgi:app
'''
If necessary, a timeout flag can be included:
'''bash
gunicorn -b 0.0.0.0:8000 --timeout 5000 wsgi:app
'''
Once running, the application can be accessed via a web browser at http://137.48.186.128:8000/

Release Notes:

Code Milestone 1:
A python script called ResizeImages.py was created within the utility folder to resize each image down to 1024 by 768. A batch job is being created on the HCC server to resize all of the images.

Code Milestone 2:
A python script called AI.py was created under the model_training folder to train the AI model using EfficientNet. The training is being done on the HCC server. The model uses binary classification to divide the images into either healthy or unhealthy.

Code Milestone 3:
requirements.txt was updated with newer/compatible versions of necessary packages. The home page of the application has been updated and finalized to reflect login functionality. A MySQL database has been set up and includes a Users table to store user login information. Additionally, the process of setting up an Ubuntu server on VMWare has also been started, but technical issues are still being worked out.

Code Milestone 4:
The server on VMWare has been set up. The UI for the login, register account, and registration success pages has been developed. Username and password restrictions have been enabled when registering an account. The MySQL database has been connected to the application, so only users with valid credentials can log in. Different AI models are being explored to try to maximize accuracy.

Code Milestone 5:
The pretrained CNN model was implemented into the flask app which labels images and displays confidence intervals on final.html. Predictions are made in a python script which dumps the results in a JSON file. The JSON file is then read by the flask app, this ensures continued speed perforamce for the application(as model predictions are time intensive and do not need to be done more than once). Repo was organized, adding cnn_model for all things CNN model prediction related, and HCC was added to reflect the necessary code for model training. Automated and manula testing was also conducted.
