# generar_escena.py — Genera y renderiza una escena POV-Ray desde Python
# Funciona en Windows, macOS y Linux
import subprocess
import platform
# 1. Definimos el contenido de la escena como una cadena de texto
escena = """
#include "colors.inc"
camera { location <0, 2, -5> look_at <0, 0, 0> }
light_source { <5, 10, -5> color White }
sphere {
<0, 0, 0>, 1
pigment { color Blue }
}
"""
# 2. Escribimos el contenido a un archivo .pov
with open("escena_python.pov", "w") as f:
    f.write(escena)
# 3. Detectamos el sistema operativo y armamos el comando apropiado
sistema = platform.system()
if sistema == "Windows":
# En Windows, POV-Ray se llama pvengine y necesita opciones especificas
    comando = ["pvengine", "escena_python.pov",
"/RENDER", "/EXIT", "+W600", "+H400"]
else:
# En macOS (Darwin) y Linux, se llama povray
    comando = ["povray", "escena_python.pov",
"+W600", "+H400"]
# 4. Invocamos a POV-Ray para renderizar
subprocess.run(comando, check=True)
print(f"Renderizado en {sistema}. Revise escena_python.png")