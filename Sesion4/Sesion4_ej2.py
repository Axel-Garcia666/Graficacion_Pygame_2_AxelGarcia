import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Animación de Pulsación")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)

# Parámetros del círculo
x = WIDTH // 2
y = HEIGHT // 2
radius = 20
min_radius = 20
max_radius = 50
growing = True
growth_speed = 0.5

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar radio
    if growing:
        radius += growth_speed
        if radius >= max_radius:
            growing = False
    else:
        radius -= growth_speed
        if radius <= min_radius:
            growing = True
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar círculo
    pygame.draw.circle(screen, BLUE, (x, y), int(radius))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()