import sys
import cv2
import numpy as np
from PIL import Image
import pyocr

IMAGE_PATH = 'images/result.png'
NAME = "result"

#original
img = cv2.imread(IMAGE_PATH)
cv2.imwrite(f'1_{NAME}_original.png', img)

#gray
img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
cv2.imwrite(f'2_{NAME}_gray.png', img)

#threshold
th = 140
img = cv2.threshold(
    img,
    th,
    255,
    cv2.THRESH_BINARY
)[1]
cv2.imwrite(f'3_{NAME}_threshold_{th}.png', img)

#bitwise
img = cv2.bitwise_not(img)
cv2.imwrite(f'4_{NAME}_bitwise.png', img)

cv2.imwrite('target.png', img)


tools = pyocr.get_available_tools()
if len(tools) == 0:
    print("No OCR tool found")
    sys.exit(1)
tool = tools[0]
text = tool.image_to_string(Image.open('target.png'), lang="eng") # eng or jpn

print(text)