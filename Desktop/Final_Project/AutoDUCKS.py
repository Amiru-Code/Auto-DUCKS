import pyautogui
import time
from datetime import datetime
from PIL import Image
import pytesseract
import csv
import tkinter as tk
from tkinter import Frame, Label, Button

def main():
    buildGUI()



#Gets user inputs and returns a config dictionary
#The amount of times I have rewritten this function is unfortunate
def initializationSettings(alterConfig): 
    if alterConfig == 'y':

        numberOfTimes = int(input('enter the number of times it should run: '))
        count = int(input('Enter the desired count enter 0 for the default of 1000000: '))
        filename = input('What is the filename? use _ for spaces: ')
        filepath = readConfig("AutoMateConfig.csv")['filepath']

        if count == 0:
            count = 1000000
        
        config = {
            "numberoftimes": numberOfTimes,
            "count": count,
            "filename": filename,
            "filepath": filepath,
    }
        
        return config
    
    elif alterConfig == 'n':
        return readConfig("AutoMateConfig.csv")
    

#This function writes the last settings used into a CSV file called userconfig.csv 
def lastConfigUsed(config):
    with open('userConfig.csv', mode = 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Parameters', 'value'])
        for key, value in config.items():
            writer.writerow([key, value])
                     
       
# This is definitely one of my favorite functions, it takes a csv file and writes it into a dictionary 
def readConfig(filename):
    config = {}
    with open(filename, newline='') as configFile:
        reader = csv.reader(configFile)
        for row in reader:
            if not row:
                continue
            key = row[0].strip().lower()
            value = row[1] if len(row) > 1 else None
            config[key] = value
    return config

def buildGUI():
    #Tkinter root object
    root = tk.Tk()

    #create main window 
    mainFrame = Frame(root)
    mainFrame.master.title("Auto DUCKS")
    mainFrame.pack(padx=192, pady=192, fill=tk.BOTH, expand=1)

    populateMainWindow(mainFrame)

    root.mainloop()


def populateMainWindow(mainFrame):

    # --- Labels + Entries ---
    Label(mainFrame, text="Number of Runs").grid(row=0, column=0, sticky="w")
    entryRuns = tk.Entry(mainFrame, width=10)
    entryRuns.grid(row=0, column=1)

    Label(mainFrame, text="Count (0 = 1,000,000)").grid(row=1, column=0, sticky="w")
    entryCount = tk.Entry(mainFrame, width=10)
    entryCount.grid(row=1, column=1)

    Label(mainFrame, text="Filename").grid(row=2, column=0, sticky="w")
    entryFilename = tk.Entry(mainFrame, width=30)
    entryFilename.grid(row=2, column=1)

    Label(mainFrame, text="Time Between Runs (sec)").grid(row=3, column=0, sticky="w")
    entryDelay = tk.Entry(mainFrame, width=10)
    entryDelay.grid(row=3, column=1)

    # --- Button callbacks ---
    def loadDefaults():
        config = readConfig("AutoMateConfig.csv")
        entryRuns.delete(0, tk.END)
        entryRuns.insert(0, config.get("numberoftimes", ""))

        entryCount.delete(0, tk.END)
        entryCount.insert(0, config.get("count", ""))

        entryFilename.delete(0, tk.END)
        entryFilename.insert(0, config.get("filename", ""))

    def runProgram():
        numberOfTimes = int(entryRuns.get())
        count = int(entryCount.get())
        filename = entryFilename.get()
        delay = float(entryDelay.get() or 0)

        if count == 0:
            count = 1_000_000

        filepath = readConfig("AutoMateConfig.csv")["filepath"]

        config = {
            "numberoftimes": numberOfTimes,
            "count": count,
            "filename": filename,
            "filepath": filepath
        }

        lastConfigUsed(config)
        killScript()

        region = (150, 449, 86, 24)

        executeProgram(
            numberOfTimes=numberOfTimes,
            count=count,
            fileName=filename,
            region=region,
            filepath=filepath
        )

    # --- Buttons ---
    Button(mainFrame, text="Load Defaults", command=loadDefaults).grid(row=4, column=0, pady=10)
    Button(mainFrame, text="Run", command=runProgram).grid(row=4, column=1, pady=10)




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
    

def scrCoor(PNGfilename):
    try:
        coordinates = pyautogui.locateCenterOnScreen(PNGfilename)
        if coordinates != None:

         return coordinates
        else: 
            print('Image not found with specified confidence. ')
    except pyautogui.ImageNotFoundException:
        print('Image not found ')
    

def executeProgram(numberOfTimes, count, fileName, region, filepath):
    try:

        i = 0

        while i < numberOfTimes:
            number = getNumberFromScreen(region)
            print(f"Detected: {number}")

            if number >= count:
                print("Target reached! Click..")
                time.sleep(0.5)

                # click on the export data
                export = scrCoor("Export.PNG")
                if export is None:
                    print("Export.PNG not found! You might need to get a new screenshot of the export button. Put it into the same \n directory as this script named Export.PNG")
                    input("Press Enter to end the script...")
                    exit()
                pyautogui.click(export)
                print(f"Clicked at ({export})")
                time.sleep(1)  # delay 2 seconds between click

                # file name with datetime
                filenameWithTime = datetime.now().strftime(f"{fileName}_%Y%m%d_%H%M%S")
                pyautogui.write(filenameWithTime, interval=0.01)

                # go to the address bar and go to the filepath
                pyautogui.hotkey('alt', 'd')
                pyautogui.write(filepath, interval=0.01)
                pyautogui.press('enter')

                #save the file 
                pyautogui.hotkey('enter')

                # click the clear button
                pressClear = scrCoor('c.PNG')
                if pressClear is None:
                    print("c.PNG not found! You might need to get a new screenshot of the clear button. Put it into the same \n directory as this script named c.PNG")
                    input("Press Enter to end the script...")
                    exit()
                pyautogui.click(pressClear)
                print(f'clicked at {pressClear}')
                time.sleep(4)

                # click on the start button
                pressStart = scrCoor('start.PNG')
                if pressStart is None:
                    print("start.PNG not found! You might need to get a new screenshot of the start button. Put it into the same \n directory as this script named start.PNG")
                    input("Press Enter to end the script...")
                    exit()
                pyautogui.click(pressStart)
                time.sleep(4)

                i += 1
                print(f"Completed {i} out of {numberOfTimes} runs.")

    except pyautogui.FailSafeException:
        print("Stopped: Mouse moved to top-left corner (0,0).")
    

if __name__ == "__main__":
    main()
    