import pyautogui
import time
from datetime import datetime
from PIL import Image
import pytesseract
import csv

def main():
    #Write to a config file instead of only getting these inputs, have the inputs write to a config and read from that.
    alterConfig = input('Do you want to edit the bounds of this run? (y/n): ')
    i = 0
    if alterConfig == 'no':
        config = readConfig("AutoMateConfig.csv")
        numberOfTimes = config[0][1]
        count = config[1][1]
        file = config[2][1]
        


    killScript() 

    #Set Tesseract to the path
    pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

    # region = (x,y,width, height)
    region = (150,449,86,24) #region is top-left corner (x,y) and width height
    

    executeProgram(numberOfTimes, count, file, region, i)


def initializationSettings():
    alterConfig = input('Do you want to edit the bounds of this run? (y/n): ')
    

    
    numberOfTimes = int(input('enter the number of times it should run: '))
    count = int(input('Enter the desired count enter 0 for the default of 1000000: ')) 
    file = input('What is the filename? use _ for spaces: ')
    if count == 0:
        count = 1000000
    


def readConfig(filename):
    config = []
    with open(filename, newline='') as configFile:
        configList = csv.reader(configFile)
        for row in configList:
            config.append(row)

    return config


def killScript():
    print("Allow you to kill the script by moving your mouse to the top-left corner (0,0)")
    pyautogui.FAILSAFE = True
    #time it take before auto start:
    duration = 5 # seconds
    print("starting click in 5 seconds. Move mouse to TOP-LEFT to stop.")
    time.sleep(duration)



def getNumberFromScreen(region):
    screenshot = pyautogui.screenshot(region=region)
    gray = screenshot.convert('L') #greyscale = better OCR
    text = pytesseract.image_to_string(gray, config = '--psm 7 digits')
    digits = ''.join(filter(str.isdigit, text))
    return int(digits) if digits else 0


def scrCoor(filename):
    coordinates = pyautogui.locateCenterOnScreen(filename)
    return coordinates


def executeProgram(numberOfTimes, count, file, region, i, filepath):
    try:
        

        while True and i < numberOfTimes:
            number = getNumberFromScreen(region)
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
                filename = datetime.now().strftime(f"{filepath}_%Y%m%d_%H%M%S")
                pyautogui.write(filename, interval=0.01)

                pyautogui.hotkey('alt' + 'd')
                pyautogui.write(file)
                pyautogui.hotkey('Enter')

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

if __name__ == "__main__":
    main()