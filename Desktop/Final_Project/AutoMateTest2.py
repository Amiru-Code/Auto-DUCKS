#AutoMateTest2
import pytest
from AutoMate import readConfig, initializationSettings
import csv

#def TestReadConfig():
#    list = readConfig('AutoMateConfig.csv')
#    print(list[3][1])
#
#TestReadConfig()

def test_initializationSettings():
    initializationSettings('y')

config = []
numberOfTimes = int(input('enter the number of times it should run: '))
count = int(input('Enter the desired count enter 0 for the default of 1000000: ')) 
file = input('What is the filename? use _ for spaces: ')
filepath = readConfig("AutoMateConfig.csv")[3][1]
if count == 0:
    count = 1000000

with open("userConfig.csv", mode='w', newline='') as configFile:
    configWriter = csv.writer(configFile)
    configWriter.writerow(['numberOfTimes', numberOfTimes])
    configWriter.writerow(['count', count])
    configWriter.writerow(['filename', file])
    configWriter.writerow(['filepath', filepath])
test_initializationSettings()
