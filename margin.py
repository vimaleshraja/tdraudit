
from cv2 import imread, line, cvtColor, COLOR_RGB2BGR
from PIL import Image
import numpy as np

def margin_content_check(image):
  flag=0
  a=0
  b=0
  if image.shape[0]!=1000:
    image = np.rot90(image, k=1)

  for i in np.concatenate((np.arange(87,90),np.arange(910,913))):  #height
    if flag==0:
      for j in range(133,686):
        pixel_value = image[i,j]
        if any(pixel_value!=255):
          flag = 1
          break
        else:
          flag = 0
          image[i,j] = (0,0,255)

  for a in range(87,910):
    if flag==0:
      for b in np.concatenate((np.arange(131,133),np.arange(686,688))):   #width
        pixel_value = image[a,b]
        if any(pixel_value!=255):
          flag = 1
          c=[a,b]
          break
        else:
          flag = 0
          image[a,b] = (0,0,255)

  return flag, image

def draw_border(image):
  a=0
  b=0
  if image.shape[0]!=1000:
    image = np.rot90(image, k=1)

  for i in np.concatenate((np.arange(87,89),np.arange(910,912))):  #height
    for j in range(132,687):
      image[i,j] = (0,0,255)

  for a in range(87,910):
    for b in np.concatenate((np.arange(132,134),np.arange(685,687))):   #width
      image[a,b] = (0,0,255)

  return image