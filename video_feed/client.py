import cv2
import socket
import numpy as np

image = cv2.imread("Barrel1.png", cv2.IMREAD_COLOR)
print("Image shape: "  + str(image.shape))
image = image.reshape(309, 227, 3)
print("Image size: " + str(image.size))

# debug code because I don't know a good python debugger, yet
# print(type(image))
# print(type(image[0]))
# print(type(image[0][0]))
# print(type(image[0][0][0]))

imageBytes = image.tobytes(order='C')

# debug code because I don't know a good python debugger, yer (it's on my TODOs, now)
# print("Image bytes:")
# print(imageBytes)

sock = socket.socket()

sock.connect(('127.0.0.1', 80))
sock.sendall(imageBytes)
sock.close()
