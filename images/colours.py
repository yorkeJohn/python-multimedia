'''
Manipulating colours in image data
'''
from matplotlib import pyplot, image
import numpy as np
import csv

def main(img: np.ndarray, suffix: str='') -> None:
  print(f'Image Shape: {img.shape}')
  pyplot.imshow(img)
  pyplot.show()

  x, y, z = img.shape
  all_colors = img.reshape(x*y, z)
  print(f'All Colors Shape: {all_colors.shape}')
  print(f'All Colors:\n{all_colors}')

  with open(f'all_colors{suffix}.csv', 'w') as file:
    csv.writer(file).writerows(all_colors)

  unique_colors, counts = np.unique(all_colors, axis=0, return_counts=True)
  print(f'Unique Colors Shape: {unique_colors.shape}')
  print(f'Unique Colors:\n{unique_colors}')
  print(f'Frequencies:\n{counts}')

  with open(f'unique_colors{suffix}.csv', 'w') as file:
    csv.writer(file).writerows(unique_colors)

  with open(f'unique_freq{suffix}.csv', 'w') as file:
    csv.writer(file).writerow(counts)

  pyplot.plot(counts)
  pyplot.ylabel('Frequency')
  pyplot.show()

  x, z = unique_colors.shape
  size = int(np.sqrt(x)) + 1
  unique_colors = np.vstack((unique_colors, np.ones((size**2 - x, z)))).reshape(size, size, z)
  pyplot.imshow(unique_colors)
  pyplot.show()

# using the original image
img = image.imread('c_small.png')
main(img)

# reducing to 3 colour bits
bits = 3
reducer = 2**bits - 1
img = np.round(img * reducer) / reducer
main(img, '_reduced')
