import math
import numpy as np
import matplotlib.pyplot as plt
from scipy import signal, misc
import sys
from PIL import Image
import sobelFilter as sobel

MIN_RADIUS = 10
MAX_RADIUS = 20

def drawCircle(image, x, y, r):
    for t in range(360):
        for p in range(-1, 1):
            a = (int) (x - round(((r + p) * np.cos(t * np.pi / 180))))
            b = (int) (y - round(((r + p) * np.sin(t * np.pi / 180))))
            if a >= 0 and a < image.shape[0] and b >= 0 and b < image.shape[1]:
                image[a, b] = (0, 200, 0)

def hough(image, minRadius, maxRadius):
    image_copy = np.copy(image)
    sobl = sobel.sobel(sobel.rgb2gray(image), 0.9)
    votes = np.zeros((image.shape[0], image.shape[1], maxRadius - minRadius))

    for x in range(votes.shape[0]):
        for y in range(votes.shape[1]):
            if sobl[x, y] == 255:
                for r in range(votes.shape[2]):
                    for t in range(360):
                        a = (int) (x - round((r + minRadius) * np.cos(t * np.pi / 180)))
                        b = (int) (y - round((r + minRadius) * np.sin(t * np.pi / 180)))
                        
                        if a >= 0 and a < votes.shape[0] and b >= 0 and b < votes.shape[1]:
                            votes[a, b, r] += 1

    circles = []

    for r in range(votes.shape[2]):
        threshold = 5 * np.pi * (r + minRadius)

        for x in range(votes.shape[0]):
            for y in range(votes.shape[1]):
                if votes[x, y, votes.shape[2] - r - 1] >= threshold:
                    found_close = False

                    for c in range(len(circles)):
                        if math.sqrt((x - circles[c][0]) * (x - circles[c][0]) + (y - circles[c][1]) * (y - circles[c][1])) < circles[c][2]:
                            if votes[x, y, votes.shape[2] - r - 1] > circles[c][3]:
                                circles.pop(c)

                            else:
                                found_close = True

                            break

                    if not found_close:
                        circles += [(x, y, votes.shape[2] - r - 1 + minRadius, votes[x, y, votes.shape[2] - r - 1])]

    for c in circles:
        drawCircle(image_copy, c[0], c[1], c[2])

    return image_copy

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Add more arguments")
        sys.exit(-1)

    minr = MIN_RADIUS
    maxr = MAX_RADIUS
        
    if len(sys.argv) >= 4:
        minr = (int) (sys.argv[2])
        maxr = (int) (sys.argv[3])

    hti = hough(sobel.parseImage(sys.argv[1]), minr, maxr)
    sobel.saveImage(hti, "hough-" + sys.argv[1])

