'''
Generating and manipulating image data
'''
from matplotlib import pyplot, image
import numpy as np
import csv

# generate a random image
random = np.random.randint(0, 255, size=400*300*3, dtype=np.uint8).reshape((400, 300, 3))
pyplot.imshow(random, vmin=0, vmax=255)
pyplot.imsave('random.png', random)
pyplot.show()

# convert an image to grayscale
image = image.imread('c_small.png')
gray = np.mean(image, axis=2)
pyplot.imshow(gray, vmin=0, vmax=1, cmap='gray')
pyplot.imsave('gray.png', gray, cmap='gray')
pyplot.show()

# write image data to CSV
with open('random.csv', 'w') as file:
  csv.writer(file).writerows(random)

with open('gray.csv', 'w') as file:
  csv.writer(file).writerows(gray)