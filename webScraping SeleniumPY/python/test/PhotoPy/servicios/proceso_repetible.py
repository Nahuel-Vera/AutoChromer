import time

import capturarErroresTXT as erroresTXT

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def proceso_repetible(driver, flags_errores):
    # seteo variables
    max_reintentos = 2
    intentos = 0
    exito = False

    while intentos < max_reintentos and not exito:
        try:
            intentos += 1
            #proceso a realizar
            #....

            exito = True
        except Exception as e:
            if intentos < max_reintentos:
                print("Reintentando... en 25 segundos\n")
                time.sleep(25)
            else:
                flags_errores["lufe"] = True
                erroresTXT.log_exception(e,f"error en seccion")
                print(f"error en seccion")
                print(f"Tipo de error: {type(e).__name__}")
                print(f"Mensaje: {str(e)}")
                print("Se alcanzó el número máximo de intentos. Abortando...\n")