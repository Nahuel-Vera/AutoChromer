import datetime
import os
import traceback


from driver_manager import DriverManager

def log_exception(e, contexto=""):
    # Crear nombre del archivo por DÍA
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = f"error_log_{fecha}.txt"

    # Crear carpeta logs si no existe
    base_path = DriverManager.get_base_path()
    log_dir = os.path.join(base_path, "logs")
    
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_filename)

    # (append) Agrega el nuevo error al archivo del día
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'='*70}\n")
        f.write(f"Fecha y Hora del error: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if contexto:
            f.write(f"Contexto: {contexto}\n")
        f.write(f"Tipo de error: {type(e).__name__}\n")
        f.write(f"Mensaje: {str(e)}\n")
        f.write("Traceback completo:\n")
        f.write(traceback.format_exc())
        f.write(f"{'='*70}\n")

    print(f"[!] Error registrado en {log_path}")

def log_exception_login_arba_afip(contexto=""):
    # Crear nombre del archivo por DÍA
    fecha = datetime.datetime.now().strftime("%Y-%m-%d")
    log_filename = f"error_log_{fecha}.txt"

    # Crear carpeta logs si no existe
    base_path = DriverManager.get_base_path()
    log_dir = os.path.join(base_path, "logs")
    
    os.makedirs(log_dir, exist_ok=True)

    log_path = os.path.join(log_dir, log_filename)

    # (append) Agrega el nuevo error al archivo del día
    with open(log_path, "a", encoding="utf-8") as f:
        f.write(f"\n{'*'*70}\n")
        f.write(f"Fecha y Hora del error: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        if contexto:
            f.write(f"Contexto: {contexto}\n")
        f.write(f"{'*'*70}\n")

    print(f"[!] Error registrado en {log_path}")