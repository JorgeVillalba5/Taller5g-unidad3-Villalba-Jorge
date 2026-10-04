# ejercicio1_casa.py
# Taller de Programación de 5.ª Generación I - Tarea práctica Unidad III
# Ejercicio 1: Composición geométrica con el algoritmo DDA
# Alumno: Jorge Ariel Villalba Martínez
#
# Dibuja una casa estilizada (vista frontal) sobre un lienzo de 600 x 500 px
# usando EXCLUSIVAMENTE la función dda() como primitiva de trazado.
# Salida: casa.png
#
# Extensiones voluntarias incluidas: árboles, nubes, humo de chimenea y
# gradientes de color (cielo, pasto).

import math
from PIL import Image


# ---------------------------------------------------------------------------
# 1. ALGORITMO DDA (material de lectura, sección 2.2)
# ---------------------------------------------------------------------------
def dda(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Traza una linea usando el algoritmo DDA."""
    dx = x1 - x0
    dy = y1 - y0
    pasos = max(abs(dx), abs(dy))
    if pasos == 0:                 # los dos puntos coinciden
        return
    x_inc = dx / pasos
    y_inc = dy / pasos
    x, y = x0, y0
    for _ in range(int(pasos) + 1):
        px, py = round(x), round(y)
        if 0 <= px < ancho and 0 <= py < alto:
            pixels[px, py] = color
        x += x_inc
        y += y_inc


# ---------------------------------------------------------------------------
# 2. FUNCIÓN AUXILIAR: línea con grosor
#    Repite dda() desplazada algunos píxeles para que los trazos se vean
#    más gruesos. Sigue usando dda() sin modificarla.
# ---------------------------------------------------------------------------
def linea_gruesa(pixels, x0, y0, x1, y1, color, ancho, alto, grosor=2):
    """Llama a dda() varias veces con pequeños desplazamientos."""
    for d in range(grosor):
        dda(pixels, x0 + d, y0, x1 + d, y1, color, ancho, alto)
        dda(pixels, x0, y0 + d, x1, y1 + d, color, ancho, alto)


# ---------------------------------------------------------------------------
# 3. ELEMENTOS GRÁFICOS BÁSICOS (una función por elemento)
# ---------------------------------------------------------------------------
def dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Rectángulo = 4 líneas DDA (arriba, derecha, abajo, izquierda)."""
    linea_gruesa(pixels, x0, y0, x1, y0, color, ancho, alto)  # lado superior
    linea_gruesa(pixels, x1, y0, x1, y1, color, ancho, alto)  # lado derecho
    linea_gruesa(pixels, x1, y1, x0, y1, color, ancho, alto)  # lado inferior
    linea_gruesa(pixels, x0, y1, x0, y0, color, ancho, alto)  # lado izquierdo


def dibujar_triangulo(pixels, p1, p2, p3, color, ancho, alto):
    """Triángulo = 3 líneas DDA que conectan los tres vértices."""
    linea_gruesa(pixels, p1[0], p1[1], p2[0], p2[1], color, ancho, alto)
    linea_gruesa(pixels, p2[0], p2[1], p3[0], p3[1], color, ancho, alto)
    linea_gruesa(pixels, p3[0], p3[1], p1[0], p1[1], color, ancho, alto)


def dibujar_cuerpo_casa(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Cuerpo de la casa: un rectángulo (4 líneas)."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)


def dibujar_techo(pixels, izq, cima, der, color, ancho, alto):
    """Techo: un triángulo (3 líneas)."""
    dibujar_triangulo(pixels, izq, cima, der, color, ancho, alto)


def dibujar_puerta(pixels, x0, y0, x1, y1, color, ancho, alto):
    """Puerta: un rectángulo (4 líneas) más una manija (un punto grueso)."""
    dibujar_rectangulo(pixels, x0, y0, x1, y1, color, ancho, alto)
    # Manija: un pequeño segmento cerca del borde derecho
    linea_gruesa(pixels, x1 - 12, (y0 + y1) // 2, x1 - 6, (y0 + y1) // 2,
                 color, ancho, alto, grosor=3)


def dibujar_ventana(pixels, x0, y0, lado, color, ancho, alto):
    """Ventana cuadrada: rectángulo de lado 'lado' (4 líneas)."""
    dibujar_rectangulo(pixels, x0, y0, x0 + lado, y0 + lado,
                       color, ancho, alto)


def dibujar_sol(pixels, cx, cy, radio, n_rayos, color, ancho, alto):
    """Sol: n_rayos líneas DDA que irradian desde (cx, cy).
    Los extremos se calculan con coordenadas polares:
        x = cx + radio * cos(angulo)      y = cy + radio * sin(angulo)
    """
    for i in range(n_rayos):
        angulo = 2 * math.pi * i / n_rayos      # reparte los rayos en 360°
        x_fin = int(cx + radio * math.cos(angulo))
        y_fin = int(cy + radio * math.sin(angulo))
        linea_gruesa(pixels, cx, cy, x_fin, y_fin, color, ancho, alto)


def dibujar_piso(pixels, y, color, ancho, alto):
    """Línea de piso que atraviesa toda la imagen horizontalmente."""
    linea_gruesa(pixels, 0, y, ancho - 1, y, color, ancho, alto, grosor=3)


# ---------------------------------------------------------------------------
# 4. EXTENSIONES VOLUNTARIAS
# ---------------------------------------------------------------------------
def dibujar_gradiente_vertical(pixels, y_ini, y_fin, color_ini, color_fin,
                               ancho, alto):
    """Gradiente: una línea horizontal DDA por fila, interpolando el color."""
    total = max(1, y_fin - y_ini)
    for y in range(y_ini, y_fin + 1):
        t = (y - y_ini) / total                       # 0.0 -> 1.0
        color = tuple(int(color_ini[k] + (color_fin[k] - color_ini[k]) * t)
                      for k in range(3))
        dda(pixels, 0, y, ancho - 1, y, color, ancho, alto)


def dibujar_arbol(pixels, x, y_base, color_tronco, color_copa, ancho, alto):
    """Árbol: tronco rectangular + copa triangular."""
    dibujar_rectangulo(pixels, x - 7, y_base - 40, x + 7, y_base,
                       color_tronco, ancho, alto)
    dibujar_triangulo(pixels, (x - 38, y_base - 40), (x, y_base - 115),
                      (x + 38, y_base - 40), color_copa, ancho, alto)


def dibujar_nube(pixels, cx, cy, semiancho, color, ancho, alto):
    """Nube: pila de líneas horizontales cortas de largo variable (elipse)."""
    semialto = semiancho // 3
    for dy in range(-semialto, semialto + 1):
        mitad = int(semiancho * math.sqrt(1 - (dy / semialto) ** 2))
        dda(pixels, cx - mitad, cy + dy, cx + mitad, cy + dy,
            color, ancho, alto)


def dibujar_chimenea(pixels, x0, x1, y_tope, y_base_izq, y_base_der,
                     color, ancho, alto):
    """Chimenea: 3 líneas (izquierda, arriba, derecha) que nacen del techo."""
    linea_gruesa(pixels, x0, y_base_izq, x0, y_tope, color, ancho, alto)
    linea_gruesa(pixels, x0, y_tope, x1, y_tope, color, ancho, alto)
    linea_gruesa(pixels, x1, y_tope, x1, y_base_der, color, ancho, alto)


def dibujar_humo(pixels, x, y, color, ancho, alto):
    """Humo: segmentos cortos que suben ondulando con una función seno."""
    for k in range(5):
        x_a = x + int(10 * math.sin(k * 0.9))
        x_b = x + int(10 * math.sin((k + 1) * 0.9))
        linea_gruesa(pixels, x_a, y - k * 12, x_b, y - (k + 1) * 12,
                     color, ancho, alto)


# ---------------------------------------------------------------------------
# 5. PROGRAMA PRINCIPAL
# ---------------------------------------------------------------------------
ancho, alto = 600, 500
imagen = Image.new("RGB", (ancho, alto), (200, 230, 255))   # frame buffer
pixels = imagen.load()

# Paleta de colores (todos distintos entre sí)
COLOR_CUERPO = (139, 69, 19)      # marrón
COLOR_TECHO = (200, 30, 30)       # rojo
COLOR_PUERTA = (30, 60, 160)      # azul
COLOR_VENTANA = (255, 140, 0)     # naranja
COLOR_SOL = (255, 200, 0)         # amarillo
COLOR_PISO = (50, 50, 50)         # gris oscuro
COLOR_TRONCO = (101, 67, 33)      # marrón oscuro
COLOR_COPA = (20, 130, 40)        # verde
COLOR_NUBE = (255, 255, 255)      # blanco
COLOR_HUMO = (110, 110, 110)      # gris
COLOR_CHIMENEA = (150, 40, 90)    # bordó

Y_PISO = 420

# Fondo: gradiente de cielo (arriba) y de pasto (abajo), con líneas DDA
dibujar_gradiente_vertical(pixels, 0, Y_PISO, (110, 170, 240), (215, 238, 255),
                           ancho, alto)
dibujar_gradiente_vertical(pixels, Y_PISO, alto - 1, (70, 180, 80),
                           (20, 100, 40), ancho, alto)

# Elementos del paisaje (se dibujan primero, quedan al fondo)
dibujar_sol(pixels, 520, 70, 50, 12, COLOR_SOL, ancho, alto)
dibujar_nube(pixels, 120, 80, 55, COLOR_NUBE, ancho, alto)
dibujar_nube(pixels, 405, 45, 40, COLOR_NUBE, ancho, alto)
dibujar_nube(pixels, 250, 120, 35, COLOR_NUBE, ancho, alto)
dibujar_arbol(pixels, 60, Y_PISO, COLOR_TRONCO, COLOR_COPA, ancho, alto)
dibujar_arbol(pixels, 530, Y_PISO, COLOR_TRONCO, COLOR_COPA, ancho, alto)

# Chimenea y humo (detrás del techo, a la derecha)
dibujar_chimenea(pixels, 340, 365, 165, 209, 228, COLOR_CHIMENEA, ancho, alto)
dibujar_humo(pixels, 352, 150, COLOR_HUMO, ancho, alto)

# La casa
dibujar_cuerpo_casa(pixels, 150, 270, 400, Y_PISO, COLOR_CUERPO, ancho, alto)
dibujar_techo(pixels, (130, 270), (275, 160), (420, 270), COLOR_TECHO,
              ancho, alto)
dibujar_puerta(pixels, 250, 340, 300, Y_PISO, COLOR_PUERTA, ancho, alto)
dibujar_ventana(pixels, 175, 300, 45, COLOR_VENTANA, ancho, alto)
dibujar_ventana(pixels, 330, 300, 45, COLOR_VENTANA, ancho, alto)

# Línea de piso que cruza toda la imagen
dibujar_piso(pixels, Y_PISO, COLOR_PISO, ancho, alto)

imagen.save("casa.png")
print("Imagen generada: casa.png")
