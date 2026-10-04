import math

ancho, alto = 3660, 3200
pixel_pitch_um = 7.5

ancho_mm = ancho * pixel_pitch_um / 1000
alto_mm = alto * pixel_pitch_um / 1000
diagonal_mm = math.sqrt(ancho_mm**2 + alto_mm**2)
diagonal_pulg = diagonal_mm / 25.4
ppi = math.sqrt(ancho**2 + alto**2) / diagonal_pulg

print(f"Diagonal física: {diagonal_pulg:.3f} pulgadas")
print(f"Densidad: {ppi:.0f} PPI")