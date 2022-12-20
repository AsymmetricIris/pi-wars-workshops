import cv2
import socket
import time
import numpy as np

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

host = "127.0.0.1"
port = 80

sock.bind((host, port))
sock.listen(1)
conn, addr = sock.accept()
print("Connection from:", str(addr))

imageBytes = conn.recv(4000098)
print("Received data")
# print("Image bytes:")
# print(imageBytes)
imageData = np.frombuffer(imageBytes, dtype=np.uint8)
# print("Image data:")
# print(type(imageData))
# print(type(imageData[0]))
# print(imageData)
image = imageData.reshape(309, 227, 3)

cv2.imshow("image", image)
cv2.waitKey(0)
cv2.destoryallwindows()
conn.close()
