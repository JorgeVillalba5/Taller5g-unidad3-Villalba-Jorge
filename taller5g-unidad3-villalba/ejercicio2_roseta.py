# ejercicio2_roseta.py
# Taller de Programación de 5.ª Generación I - Tarea práctica Unidad III
# Ejercicio 2: Composición dinámica con el algoritmo de Bresenham
# Alumno: Jorge Ariel Villalba Martínez
#
# Genera rosetas geométricas conectando puntos equiespaciados de una
# circunferencia imaginaria (que no se dibuja) con líneas de Bresenham.
# Salidas: roseta_12.png, roseta_24.png, roseta_36.png (+ roseta.png)
#
# Extensiones voluntarias incluidas:
#   - roseta_saltos_5.png : solo conecta puntos no adyacentes (saltos de 5)
#   - roseta_24_azul.png  : fondo de color y líneas en colores complementarios
#   - roseta_animacion.gif: 20 rosetas con N creciente de 5 a 24

import math
import colorsys
from PIL import Image


# ---------------------------------------------------------------------------
# 1. ALGORITMO DE BRESENHAM (material, sección 2.3)
# ---------------------------------------------------------------------------
def bresenham(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Bresenham generalizado, aritmetica entera."""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy
    x, y = x0, y0
    while True:
        if 0 <= x < ancho and 0 <= y < alto:
            pixels[x, y] = color
        if x == x1 and y == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x += sx
        if e2 < dx:
            err += dx
            y += sy


# ---------------------------------------------------------------------------
# 2. DISTRIBUCIÓN DE PUNTOS SOBRE LA CIRCUNFERENCIA
# ---------------------------------------------------------------------------
def generar_puntos_circulo(cx, cy, radio, n):
    """Devuelve n puntos equiespaciados sobre la circunferencia (cx, cy, radio).
    El punto i está en el ángulo 2*pi*i/n (coordenadas polares -> cartesianas).
    """
    puntos = []
    for i in range(n):
        angulo = 2 * math.pi * i / n
        x = cx + int(round(radio * math.cos(angulo)))
        y = cy + int(round(radio * math.sin(angulo)))
        puntos.append((x, y))
    return puntos


# ---------------------------------------------------------------------------
# 3. GRADIENTE DE COLOR
# ---------------------------------------------------------------------------
def color_linea(i, j, n, hue_ini=0.0, hue_rango=1.0):
    """Calcula el color de la línea que une los puntos i y j (i < j).

    - TONO (hue): depende del ángulo del punto medio de la cuerda. Ese ángulo
      es proporcional a (i + j), así que las líneas que apuntan hacia la misma
      zona de la roseta comparten color y el círculo cromático se recorre una
      sola vez alrededor de la figura.
    - BRILLO (value): depende de la distancia de la cuerda al centro. Las
      cuerdas lejanas al centro (cortas) son más brillantes y las que pasan
      cerca del centro (diámetros) son más oscuras.
    """
    angulo_norm = (i + j) / (2 * n)                 # 0..1 (ángulo del punto medio)
    d = j - i                                       # separación entre puntos
    dist_norm = abs(math.cos(math.pi * d / n))      # 1 = cuerda corta, 0 = diámetro
    hue = (hue_ini + hue_rango * angulo_norm) % 1.0
    brillo = 0.65 + 0.35 * dist_norm
    r, g, b = colorsys.hsv_to_rgb(hue, 1.0, brillo)
    return (int(r * 255), int(g * 255), int(b * 255))


# ---------------------------------------------------------------------------
# 4. DIBUJO DE LA ROSETA
# ---------------------------------------------------------------------------
def dibujar_roseta(pixels, puntos, ancho, alto, hue_ini=0.0, hue_rango=1.0):
    """Conecta TODOS los pares de puntos con Bresenham (n*(n-1)/2 líneas).
    hue_ini y hue_rango son opcionales: permiten cambiar la paleta sin
    alterar la forma de llamar a la función.
    """
    n = len(puntos)
    for i in range(n):
        for j in range(i + 1, n):                   # cada par una sola vez
            color = color_linea(i, j, n, hue_ini, hue_rango)
            bresenham(pixels, puntos[i][0], puntos[i][1],
                      puntos[j][0], puntos[j][1], color, ancho, alto)


def dibujar_roseta_saltos(pixels, puntos, salto, ancho, alto):
    """EXTENSIÓN: solo conecta puntos cuya separación circular es múltiplo de
    'salto' (por ejemplo 5, 10, 15...). Nunca conecta puntos adyacentes."""
    n = len(puntos)
    for i in range(n):
        for j in range(i + 1, n):
            separacion = min(j - i, n - (j - i))    # distancia sobre el círculo
            if separacion % salto == 0:
                color = color_linea(i, j, n)
                bresenham(pixels, puntos[i][0], puntos[i][1],
                          puntos[j][0], puntos[j][1], color, ancho, alto)


def crear_imagen(lado, fondo):
    """Crea el lienzo cuadrado y devuelve (imagen, pixels)."""
    img = Image.new("RGB", (lado, lado), fondo)
    return img, img.load()


# ---------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    LADO = 700
    CENTRO = LADO // 2
    RADIO = 300
    FONDO = (0, 0, 0)                               # fondo negro

    # --- Requisito: tres variantes con distinto N -------------------------
    for n in [12, 24, 36]:
        img, pixels = crear_imagen(LADO, FONDO)
        puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, n)
        dibujar_roseta(pixels, puntos, LADO, LADO)
        img.save(f"roseta_{n}.png")
        print(f"roseta_{n}.png  ({n * (n - 1) // 2} líneas)")
        if n == 24:
            img.save("roseta.png")                  # nombre pedido en el requisito 4

    # --- Extensión 1: roseta con saltos de 5 (solo puntos no adyacentes) --
    img, pixels = crear_imagen(LADO, FONDO)
    puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, 30)
    dibujar_roseta_saltos(pixels, puntos, 5, LADO, LADO)
    img.save("roseta_saltos_5.png")
    print("roseta_saltos_5.png")

    # --- Extensión 2: fondo azul + líneas cálidas (complementarios) -------
    # Tonos 0.0-0.17 = rojo -> amarillo, complementarios del azul de fondo.
    img, pixels = crear_imagen(LADO, (10, 20, 70))
    puntos = generar_puntos_circulo(CENTRO, CENTRO, RADIO, 24)
    dibujar_roseta(pixels, puntos, LADO, LADO, hue_ini=0.0, hue_rango=0.17)
    img.save("roseta_24_azul.png")
    print("roseta_24_azul.png")

    # --- Extensión 3: GIF con 20 rosetas, N de 5 a 24 ---------------------
    LADO_GIF, RADIO_GIF = 500, 215
    cuadros = []
    for n in range(5, 25):                          # 5, 6, ..., 24 -> 20 cuadros
        img, pixels = crear_imagen(LADO_GIF, FONDO)
        puntos = generar_puntos_circulo(LADO_GIF // 2, LADO_GIF // 2,
                                        RADIO_GIF, n)
        dibujar_roseta(pixels, puntos, LADO_GIF, LADO_GIF)
        cuadros.append(img)
    cuadros[0].save("roseta_animacion.gif", save_all=True,
                    append_images=cuadros[1:], duration=350, loop=0)
    print(f"roseta_animacion.gif ({len(cuadros)} cuadros)")
