import ctypes
import os
import signal
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import psutil
import time
import subprocess
import atexit

class DriverManager:
    def __init__(self):
        self._driver = None
        self._download_dir = None
        self._unique_marker = f"--selenium-marker-{os.getpid()}"  # Marcador único por instancia

    @staticmethod
    def get_base_path():
        paths_to_check = [
            os.path.join(os.path.expanduser("~"), "Desktop", "Git", "python", "Autom chromer"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Git", "python", "Autom chromer"),
            os.path.dirname(os.path.abspath(__file__))
        ]
        
        for path in paths_to_check:
            if os.path.isdir(path):
                return path
        return os.path.dirname(os.path.abspath(__file__))

    def _kill_process_tree(self, pid):
        """Mata un proceso y todos sus hijos de forma más segura"""
        try:
            parent = psutil.Process(pid)
            children = parent.children(recursive=True)
            
            # Primero matar a los hijos
            for child in children:
                try:
                    if child.is_running():
                        child.kill()
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Esperar un momento
            time.sleep(0.1)
            
            # Luego matar al padre si todavía existe
            if parent.is_running():
                parent.kill()
                
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            pass

    def _cleanup_chrome_processes(self):
        """Limpieza específica de procesos Chrome iniciados por este programa"""
        target_processes = ['chrome.exe', 'chromedriver.exe']
        
        for proc in psutil.process_iter(['pid', 'name', 'cmdline', 'create_time']):
            try:
                if not proc.info['name'] or proc.info['name'].lower() not in target_processes:
                    continue
                    
                cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''
                
                # Verificar si es un proceso de nuestro programa
                if (self._unique_marker in cmdline or  # Nuestro marcador
                    (proc.info['name'].lower() == 'chromedriver.exe' and 
                    '--port=' in cmdline)):  # Chromedriver iniciado por nosotros
                    
                    print(f"Terminando proceso de nuestro programa: {proc.info['name']} (PID: {proc.pid})")
                    self._kill_process_tree(proc.pid)
                    
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                continue


    def create_driver(self, headless):
        """Crea una instancia del WebDriver con configuración optimizada"""
        if self._driver:
            try:
                # Verificar si el driver existente sigue siendo válido
                self._driver.current_url
                return self._driver
            except:
                self._driver = None

        base_path = self.get_base_path()
        self._download_dir = os.path.join(base_path, "Descargas")
        os.makedirs(self._download_dir, exist_ok=True)

        options = webdriver.ChromeOptions()
        options.binary_location = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        
        # Configuración de opciones (tus argumentos existentes)
        chrome_args = [
            f"{self._unique_marker}",  # Marcador único
            #"--headless",
            "--disable-software-rasterizer",
            "--ignore-certificate-errors",
            "--enable-unsafe-swiftshader",
            "--no-sandbox",
            "--enable-logging",
            "--disable-gpu",
            "--window-size=1280,1600",  # Tamaño de ventana
            "--force-device-scale-factor=0.70",
            "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.6998.99 Safari/537.36",
            # "--disable-features=BlockInsecurePrivateNetworkRequests",
            # "--disable-features=PrivateNetworkAccess",
            # "--disable-background-networking",
        ]
        
        
        if headless:
            chrome_args.insert(1, "--headless")


        for arg in chrome_args:
            options.add_argument(arg)

        # Configuración de preferencias (tus preferencias existentes)
        options.add_experimental_option("prefs", {
            "download.default_directory": self._download_dir,
            # ... (tus otras preferencias)

            # "profile.default_content_setting_values.media_stream_mic": 2,
            # "profile.default_content_setting_values.media_stream_camera": 2,
            # "profile.default_content_setting_values.geolocation": 2,
            # "profile.default_content_setting_values.notifications": 2,
            # "profile.default_content_setting_values.midi_sysex": 2,
            # "profile.default_content_setting_values.usb": 2,
            # "profile.default_content_setting_values.serial": 2,
            # "profile.default_content_setting_values.hid": 2,
        })

        # chromedriver_path = os.path.join(base_path, "webScraping SeleniumPY", "chromedriver-win64", "chromedriver.exe")
        
        # --- AQUÍ VA LA CONFIGURACIÓN DEL SERVICE CON EL MARCADOR ---

        service = Service(
            ChromeDriverManager().install(),

            #executable_path=chromedriver_path,
            service_args=[
                f'--marked={self._unique_marker}'  # Solo el marcador único
            ]
        )
        # -----------------------------------------------------------

        try:
            self._driver = webdriver.Chrome(service=service, options=options)
            # Configuraciones adicionales del driver...
            return self._driver
        except Exception as e:
            self._cleanup_chrome_processes()
            raise RuntimeError(f"No se pudo crear el WebDriver: {str(e)}")

    def close_driver(self):
        """Cierra el driver de forma segura"""
        if self._driver:
            try:
                self._driver.quit()
            except Exception as e:
                print(f"Error al hacer quit(): {e}")
            finally:
                self._driver = None

        # Limpieza profunda
        self._cleanup_chrome_processes()



    #--------
    def _force_kill_all_chrome_instances(self):
        # Diálogo de confirmación con botones Sí/No
        response = ctypes.windll.user32.MessageBoxW(
            0,
            "⚠️ SE CERRARÁN TODAS LAS INSTANCIAS DE CHROME ⚠️\n\n¿Está seguro de continuar?",
            "CONFIRMACIÓN REQUERIDA",
            0x34  # Icono de advertencia + Botones Sí/No (0x4) + Diálogo modal (0x1000)
        )
        
        # Códigos de respuesta: 6=Yes, 7=No
        if response == 6:
            if os.name == 'nt':
                subprocess.run("taskkill /IM chrome.exe /IM chromedriver.exe /F /T", 
                            shell=True, 
                            stdout=subprocess.DEVNULL, 
                            stderr=subprocess.DEVNULL)
            else:
                subprocess.run("pkill -f chrome", shell=True)
            print("✅ Todos los procesos de Chrome finalizados.")
        else:
            print("❌ Operación cancelada por el usuario.")
    #--------


    def __enter__(self):
        """Para uso con with statement"""
        return self.create_driver()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Garantiza la limpieza al salir del contexto"""
        self.close_driver()
        return False

    def get_driver(self):
        return self._driver

    def get_download_dir(self):
        return self._download_dir
    

    def _is_important_process(self, proc):
        """Determina si un proceso es importante y no debe ser eliminado"""
        try:
            # Excluir procesos del sistema o de otros programas importantes
            cmdline = ' '.join(proc.info['cmdline']).lower() if proc.info['cmdline'] else ''
            
            exclusion_patterns = [
                'system32', 'windowsapps', 'pythonlauncher', 
                'ide', 'pycharm', 'vscode', 'spyder'
            ]
            
            return any(pattern in cmdline for pattern in exclusion_patterns)
        except:
            return False
    
    
    def eliminar_procesos_python(self):
        """Elimina procesos Python residuales de forma segura y silenciosa"""
        current_pid = os.getpid()
        
        try:
            # Método 1: Comandos del sistema (rápido pero menos preciso)
            if os.name == 'nt':  # Windows
                creation_flags = subprocess.CREATE_NO_WINDOW | subprocess.HIGH_PRIORITY_CLASS
                
                subprocess.run(
                    f'taskkill /FI "PID ne {current_pid}" /IM python.exe /F /T',
                    shell=True,
                    creationflags=creation_flags,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
                
                subprocess.run(
                    f'taskkill /FI "PID ne {current_pid}" /IM pythonw.exe /F /T',
                    shell=True,
                    creationflags=creation_flags,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
            else:  # Linux/Mac
                subprocess.run(
                    f'pkill -f "python.*" -P {current_pid}',
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL,
                    timeout=5
                )
            
            time.sleep(0.5)  # Pequeña pausa
            
            # Método 2: Psutil (más preciso para procesos resistentes)
            for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    name = proc.info['name'].lower() if proc.info['name'] else ''
                    if 'python' in name and proc.pid != current_pid:
                        # Verificar si es un proceso hijo o relacionado
                        if not self._is_important_process(proc):
                            proc.kill()
                            time.sleep(0.05)  # Pequeña pausa entre kills
                except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                    continue
                    
        except Exception as e:
            # Silenciar errores para no afectar la interfaz
            pass

    
