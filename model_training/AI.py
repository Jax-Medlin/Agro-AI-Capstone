#EfficientNet
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import EfficientNetB0

# Define constants
IMAGE_SIZE = (1024, 768)
BATCH_SIZE = 32
EPOCHS = 10
NUM_CLASSES = 3

# Define file paths
train_dir = '/work/hsiycsci4970/jaxmedlin/model_training_handheld_only/training'
validation_dir = '/work/hsiycsci4970/jaxmedlin/model_training_handheld_only/validation'

# Data preprocessing
train_datagen = ImageDataGenerator(rescale=1./255)
validation_datagen = ImageDataGenerator(rescale=1./255)

train_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

validation_generator = validation_datagen.flow_from_directory(
    validation_dir,
    target_size=IMAGE_SIZE,
    batch_size=BATCH_SIZE,
    class_mode='binary'
)

# Build EfficientNet model
base_model = EfficientNetB0(weights='imagenet', include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
output = Dense(1, activation='sigmoid')(x)  # Output layer with 1 neuron and sigmoid activation
model = tf.keras.Model(inputs=base_model.input, outputs=output)

# Freeze the base model
# base_model.trainable = False

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

#print model
print(model.summary())

# Train model
history = model.fit(
    train_generator,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=EPOCHS,
    validation_data=validation_generator,
    validation_steps=validation_generator.samples // BATCH_SIZE
)

# Save the model
model.save('maize_leaf_classifier_efficientnet_HH_only.h5')                