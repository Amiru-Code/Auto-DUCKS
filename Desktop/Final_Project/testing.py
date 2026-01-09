import pyautogui
import time
from PIL import Image
import pytesseract

print("Allow you to kill the script by moving your mouse to the top-left corner (0,0)")
pyautogui.FAILSAFE = True
#time it take before auto start:
duration = 5 # seconds
print("starting click in 5 seconds. Move mouse to TOP-LEFT to stop.")
time.sleep(duration)

#Set Tesseract to the path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

#FUNCTION TO scan the screen and find the coordinates of the filename we want to click on:
def find_text_coordinates(target_text, scale=2.0):
    screenshot = pyautogui.screenshot()
    img = screenshot.convert('RGB')

    width, height = img.size
    
    resized_img = img.resize((int(width * scale), int(height * scale)))
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data['text']):
        if word.strip().lower() == target_text.strip().lower():
            x = data['left'][i] // scale
            y = data['top'][i] // scale
            w = data['width'][i] // scale
            h = data['height'][i] // scale

            center_x = int(x + w / 2)
            center_y = int(y + h / 2)

            print(f"Found '{target_text}' at ({center_x}, {center_y})")
            return (center_x, center_y)


        print (f"Could not find '{target_text}' on screen.")
        print ([word.strip() for word in data['text'] if word.strip()])
        return None

find_text_coordinates('PAPPy')
