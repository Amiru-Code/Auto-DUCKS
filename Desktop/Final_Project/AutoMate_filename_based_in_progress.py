import pyautogui
import time
from datetime import datetime
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
def find_text_coordinates(target_text):
    screenshot = pyautogui.screenshot()
    img = screenshot.convert('RGB')

    
    data = pytesseract.image_to_data(img, output_type=pytesseract.Output.DICT)

    for i, word in enumerate(data['text']):
        if word.strip().lower() == target_text.strip().lower() or target_text.strip().lower() == word.strip().lower():
            x = data['left'][i]
            y = data['top'][i] 
            w = data['width'][i] 
            h = data['height'][i] 
            center_x = int(x + w // 2)
            center_y = int(y + h // 2)

            print(f"Found '{target_text}' at ({center_x}, {center_y})")
            return (center_x, center_y)


        print (f"Could not find '{target_text}' on screen.")
        print ([word.strip() for word in data['text'] if word.strip()])
        return None
    





# detect the region
region = (172,325,214,343)
def get_number_from_screen():
    screenshot = pyautogui.screenshot(region=region)
    gray = screenshot.convert('L') #greyscale = better OCR
    text = pytesseract.image_to_string(gray, config = '--psm 7 digits')
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else 0
try:
    while True:
        #number = get_number_from_screen()
        #print(f"Detected: {number}")

        #if number >= 100000:
            #print(" Target reached! Click..")
            time.sleep(1)

        
            #click on the export data
            pyautogui.click(x=1593, y=43)
            print("Clicked at x = 1593, y =43")
            time.sleep(3)
             #delay 2 seconds between click

            #click on desktop
            pyautogui.click(find_text_coordinates('@@SS'))
            print(f'Clicked at {find_text_coordinates("@@SS")}')
            time.sleep(3000) #delay 2 seconds between click
            
            #click on PAS srping 2025
            pyautogui.doubleClick(x=267, y=480)
            print("Clicked at (301, 421) ")
            time.sleep(2) #delay 2 seconds between click

            #click on data(auto)
            pyautogui.doubleClick(x=297, y=170)
            print("Clicked at (267, 160) ")
            time.sleep(2) #delay 2 seconds between click

            #click on filename
            pyautogui.click(x=424, y=829)
            print("Clicked at (162, 823) ")
            time.sleep(2) #delay 2 seconds between click

            #file name with dattime:
            filename = datetime.now().strftime("Zeolite_without_Source_%Y%m%d_%H%M%S")

            #type it in and save:
            pyautogui.write(filename, interval= 0.1)
            pyautogui.click(x=1192, y = 900)

             #click the restart button:
            pyautogui.click(x=959, y=95)

            #CLICK ON THE START BOTTON
            pyautogui.click(x=1000, y =89)
            time.sleep(1) #delay 2 minutes between click

            pyautogui.click(x=954, y=82)
            
except pyautogui.FailSafeException:
    print(" Stopped: Mouse moved to top-left corner (0,0).")
