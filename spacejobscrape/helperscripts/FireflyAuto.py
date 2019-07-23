'''
Author: JJ Fiedler
'''

from selenium import webdriver
import pyautogui
import pyperclip
import platform
import os

def run():

    #Uses webdriver and chromedriver to open the job site
    chromedriver = "/Users/JJ/Documents/ProgrammingStuff/PythonFiles/jobsitewebscrape/spacejobscrape/helperscripts/chromedriver"
    driver = webdriver.Chrome(chromedriver)
    driver.get("https://workforcenow.adp.com/mascsr/default/mdf/recruitment/recruitment.html?cid=241aedef-e1d0-4fca-8d2a-bb3ff0afed85&ccId=19000101_000001&type=JS&lang=en_US")
    driver.set_window_position(0, 0)
    driver.set_window_size(1280, 800)

    #Setting screen boundaries
    pyautogui.PAUSE = 10
    xDefault, yDefault = 1280, 800
    pyautogui.PAUSE = 1
    x = (xDefault / 2) + 5
    y = yDefault / 2

    #Opening inspect tool in Google Chrome
    pyautogui.rightClick(x, y)
    pyautogui.PAUSE = 1
    x = x + 40
    y = y + 180
    pyautogui.click(x, y)
    pyautogui.PAUSE = 1

    #Setting choordinates to where the network tab lies
    x = xDefault * .814698
    y = yDefault * .200250313

    #Moving to the network tab
    pyautogui.moveTo(x, y, 2)
    pyautogui.PAUSE = 1

    #Clicking the network tab
    x, y = pyautogui.position()
    pyautogui.PAUSE = 1
    pyautogui.click(x, y)
    pyautogui.PAUSE = 1

    #Setting the choordinates to the XHR subtab
    x = x-260
    y = y+72
    #Clicking the XHR tab
    pyautogui.click(x, y)
    pyautogui.PAUSE = 1

    #Setting the choordinates for the open tab in the webbrowser
    x = xDefault * .15324472
    y = yDefault * .05632040

    #Clicking the reload button
    pyautogui.rightClick(x, y)
    pyautogui.PAUSE = 1
    x = x + 50
    y = y + 40
    pyautogui.click(x, y)

    #Scrolling down to load all API request links
    y = y + 300
    pyautogui.moveTo(x, y, 3)
    pyautogui.scroll(-40, pause=1)

    #Clicking the first API request tab
    x = xDefault * .61688819
    y = yDefault * .536921151
    pyautogui.click(x, y)

    #Clicking the header tab
    x = xDefault * .763096169
    y = yDefault * .429286608
    pyautogui.click(x, y)

    #Copying the first link
    x = xDefault * .816262705
    y = yDefault * .602002503
    pyautogui.moveTo(x, y)
    x = xDefault * .810789679
    y = yDefault * .49436796
    pyautogui.dragTo(x, y, button='left')

    #Detecing os to determine proper copy shortcut
    if platform.system()=="Darwin":
        pyautogui.hotkey('command', 'c')
    else:
        pyautogui.hotkey('ctrl', 'c')

    # "Pasting" the copied link
    jsonLink1 =  pyperclip.paste()

    #Clicking the second API request tab
    x = xDefault * .61688819
    y = yDefault * .56320401
    pyautogui.click(x, y)

    #Copying the second link
    x = xDefault * .86395622
    y = yDefault * .602002503
    pyautogui.moveTo(x, y)
    x = xDefault * .810789679
    y = yDefault * .49436796
    pyautogui.dragTo(x, y, button='left')

    #Detecing os to determine proper copy shortcut
    if platform.system()=="Darwin":
        pyautogui.hotkey('command', 'c')
    else:
        pyautogui.hotkey('ctrl', 'c')

    # "Pasting" the copied link
    jsonLink2 = pyperclip.paste()

    links = [jsonLink1, jsonLink2]

    return links
    driver.close()