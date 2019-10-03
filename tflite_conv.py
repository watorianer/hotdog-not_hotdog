import numpy as np
import tensorflow as tf

keras_file = './model/auswahl-012-0.2514.hdf5'
converter = tf.lite.TFLiteConverter.from_keras_model_file(keras_file)
tflite_model = converter.convert()
open('model3.tflite', 'wb').write(tflite_model)