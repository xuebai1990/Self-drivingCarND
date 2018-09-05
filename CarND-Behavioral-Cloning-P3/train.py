import csv
import cv2
import numpy as np

lines = []
with open("data/driving_log.csv") as csvfile:
   reader = csv.reader(csvfile)
   next(reader)
   for line in reader:
      lines.append(line)

images = []
measurements = []
correction = 0.15
for line in lines:
   path_center = line[0]
   path_left = line[1]
   path_right = line[2]
   filename_center = path_center.split('/')[-1]
   filename_left = path_left.split('/')[-1]
   filename_right = path_right.split('/')[-1]
   image_path_center = "data/IMG/" + filename_center
   image_path_left = "data/IMG/" + filename_left
   image_path_right = "data/IMG/" + filename_right
   image_center = cv2.imread(image_path_center)
   image_left = cv2.imread(image_path_left)
   image_right = cv2.imread(image_path_right)
   images.extend([image_center, image_left, image_right])

   steering_center = float(line[3])
   steering_left = steering_center + correction
   steering_right = steering_center - correction
   measurements.extend([steering_center, steering_left, steering_right])

   #augment by flipping
   flip_image_center = cv2.flip(image_center, 1)
   flip_image_left = cv2.flip(image_left, 1)
   flip_image_right = cv2.flip(image_right, 1)
   images.extend([flip_image_center, flip_image_left, flip_image_right])
   measurements.extend([-steering_center, -steering_left, -steering_right])

X_train = np.array(images)
Y_train = np.array(measurements)
print("Finished loading data!")

from keras.models import Sequential
from keras.layers import Flatten, Dense, Lambda, Cropping2D
from keras.layers.convolutional import Convolution2D
from keras.layers.pooling import MaxPooling2D

model = Sequential()
model.add(Lambda(lambda x: x / 255.0 - 0.5, input_shape=(160,320,3)))
model.add(Cropping2D(cropping=((65,25), (0,0))))
model.add(Convolution2D(24,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(36,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(48,5,5,subsample=(2,2),activation='relu'))
model.add(Convolution2D(64,3,3,subsample=(1,1),activation='relu'))
model.add(Convolution2D(64,3,3,subsample=(1,1),activation='relu'))
model.add(Flatten())
model.add(Dense(1164,activation='relu'))
model.add(Dense(100,activation='relu'))
model.add(Dense(50,activation='relu'))
model.add(Dense(10,activation='relu'))
model.add(Dense(1))

model.compile(loss='mse', optimizer='adam')
model.fit(X_train, Y_train, batch_size=32, epochs=4, validation_split=0.2, shuffle=True)
model.save('model.h5')
