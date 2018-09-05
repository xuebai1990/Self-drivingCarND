import csv
import cv2
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

lines = []
with open("../data/driving_log.csv") as csvfile:
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
   image_path_center = "../data/IMG/" + filename_center
   image_path_left = "../data/IMG/" + filename_left
   image_path_right = "../data/IMG/" + filename_right
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

fig = sns.distplot(Y_train)
fig.savefig("hist.png")
