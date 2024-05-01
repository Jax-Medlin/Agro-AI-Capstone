import numpy as np
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D
from tensorflow.keras.preprocessing.image import ImageDataGenerator
from tensorflow.keras.applications import InceptionV3
from tensorflow.keras.callbacks import EarlyStopping

# Define early stopping callback
early_stopping = EarlyStopping(monitor='val_accuracy', patience=20, restore_best_weights=True)

# Define constants
IMAGE_SIZE = (600, 400)
BATCH_SIZE = 32
NUM_CLASSES = 2

# Define file paths
train_dir = '/work/hsiycsci4970/jaxmedlin/handheld_ouput/training'
validation_dir = '/work/hsiycsci4970/jaxmedlin/handheld_ouput/validation'

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

# Repeat the datasets indefinitely
train_dataset = tf.data.Dataset.from_generator(
    lambda: train_generator,
    output_types=(tf.float32, tf.float32),
    output_shapes=([None, IMAGE_SIZE[0], IMAGE_SIZE[1], 3], [None])
).repeat()

validation_dataset = tf.data.Dataset.from_generator(
    lambda: validation_generator,
    output_types=(tf.float32, tf.float32),
    output_shapes=([None, IMAGE_SIZE[0], IMAGE_SIZE[1], 3], [None])
).repeat()

# Build InceptionV3 model
base_model = InceptionV3(weights='imagenet', include_top=False, input_shape=(IMAGE_SIZE[0], IMAGE_SIZE[1], 3))
x = GlobalAveragePooling2D()(base_model.output)
x = Dense(256, activation='relu')(x)
output = Dense(1, activation='sigmoid')(x)  # Output layer with 1 neuron and sigmoid activation
model = tf.keras.Model(inputs=base_model.input, outputs=output)

# Compile model
model.compile(
    optimizer='adam',
    loss='binary_crossentropy',
    metrics=['accuracy']
)

#print model
print(model.summary())

# Train model with early stopping
history = model.fit(
    train_dataset,
    steps_per_epoch=train_generator.samples // BATCH_SIZE,
    epochs=120,  # Use a large number of epochs
    validation_data=validation_dataset,
    validation_steps=validation_generator.samples // BATCH_SIZE,
    callbacks=[early_stopping]  # Pass the early stopping callback
)
# Save the model
model.save('HH_only_inception_repeat_600by400with20patience.h5')
