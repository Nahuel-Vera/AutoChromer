AutoChromer 🤖🧭

Automatización de procesos con Python + Selenium, orientada a scraping, procesamiento de PDFs y manejo de archivos multimedia.
El proyecto permite ejecutar flujos automatizados desde una interfaz gráfica, utilizando drivers configurables y soporte opcional para conversión de archivos.

🚀 Features
Automatización web con Selenium
Interfaz gráfica en Python
Soporte para procesamiento de PDFs
Conversión de archivos de audio (opcional)
Configuración flexible mediante variables de entorno

🛠️ Tech Stack
Python
Selenium
Tkinter
FFmpeg (opcional)
Poppler (opcional)

📦 Instalación
1️⃣ Requisitos
Python 3.x
pip

2️⃣ Crear entorno virtual
Ubicate en la raíz del proyecto Autom chromer:
python -m venv env

Activá el entorno virtual:
env\Scripts\activate

3️⃣ Instalar dependencias
pip install -r ".\webScraping SeleniumPY\requirements2.txt"

▶️ Uso
Ejecutar el programa desde:
.\webScraping SeleniumPY\python\test\PhotoPy\interfaz.py

⚙️ Configuración (.env)
Crear un archivo .env en la raíz del proyecto con las siguientes variables:
FFMPEG_PATH=
POPPLER_PATH=


Estas variables son opcionales y solo necesarias si se requiere:
Extraer imágenes desde PDFs (Poppler)
Convertir archivos de audio (FFmpeg)

📌 Ejemplo
FFMPEG_PATH=C:/Users/USUARIO/Desktop/Git/python/Autom chromer/webScraping SeleniumPY/ffmpeg/bin
POPPLER_PATH=C:/Users/USUARIO/Desktop/Git/python/Autom chromer/webScraping SeleniumPY/poppler/Library/bin

## 🧠 Detalles técnicos
En la clase `driver_manager` se definen las rutas por defecto donde el programa intenta localizar el proyecto.
Por defecto, se buscan las siguientes ubicaciones:

- `Desktop/Git/python/Autom chromer`
- `OneDrive/Desktop/Git/python/Autom chromer`
- Ruta actual desde donde se ejecuta el script

```python
paths_to_check = [
    os.path.join(os.path.expanduser("~"), "Desktop", "Git", "python", "Autom chromer"),
    os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Git", "python", "Autom chromer"),
    os.path.dirname(os.path.abspath(__file__))
]
```

Desktop
OneDrive/Desktop
Ruta actual del script
Esto permite flexibilidad según el entorno del usuario.

📁 Notas
El entorno virtual (env) no se sube al repositorio
El archivo .env es local
Las rutas pueden adaptarse según el sistema

📌 Estado del proyecto
🟡 En desarrollo / uso personal
Mejoras futuras incluyen:
Mayor modularización
Logging avanzado
Manejo de errores centralizado

🧑‍💻 Autor
Nahuel Vera
Python Automation & Web Scraping
