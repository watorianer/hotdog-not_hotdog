# use the pretrained mobilenet_v2 and fine tune it
# to recognize pictures of hotdog and not hotdog

# import the necessary packages
from keras.applications import MobileNetV2
from keras import models
from keras import layers
from keras import optimizers
from keras.preprocessing.image import ImageDataGenerator
from keras.callbacks import ModelCheckpoint
from keras.callbacks import EarlyStopping
from helper.callbacks import TrainingMonitor
from imutils import paths
import os
import argparse
import numpy as np


# construct the argument parser and parse the
# arguments
ap = argparse.ArgumentParser()
ap.add_argument('-d', '--directory', default='./data/',
    help='path to the directory containing the training images')
ap.add_argument('-m', '--model', default='./model/',
    help='path where to save the model')
ap.add_argument('-mo', '--monitoring', default='./monitoring/',
    help='path where to save the monitoring graph')
args = vars(ap.parse_args())

# load the network
mobile_net = MobileNetV2(alpha=0.5, include_top=False, input_shape=(224, 224, 3))

# Freeze the layers of mobile_net
mobile_net.trainable = False

# create the model
model = models.Sequential()

# add the base model
model.add(mobile_net)

# add the new layers
model.add(layers.Flatten())
model.add(layers.Dense(256))
model.add(layers.Activation('relu'))
model.add(layers.Dense(256))
model.add(layers.Activation('relu'))
model.add(layers.Dropout(0.5))
model.add(layers.Dense(1))
model.add(layers.Activation('sigmoid'))

# get training and validaton directory
train_dir = os.path.join(args['directory'], 'train')
val_dir = os.path.join(args['directory'], 'validation')

# construct the image generator for data augmentation
# of the training data
train_datagen = ImageDataGenerator(
    rescale=1./255,
    rotation_range=30, 
    width_shift_range=0.1,
    height_shift_range=0.1, 
    shear_range=0.2,
    zoom_range=0.2,
    horizontal_flip=True, 
    fill_mode='nearest')

# construct the image generator for the validation data
val_datagen = ImageDataGenerator(rescale=1./255)

# construct the dataflow from the training directory
tain_generator = train_datagen.flow_from_directory(
    train_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# construct the dataflow from the validation directory
val_generator = val_datagen.flow_from_directory(
    val_dir,
    target_size=(224, 224),
    batch_size=32,
    class_mode='binary'
)

# build callback to serialize the model if validation
# loss decreased
fname = os.path.join(args['model'], 
    '{epoch:03d}-{val_loss:.4f}.hdf5')
checkpoint = ModelCheckpoint(fname, monitor='val_loss', verbose=1,
    save_best_only=True)

# build early stopping callback
early_stopping = EarlyStopping(monitor='val_loss', patience=10, verbose=1,
    restore_best_weights=True)

# Build the monitoring callback
figPath = os.path.sep.join([args['monitoring'], '{}.png'.format(
    os.getpid())])
jsonPath = os.path.sep.join([args['monitoring'], '{}.json'.format(
    os.getpid())])
monitoring = TrainingMonitor(figPath, jsonPath)

callbacks = [checkpoint, early_stopping, monitoring]

# Try some different learning optimizer
opt = optimizers.SGD(lr=0.0001, decay=0.0001 / 100, momentum=0.9, nesterov=True)
opt2 = optimizers.Adam(decay=0.0001/100)

# compile the model
model.compile(loss='binary_crossentropy',
    optimizer=opt,
    metrics=['accuracy'])

history = model.fit_generator(
    tain_generator,
    steps_per_epoch = 57,
    epochs = 100,
    callbacks=callbacks,
    validation_data=val_generator,
    validation_steps=7
)