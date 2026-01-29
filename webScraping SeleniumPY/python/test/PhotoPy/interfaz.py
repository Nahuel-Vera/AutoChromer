import tkinter as tk
import threading
import os
import sys
import time

import photoPy as ejecutar
from capturarErroresTXT import log_exception
from tkinter import messagebox
from driver_manager import DriverManager

class RedirectText:
    def __init__(self, widget, flush_interval=200, max_lines=1000):
        self.widget = widget
        self.buffer = ""
        self.flush_interval = flush_interval
        self.max_lines = max_lines
        self.widget.after(self.flush_interval, self.flush)


    def write(self, text):
        self.buffer += text


    def flush(self):
        if self.buffer:
            self.widget.insert(tk.END, self.buffer)
            self.widget.see(tk.END)
            self.buffer = ""
            # Limitar líneas
            total_lines = int(self.widget.index('end-1c').split('.')[0])
            if total_lines > self.max_lines:
                self.widget.delete('1.0', f'{total_lines - self.max_lines}.0')
        self.widget.after(self.flush_interval, self.flush)


class Interfaz:
    def __init__(self, root):
        self.root = root
        self.root.title("Autom chromer 2 pasos")
        self.root.geometry("800x600")
        self.ruta_excel = tk.StringVar()
        self.execution_thread = None
        self.create_widgets()


    def create_widgets(self):
        self.text_widget = tk.Text(self.root, wrap="word", height=20, width=80)
        self.text_widget.pack(pady=20, padx=20, fill=tk.BOTH, expand=True)

        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)

        #BOTONES:

        fila_botones = tk.Frame(self.root)
        fila_botones.pack(pady=20)

        self.btn_guardar_proceso = tk.Button(
            fila_botones,
            text="Ejecutar Proceso 1 (Manual)",
            command=self.guardar_proceso,
            bg="#127C12",
            fg="white"
        )
        self.btn_guardar_proceso.pack(side="left", padx=10)

        self.btn_ejecutar = tk.Button(
            fila_botones,
            text="Ejecutar",
            command=self.ejecutar_programa,
            bg="#2196F3",
            fg="white"
        )
        self.btn_ejecutar.pack(side="left", padx=10)


    def ejecutar_programa(self):
        driver_manager = DriverManager()
        base_dir = driver_manager.get_base_path()
        data_dir = os.path.join(base_dir, "data")
        proceso_file = os.path.join(data_dir, "proceso_data.json")
        if not os.path.exists(proceso_file):
            messagebox.showwarning(
                "Falta el Proceso 1",
                "Primero ejecutá el Proceso 1 (Manual)"
            )
            return

        self.btn_ejecutar.config(state=tk.DISABLED)
        self.execution_thread = threading.Thread(target=self.run_program)
        self.execution_thread.daemon = True
        self.execution_thread.start()
        self.check_thread()

    
    def guardar_proceso(self):
            self.btn_guardar_proceso.config(state=tk.DISABLED)
            self.execution_thread = threading.Thread(target=self.run_guardar_proceso)
            self.execution_thread.daemon = True
            self.execution_thread.start()
            self.check_thread()


    def run_program(self):
        try:
            ejecutar.main()
        except Exception as e:
            print(f"\nError durante la ejecución: {str(e)}")
            messagebox.showerror("Error de Ejecución", f"Ocurrió un error: {str(e)}")
            log_exception(e, contexto="Falla en ejecucion completa de programa")
            ejecutar.cerrar_driver()
            ejecutar.kill_all_chrome()
            ejecutar.cerrar_python()

    
    def run_guardar_proceso(self):
        try:
            ejecutar.guardar_proceso()
        except Exception as e:
            print(f"\nError durante la ejecución del PASO 1 (Manual): {str(e)}")
            messagebox.showerror("Error de Ejecución del PASO 1 (Manual)", f"Ocurrió un error: {str(e)}")
            log_exception(e, contexto="Falla en ejecucion completa de programa del PASO 1 (Manual)")
            ejecutar.cerrar_driver()
            ejecutar.kill_all_chrome()
            ejecutar.cerrar_python()

    def check_thread(self):
        if self.execution_thread and self.execution_thread.is_alive():
            self.root.after(300, self.check_thread)
        else:
            print("\nPrograma terminado.")
            self.btn_ejecutar.config(state=tk.NORMAL)



def on_closing(root, app):
    if app.execution_thread and app.execution_thread.is_alive():
        if messagebox.askyesno("Cerrar", "El programa aún está corriendo. ¿Quieres cerrar de todas formas?"):
            try:
                ejecutar.cerrar_driver()
                ejecutar.kill_all_chrome()
                ejecutar.cerrar_python()
            except Exception as e:
                print(f"Error cerrando el driver: {e}")
                log_exception(e, contexto="Falla al cerrar driver/python/chromes")
            root.destroy()
        else:
            return
    else:
        try:
            ejecutar.cerrar_driver()
            ejecutar.kill_all_chrome()
            ejecutar.cerrar_python()
        except Exception as e:
            print(f"Error cerrando el driver: {e}")
            log_exception(e, contexto="Falla al cerrar driver/python/chromes")
        root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = Interfaz(root)

    sys.stdout = RedirectText(app.text_widget)
    root.protocol("WM_DELETE_WINDOW", lambda: on_closing(root, app))
    root.mainloop()
