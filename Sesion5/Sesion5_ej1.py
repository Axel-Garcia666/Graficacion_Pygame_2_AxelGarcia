import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Ajuste de Tamaño Dinámico")

# Colores
WHITE = (255, 255, 255)

# Cargar imagen
def cargar_imagen(ruta):
    try:
        imagen = pygame.image.load(ruta)
        return imagen
    except pygame.error as e:
        print(f"No se pudo cargar la imagen: {ruta}")
        print(e)
        sys.exit()

# Ruta de la imagen (reemplaza con tu propia imagen)
ruta_imagen = "imagen.png"  # Cambia por la ruta de tu imagen

# Si la imagen no existe, creamos una superficie de ejemplo
if not os.path.exists(ruta_imagen):
    print("Creando imagen de ejemplo...")
    imagen_original = pygame.Surface((100, 100))
    imagen_original.fill((255, 0, 0))
    pygame.draw.circle(imagen_original, (0, 255, 0), (50, 50), 40)
    pygame.draw.rect(imagen_original, (0, 0, 255), (30, 30, 40, 40))
else:
    imagen_original = cargar_imagen(ruta_imagen)

# Parámetros de la imagen
escala = 1.0
escala_min = 0.1
escala_max = 3.0
paso_escala = 0.1

# Posición central
pos_x = WIDTH // 2
pos_y = HEIGHT // 2

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            # Aumentar tamaño con +
            if event.key == pygame.K_PLUS or event.key == pygame.K_KP_PLUS:
                escala = min(escala + paso_escala, escala_max)
            # Disminuir tamaño con -
            elif event.key == pygame.K_MINUS or event.key == pygame.K_KP_MINUS:
                escala = max(escala - paso_escala, escala_min)
    
    # Calcular nuevo tamaño manteniendo proporciones
    ancho_original, alto_original = imagen_original.get_size()
    nuevo_ancho = int(ancho_original * escala)
    nuevo_alto = int(alto_original * escala)
    
    # Escalar imagen manteniendo proporciones
    imagen_escalada = pygame.transform.scale(imagen_original, (nuevo_ancho, nuevo_alto))
    
    # Calcular posición para centrar
    rect_imagen = imagen_escalada.get_rect(center=(pos_x, pos_y))
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar imagen escalada
    screen.blit(imagen_escalada, rect_imagen)
    
    # Mostrar información de escala
    font = pygame.font.Font(None, 36)
    texto = font.render(f"Escala: {escala:.1f}x (Usa + y - para cambiar)", True, (0, 0, 0))
    screen.blit(texto, (10, 10))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()