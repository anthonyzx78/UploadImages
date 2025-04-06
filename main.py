import pickle
import time
import os
import undetected_chromedriver as uc
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from tkinter import Tk
from tkinter.filedialog import askdirectory
from os import walk
from pynput.keyboard import Key, Controller

file_names = list()
# file_names_error = list()

# options = Options()
# options.add_argument("--window-size=600,600")

service = Service(executable_path="chromedriver.exe")
driver = uc.Chrome(service=service)
# driver.set_window_size(800, 600)
# driver.set_window_position(960, 540)

# os.system('cls' if os.name == 'nt' else 'clear')

path = askdirectory(title='Select Folder')
# print(path)
# print(path.replace("/", "\\"))
driver.get("https://www.plupload.com/examples/")

WebDriverWait(driver, 5).until(
    EC.presence_of_element_located(
        (By.XPATH, '//*[@id="uploader_browse"]/span[2]'))
)

inputElenent = driver.find_element(By.XPATH, '//*[@id="uploader_browse"]/span[2]')

Keyboard = Controller()

for root, dirc, files in walk(path):

    for FileName in files:

        inputElenent.click()
        time.sleep(1)
        Keyboard.type(f"{path.replace("/","\\")}\{FileName}")
        time.sleep(1)
        Keyboard.press(Key.enter)
        time.sleep(1)
        Keyboard.release(Key.enter)
        time.sleep(1)
        print(f"La imagen del terminal {FileName[:-4]} se ha subido satisfactoriamente.")
        time.sleep(1)
        # input()
        

# with open("file.txt", "w") as file:
#     file.write("")

# with open("file.txt", "a+") as file:
#     for i in sorted(file_names, key=len):
#         file.write(i.upper())
