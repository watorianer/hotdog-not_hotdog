import tensorflow as tf
import tkinter as tk
from tkinter import filedialog
import PIL
from PIL import Image
import numpy as np
import time

# DEF. PARAMETERS
img_row, img_column = 224, 224
num_channel = 3
num_batch = 1
input_mean = 0
input_std = 255.0
floating_model = True

path = "./model/tflite/model3.tflite"


interpreter = tf.lite.Interpreter(path)
interpreter.allocate_tensors()

# obtaining the input-output shapes and types
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()
print(input_details, '\n', output_details)

# file selection window for input selection
root = tk.Tk()
root.withdraw()
file_path = filedialog.askopenfilename()
input_img = Image.open(file_path)
input_img = input_img.resize((img_row, img_column))
input_img = np.expand_dims(input_img, axis=0)

input_img = (np.float32(input_img) - input_mean) / input_std

interpreter.set_tensor(input_details[0]['index'], input_img)

# running inference
interpreter.invoke()

output_data = interpreter.get_tensor(output_details[0]['index'])
results = np.squeeze(output_data)
print(results)
