Instalar python y pip 
generar el enviroment en la carpeta Autom chromer
posicionado en la carpeta "Autom chromer" usar el siguiente comando
Para generar el env: "python -m venv env"

Usar el comando "pip install -r '.\webScraping SeleniumPY\requirements2.txt'", el cual instala las correspondientes dependencias necesarias para utilizar el programa

al ejecutar, ejecutar desde ".\webScraping SeleniumPY\python\test\PhotoPy\interfaz.py"


Detalles tecnicos a tener en cuenta:

Respecto al programa, tener en cuenta que en la clase "driver_manager" se encuentran las direcciones por defecto, en este caso entramos en base al "usuario/Desktop" o "usuario/OneDrive"

serian estas lineas:
paths_to_check = [ #Desktop\Autom chromer
            os.path.join(os.path.expanduser("~"), "Desktop", "Git", "python", "Autom chromer"),
            os.path.join(os.path.expanduser("~"), "OneDrive", "Desktop", "Git", "python", "Autom chromer"),
            os.path.dirname(os.path.abspath(__file__))
        ]

y en el .env completar con las variables:
"FFMPEG_PATH="
"POPPLER_PATH="

estas son librerias que se requieren en caso de buscar sacar fotos a PDFs con "POPPLER" y "FFMPEG" para convertir archivos EJ .wave a .mp3
Dependiendo de para que se utilice el proceso, puede llegar a ser util:

en mi caso las tengo misma carpeta
y reemplazar el usuario "(usuarioNahu)"

FFMPEG_PATH=C:/Users/(usuarioNahu)/Desktop/Git/python/Autom chromer/webScraping SeleniumPY/ffmpeg/ffmpeg-version-7.1.1/ffmpeg-7.0.2-essentials_build/bin

POPPLER_PATH=C:/Users/(usuarioNahu)/Desktop/Git/python/Autom chromer/webScraping SeleniumPY/poppler-24.08.0/Library/bin
