# import the necessary packages
from keras.models import load_model
from keras.preprocessing import image
import numpy as np
import matplotlib.pyplot as plt

model = load_model('./model/auswahl-012-0.2514.hdf5')
model.summary()

img = image.load_img('./misc/hotdog_test.jpg', target_size=(224, 224))
img_tensor = image.img_to_array(img)
img_tensor = np.expand_dims(img_tensor, axis=0)
img_tensor /= 255

plt.imshow(img_tensor[0])
plt.show()

prediction = model.predict(img_tensor)
print(prediction)