import time

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

def buscarPalabraPor_a(driver, palabra):
    time.sleep(2)
    try:
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.TAG_NAME, "a"))
        )
        elementos = driver.find_elements(By.TAG_NAME, "a")

        for elemento in elementos:
            if palabra in elemento.text:
                elemento.click()
                time.sleep(2)
                break
        else:
            return f"no existe el servicio {palabra} con el usuario"
    except ValueError:
        print("⚠️")
        

def cerrarSesionARBA(driver):
    boton = WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "fa-circle-user"))
        )
    boton.click()
    
    cerrar = WebDriverWait(driver, 12).until(
        EC.element_to_be_clickable((By.CLASS_NAME, "fa-right-from-bracket"))
    )
    cerrar.click()
    time.sleep(2)
    print("sesion CERRADA.")

# tomar captura por ID
def capturar_por_ID(driver, id, ruta_screenshot):
    time.sleep(2)
    try:
        # Obtener el elemento por su tag
        elemento = driver.find_element(By.ID, id)

        # Tomar la captura de pantalla del elemento
        elemento.screenshot(ruta_screenshot)

        print(f"Captura de pantalla del elemento '{id}' guardada en: {ruta_screenshot}")

    except Exception as e:
        print(f"Error al capturar la pantalla del elemento '{id}': {e}")

def buscarPalabraPor_ID(driver, id):
    """Verifica si un elemento con el ID dado está presente en el DOM y devuelve True/False."""
    time.sleep(2)
    try:
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.ID, id))
        )
        return True 

    except Exception:
        print(f"no encontre el ID")
        return False 

def capturar_por_tag_Dom(driver, ruta_screenshot):
    time.sleep(2)
    try:
        driver.set_window_size(800,2000)
        driver.maximize_window()
       # Obtener el elemento 'main'
        main_element = driver.find_element(By.TAG_NAME, "main")

        # Dentro de 'main', obtener el primer elemento 'section'
        section_element = main_element.find_element(By.TAG_NAME, "section")

        # Tomar la captura de pantalla del elemento 'section'
        section_element.screenshot(ruta_screenshot)

        driver.set_window_size(800,600)
        driver.maximize_window()

    except Exception as e:
        print(f"Error al capturar la pantalla del elemento Dom: {e}")

def capturar_por_tag(driver, tag, ruta_screenshot):
    time.sleep(2)
    try:
        # Obtener el elemento por su tag
        elemento = driver.find_element(By.TAG_NAME, tag)

        # Tomar la captura de pantalla del elemento
        elemento.screenshot(ruta_screenshot)

        print(f"Captura de pantalla del elemento '{tag}' guardada en: {ruta_screenshot}")

    except Exception as e:
        print(f"Error al capturar la pantalla del elemento '{tag}': {e}")

def buscarPalabraPor_Clase(driver, clase):
    """Verifica si un elemento con la clase dado está presente en el DOM y devuelve True/False."""
    time.sleep(2)
    try:
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CLASS_NAME, clase))
        )
        return True 

    except Exception:
        print(f"no encontre la clase")
        return False 

# tomar captura por elementos(tag)
def capturar_elemento(driver, seccion, ruta_screenshot):
    time.sleep(2)
    
    # Obtener las dimensiones del body
    elemento = driver.find_element(By.TAG_NAME, seccion)

    elemento.screenshot(ruta_screenshot)
    print(f"Captura de pantalla del body guardada en: {ruta_screenshot}")

def buscarPalabra(driver, palabra):
    time.sleep(2)
    try:
        WebDriverWait(driver, 12).until(
            EC.presence_of_element_located((By.CLASS_NAME, "bold"))
        )
        elementos = driver.find_elements(By.CLASS_NAME, "bold")

        for elemento in elementos:
            if palabra in elemento.text:
                driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", elemento)
                time.sleep(1)  # ✅ Espera extra tras scroll para evitar click interceptado
                elemento.click()
                time.sleep(2)
                return True  # Se encontró y se hizo clic

        return False  # No se encontró la palabra
    except Exception as e:
        print(f"⚠️ Error al buscar la palabra: {palabra}")
        #print(f"Tipo de error: {type(e).__name__}")
        #print(f"Mensaje: {str(e)}")
        #traceback.print_exc()
        return False
    
# tomar captura de pantalla completa
def capturar_pagina_completa(driver, ruta_screenshot):

    time.sleep(2)
    # Tomar la captura de pantalla de la ventana ajustada
    driver.save_screenshot(ruta_screenshot)
    print(f"Captura de pantalla guardada en: {ruta_screenshot}")

def espera_pres_cli(driver):
    try:
        # 1. Cambiar al iframe (con espera)
        iframe = WebDriverWait(driver, 20).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "iframe[src*='homeContribuyente']"))
        )
        driver.switch_to.frame(iframe)
        print("✅ Iframe localizado y cambiado")

        # 2. Esperar a que TODO cargue (solución universal)
        time.sleep(15)
        WebDriverWait(driver, 20).until(
            lambda d: d.execute_script("return document.readyState") == "complete"
        )
        time.sleep(5) # new
        print("🔄 Página completamente cargada dentro del iframe")
        return True

    except Exception as e:
        print(f"❌ problema en carga de AFIP CLI/PRES: {str(e)}")
        return False
    finally:
        print("volvi al iframe principal")
        driver.switch_to.default_content()

