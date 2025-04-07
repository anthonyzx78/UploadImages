import os
import time
from os import walk
from tkinter import Tk
from tkinter.filedialog import askdirectory, askopenfile

import undetected_chromedriver as uc
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pynput.keyboard import Key, Controller


def seleccionar_carpeta():
    # Evita que se abra la ventana raíz de Tkinter
    Tk().withdraw()
    carpeta = askdirectory(title='Selecciona la carpeta con las imágenes')
    carpeta = carpeta.replace("/", "\\")
    if not carpeta:
        raise ValueError("No se seleccionó ninguna carpeta.")
    return carpeta


def iniciar_driver():
    Tk().withdraw()
    driverFile = askopenfile(title='Selecciona el driver')
    service = Service(executable_path=driverFile)
    driver = uc.Chrome(service=service)
    return driver


def subir_imagenes(driver, carpeta):
    # Acceder a la página
    driver.get("https://www.plupload.com/examples/")

    # Esperar a que el botón de subida esté presente
    espera = WebDriverWait(driver, 10)
    espera.until(EC.presence_of_element_located(
        (By.XPATH, '//*[@id="uploader_browse"]/span[2]')))

    # Encontrar el elemento que dispara la carga de archivos
    input_element = driver.find_element(
        By.XPATH, '//*[@id="uploader_browse"]/span[2]')

    keyboard = Controller()

    # Iterar sobre los archivos en la carpeta
    for root, _, files in walk(carpeta):
        for file_name in files:
            # Construir la ruta completa del archivo de forma segura
            ruta_archivo = os.path.join(carpeta, file_name)

            # Realizar la acción de carga
            try:
                input_element.click()
            except Exception as e:
                print(f"Error al hacer click en el elemento: {e}")
                continue

            # Espera fija; se puede reemplazar por espera dinámica si es necesario
            time.sleep(1)

            # Enviar la ruta del archivo por teclado usando pynput
            keyboard.type(ruta_archivo)
            time.sleep(1)
            keyboard.press(Key.enter)
            time.sleep(0.5)
            keyboard.release(Key.enter)
            time.sleep(1)

            # Separa la extensión del nombre usando os.path.splitext para mayor robustez
            nombre_sin_ext, _ = os.path.splitext(file_name)
            print(
                f"La imagen '{nombre_sin_ext}' se ha subido satisfactoriamente.")
            time.sleep(1)


def main():
    try:
        carpeta = seleccionar_carpeta()
    except ValueError as e:
        print(e)
        return

    driver = iniciar_driver()

    try:
        subir_imagenes(driver, carpeta)
    except Exception as e:
        print(f"Ocurrió un error durante el proceso: {e}")
    finally:
        driver.quit()


if __name__ == "__main__":
    main()
