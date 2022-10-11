import sys
import cv2
import numpy as np
from PIL import Image
import pyocr
import tempfile

IMAGE_PATH = 'images/result.jpg'
NAME = "result"

# original image
img = cv2.imread(IMAGE_PATH)


with tempfile.TemporaryDirectory() as tmpdir:
    # ==== title =====
    img_title = img[0 : 50, 100: 600]
    cv2.imwrite(f'{tmpdir}/title.jpg', img_title)


    # ===== difficulty =====
    img_difficulty_cut = img[50 : 95, 105: 250]

    # grayscale conversion
    img_difficulty_gray = cv2.cvtColor(img_difficulty_cut, cv2.COLOR_BGR2GRAY)

    # binarization
    img_difficulty_bit = cv2.bitwise_not(img_difficulty_gray)

    # output
    cv2.imwrite(f'{tmpdir}/difficulty.jpg', img_difficulty_bit)


    # ===== max_combo =====
    img_maxCombo_cut = img[450 : 630, 140: 460]

    # grayscale conversion
    img_maxCombo_gray = cv2.cvtColor(img_maxCombo_cut, cv2.COLOR_BGR2GRAY)

    # binarization
    img_maxCombo_bit = cv2.bitwise_not(img_maxCombo_gray)

    # output
    cv2.imwrite(f'{tmpdir}/maxCombo.jpg', img_maxCombo_bit)


    # ===== notes =====
    img_notes = img[445 : 630, 605 : 705]
    cv2.imwrite(f'{tmpdir}/notes.jpg', img_notes)


    # result
    # lang = eng or jpn
    tools = pyocr.get_available_tools()
    if len(tools) == 0:
        print("No OCR tool found.\n")
        sys.exit(1)
    tool = tools[0]

    text = tool.image_to_string(Image.open(f'{tmpdir}/title.jpg'), lang="jpn")
    print(f"Title : {text}")

    text = tool.image_to_string(Image.open(f'{tmpdir}/difficulty.jpg'), lang="jpn")
    print(f"Difficulty : {text}")

    text = tool.image_to_string(Image.open(f'{tmpdir}/maxCombo.jpg'), lang="eng")
    print(f"Max combo : {text}")

    print("Notes judge :")
    text = tool.image_to_string(Image.open(f'{tmpdir}/notes.jpg'), lang="eng")
    data = text.splitlines()
    judge = ["PERFECT", "GREAT", "GOOD", "BAD", "MISS"]
    for i in range(5):
        print(f"{judge[i]} - {data[i]}")
    
