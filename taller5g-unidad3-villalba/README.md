# taller5g-unidad3-villalba

**Materia:** Taller de Programación de 5.ª Generación I
**Docente:** Prof. Mgtr. Alberto F. Giménez Méndez
**Alumno:** Jorge Ariel Villalba Martínez (apellido: Villalba)
**Tarea:** Práctica Unidad III - Conversión por rastreo (DDA y Bresenham)
**Universidad Americana** - Asunción, Paraguay - 2026

## Contenido

| Archivo | Descripción |
|---|---|
| `ejercicio1_casa.py` | Ejercicio 1: casa estilizada de 600x500 px con el algoritmo **DDA**. |
| `ejercicio2_roseta.py` | Ejercicio 2: rosetas geométricas de 700x700 px con el algoritmo de **Bresenham**. |
| `casa.png` | Imagen generada por el Ejercicio 1. |
| `roseta_12.png`, `roseta_24.png`, `roseta_36.png` | Imágenes generadas por el Ejercicio 2 (`roseta.png` es una copia de la de N=24). |
| `roseta_saltos_5.png`, `roseta_24_azul.png`, `roseta_animacion.gif` | Extensiones voluntarias del Ejercicio 2. |

## Cómo ejecutar

Requisitos: Python 3.8 o superior y la biblioteca Pillow.

```bash
pip install pillow
python ejercicio1_casa.py     # genera casa.png
python ejercicio2_roseta.py   # genera las rosetas y el GIF
```

Las imágenes se guardan en la carpeta desde la que se ejecuta el script.

## Extensiones voluntarias implementadas

- **Ejercicio 1:** árboles (tronco rectangular + copa triangular), nubes (líneas horizontales cortas), humo de chimenea y gradientes de color (cielo y pasto).
- **Ejercicio 2:** roseta que conecta solo puntos no adyacentes (saltos de 5), roseta con fondo de color y líneas complementarias, y GIF animado con 20 rosetas (N de 5 a 24).
