from pytesseract import pytesseract
import os
import re
import cv2
import numpy as np

if __name__ == '__main__':
    pytesseract.tesseract_cmd = "C:/Program Files/Tesseract-OCR/tesseract.exe"
    pattern = r'dog #(\d+)'
    input_dir = r'images/'
    custom_config = '--oem 3 --psm 11'
    all_matches = []

    for root, dirs, filenames in os.walk(input_dir):
        for filename in filenames:
            try:
                img_low = cv2.imread(input_dir + filename)
                if img_low is None:
                    print(f"Could not read: {filename}")
                    continue

                text = pytesseract.image_to_string(img_low, config=custom_config)
                matches = re.findall(pattern, text, re.IGNORECASE)
                all_matches.extend(matches)

            except Exception as e:
                print(f"Failed on {filename}: {e}")
                continue

    all_matches = sorted(set(all_matches), key=lambda x: int(x))
    full_range = range(int(all_matches[0]), int(all_matches[-1]) + 1)
    missing = [str(n) for n in full_range if str(n).zfill(3) not in all_matches and str(n) not in all_matches]

    for i, m in enumerate(all_matches):
        if i > 0 and int(m) != int(all_matches[i - 1]) + 1:
            print('-----')
        print(f"dog #{m.zfill(3)}")

    print('\n' + '='*20)
    print("MISSING:")
    for m in missing:
        print(f"dog #{str(m).zfill(3)}")