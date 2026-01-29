import openpyxl
import os
import time
import glob
import datetime
import traceback
import re
import json


import capturarErroresTXT as erroresTXT
from driver_manager import DriverManager

from servicios.proceso_repetible import proceso_repetible

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


import shutil



#driver = None

#DATA_FILE = "proceso_data.json"
RUTA_EXCEL = ""

driver_manager = DriverManager()
BASE_DIR = driver_manager.get_base_path()
DATA_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(DATA_DIR, exist_ok=True)

DATA_FILE = os.path.join(DATA_DIR, "proceso_data.json")

#--------------------------------------------------------------------------------------------------------------------------
#cerrar y abrir el DRIVER y python
def cerrar_python():
    driver_manager.eliminar_procesos_python()

def iniciar_driver(headless):
    if headless == True:
        return driver_manager.create_driver("--headless")
    else:
        return driver_manager.create_driver(None)

def cerrar_driver():
    driver_manager.close_driver()

def kill_all_chrome():
    driver_manager._force_kill_all_chrome_instances()

def eliminar_contenido_directorio(ruta):
    if os.path.exists(ruta):
        for nombre in os.listdir(ruta):
            ruta_completa = os.path.join(ruta, nombre)
            try:
                if os.path.isfile(ruta_completa) or os.path.islink(ruta_completa):
                    os.remove(ruta_completa)
                elif os.path.isdir(ruta_completa):
                    shutil.rmtree(ruta_completa)
            except Exception as e:
                print(f"No se pudo eliminar {ruta_completa}: {e}")

#--------------------------------------------------------------------------------------------------------------------------
#Parte selenium
    
def CerrarVentanas(driver):
    time.sleep(2)
    
    # Guardar la ventana principal
    if len(driver.window_handles) == 0:
        print("No hay ventanas abiertas.")
        return

    main_window = driver.window_handles[0]

    # Cerrar todas las ventanas excepto la principal
    for handle in driver.window_handles:
        if handle != main_window:
            try:
                driver.switch_to.window(handle)
                driver.close()
            except:
                print(f"No se pudo cerrar la ventana: {handle}")
    
    # Volver a la ventana principal después de cerrar las demás
    try:
        driver.switch_to.window(main_window)
    except:
        print("La ventana principal ya no existe.")

    time.sleep(2)

def evitar_pop_ups(driver):
    driver.execute_cdp_cmd(
    "Page.addScriptToEvaluateOnNewDocument",
    {"source": "window.alert = function() {}; window.confirm = () => true;"}
    )


def capturar_xpath2(driver):
    driver.execute_script("""
        window.lastXPath = null;

        function getXPath(element) {
            if (element.id) return '//*[@id="' + element.id + '"]';
            if (element === document.body) return '/html/body';

            let ix = 0;
            const siblings = element.parentNode.children;

            for (let i = 0; i < siblings.length; i++) {
                const sibling = siblings[i];

                if (sibling === element) {
                    return getXPath(element.parentNode) + '/' +
                        element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                }

                if (sibling.tagName === element.tagName) {
                    ix++;
                }
            }
        }
        
        document.addEventListener("pointerdown", function (e) {
            window.lastXPath = getXPath(e.target);
        }, { once: true, capture: true });

    """)

    
    return WebDriverWait(driver, 9999).until(
        lambda d: d.execute_script("return window.lastXPath;")
    )


def capturar_xpath(driver):
    driver.execute_script("""
        window.lastXPath = null;

        function getXPath(element) {
            if (element.id) return '//*[@id="' + element.id + '"]';
            if (element === document.body) return '/html/body';

            let ix = 0;
            const siblings = element.parentNode.childNodes;

            for (let i = 0; i < siblings.length; i++) {
                const sibling = siblings[i];

                if (sibling === element) {
                    return getXPath(element.parentNode) + '/' +
                        element.tagName.toLowerCase() + '[' + (ix + 1) + ']';
                }

                if (sibling.nodeType === 1 &&
                    sibling.tagName === element.tagName) {
                    ix++;
                }
            }
        }

        // Capturás pointerdown (NO lo cancelás)
        document.addEventListener("pointerdown", function (e) {
            window.lastXPath = getXPath(e.target);
        }, { once: true, capture: true });

        // Cancelás el click que navega
        document.addEventListener("click", function (e) {
            e.preventDefault();
            e.stopPropagation();
        }, { once: true, capture: true });

    """)
	
    return WebDriverWait(driver, 9999).until(
        lambda d: d.execute_script("return window.lastXPath;")
    )



def clickear_xpath(driver, xpath):
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.XPATH, xpath))
        ).click()
        # driver.find_element(By.XPATH, xpath).click()
        time.sleep(2)

    except Exception as e:
        print("Error clickeando el xpath ", xpath)
        print(f"Tipo de error: {type(e).__name__}\n")
        print(f"Mensaje: {str(e)}\n")


# Automatización con Selenium
def abrir_pagina_login(driver):
    #base_path = driver_manager.get_base_path()

    #logs para detectar errores por secciones
    flags_errores = {
        "lufe": False,
    }


    try:
        
        driver.maximize_window()
        #--------------------------------------------------------------------------------------------------
        #comienzo de navegacion...
        driver.get("https://www.google.com")
        time.sleep(2)
        
        xpaths = []
        for i in range(5):  # hoy 5, mañana lo que quieras
            print(f"Esperando click #{i+1}")
            xpath = capturar_xpath(driver)
            xpaths.append(xpath)

            print("Capturado:", xpath)
            clickear_xpath(driver, xpath)
             
            print("xpath clickeado: ", xpath)
            print("paso:", i+1)

            
        print("XPaths recibido en Python:", xpaths)

        return flags_errores, xpaths
        #----------------------------------------------------------------------------------------------------------
        #END
        
    except Exception as e:
        print("Error durante la automatización en la primera parte:", e)
        erroresTXT.log_exception(e,f" Error durante la automatización en la primera parte")
        print(f"error")
        return flags_errores, xpaths
    finally:
        cerrar_driver()
        #kill_tagged_chromes()
        #driver.quit()


def guardar_proceso():
    #xpaths = []
    driver = iniciar_driver(headless=False)
    evitar_pop_ups(driver)
    time.sleep(1)

    flags_errores, xpaths = abrir_pagina_login(driver)
    time.sleep(10)
    print(flags_errores)
    data = {
        "flags_errores": flags_errores,
        "xpaths": xpaths,
        "timestamp": time.time()
    }
    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    print("Proceso 1 completado. Datos guardados en JSON.")


#main

def main():
    #base_path = driver_manager.get_base_path()

    if not os.path.exists(DATA_FILE):
        raise Exception("No existe el archivo del Proceso 1")

    with open(DATA_FILE, "r", encoding="utf-8") as f:
        data = json.load(f)

    xpaths = data.get("xpaths")
    flags_errores = data.get("flags_errores")

    if not xpaths:
        raise Exception("El archivo JSON no contiene XPaths válidos")


    try:
        driver2= iniciar_driver(headless=True)
        evitar_pop_ups(driver2)
        driver2.maximize_window()
        driver2.get("https://www.google.com")
        time.sleep(2)

        for xpath in xpaths:
            time.sleep(3)
            WebDriverWait(driver2, 12).until(EC.element_to_be_clickable((By.XPATH, xpath)))
            driver2.find_element(By.XPATH, xpath).click()
            print("se hizo el click donde anteriormente se busco en xpath: ",xpath)
    except Exception as e:
        print("Error en Proceso 2:", e)
        print(f"Tipo de error: {type(e).__name__}\n")
        print(f"Mensaje: {str(e)}\n")
        raise
    finally:
        cerrar_driver()
    time.sleep(2)