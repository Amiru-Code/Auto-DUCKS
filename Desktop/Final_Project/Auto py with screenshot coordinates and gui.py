import pyautogui
import time
from datetime import datetime
from PIL import Image
import pytesseract
#use X,Y Coordinate.py to find the right cordinate if needed
#change the click coordinate if needed
#add click points if needed
i = 0
numberOfTimes = int(input('enter the number of times it should run: '))
count = int(input('Enter the desired count enter 0 for the default of 1000000: ')) 
file = input('What is the filename? use _ for spaces: ')
if count == 0:
     count = 1000000

print("Allow you to kill the script by moving your mouse to the top-left corner (0,0)")
pyautogui.FAILSAFE = True
#time it take before auto start:
duration = 5 # seconds
print("starting click in 5 seconds. Move mouse to TOP-LEFT to stop.")
time.sleep(duration)

#Set Tesseract to the path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# detect the region
region = (150,449,86,24) #region is top-left corner (x,y) and width height
# region = (x,y,width, height)
def get_number_from_screen():
    screenshot = pyautogui.screenshot(region=region)
    gray = screenshot.convert('L') #greyscale = better OCR
    text = pytesseract.image_to_string(gray, config = '--psm 7 digits')
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else 0

def scrCoor(filename):
    coordinates = pyautogui.locateCenterOnScreen(filename)
    return coordinates

try:
    

    while True and i < numberOfTimes:
        number = get_number_from_screen()
        print(f"Detected: {number}")

        if number >= count:
            print("Target reached! Click..")
            time.sleep(0.5)

            # click on the export data
            export = scrCoor("Export.PNG")
            pyautogui.click(export)
            print(f"Clicked at ({export})")
            time.sleep(1)  # delay 2 seconds between click

            # file name with datetime
            filename = datetime.now().strftime(f"{file}_%Y%m%d_%H%M%S")
            pyautogui.write(filename, interval=0.01)

            # click on PAS Fall 2025
            fall2025 = scrCoor('Fall2025.PNG')
            pyautogui.click(fall2025)
            print(f"Clicked at ({fall2025})")
            time.sleep(0.5)


            # click on data(auto)
            dataAuto = scrCoor('DataAuto.PNG')
            pyautogui.doubleClick(dataAuto)
            print(f"Clicked at ({dataAuto})")
            time.sleep(0.5)


            # type it in and save
            pyautogui.hotkey('Enter')

            # click the clear button
            pressClear = scrCoor('c.PNG')
            pyautogui.click(pressClear)
            print(f'clicked at {pressClear}')
            time.sleep(4)

            # click on the start button
            pressStart = scrCoor('start.PNG')
            pyautogui.click(pressStart)
            time.sleep(4)

            i += 1

except pyautogui.FailSafeException:
    print("Stopped: Mouse moved to top-left corner (0,0).")
