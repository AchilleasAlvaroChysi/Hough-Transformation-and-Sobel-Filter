import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, misc
import sys
from PIL import Image

def rgb2gray(rgb):
	if (not len(rgb.shape) < 3):
	    return np.dot(rgb[...,:3], [0.3333, 0.3333, 0.3333])

	return rgb
	
def parseImage(fileName):
	return np.array(Image.open(fileName))

def thresholdImage(image,thresh):
	result = np.copy(image)
	for i in range (result.shape[0]):
		for j in range (result.shape[1]):
			if result[i,j]<float(float(thresh)*255.0):
				result[i,j] = 0.0
			else:
				result[i,j] = 255.0
	return result

def sobel(image, threshold):
	Gx = np.array([ [-1 , 0, 1], [-2, 0, 2], [-1, 0, 1]])
	Gy = np.array([ [-1, -2, -1], [0, 0, 0], [1, 2, 1]])
	Sx = signal.convolve2d(image, Gx, boundary = 'symm', mode = 'same')
	Sy = signal.convolve2d(image, Gy, boundary = 'symm', mode = 'same')
	Smag = np.abs(Sx)+np.abs(Sy)
	return thresholdImage(Smag,threshold)

def saveImage(image, path):
	misc.imsave(path, image)

if __name__ == "__main__":
	if len(sys.argv) < 3:
		print("Add more arguments")
		sys.exit(-1)

	saveImage(sobel(rgb2gray(parseImage(sys.argv[1])), sys.argv[2]),"sobel-" + sys.argv[1])
