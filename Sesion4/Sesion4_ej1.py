import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Robote con Velocidad Variable")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)

# Posición y velocidad inicial del círculo
x = WIDTH // 2
y = HEIGHT // 2
radius = 30
speed_x = 5
acceleration = 0.1

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Actualizar posición
    x += speed_x
    
    # Rebotar en los bordes y acelerar
    if x + radius > WIDTH or x - radius < 0:
        speed_x = -speed_x * 1.1  # Invertir dirección y aumentar velocidad
        # Asegurar que no exceda límites
        if x + radius > WIDTH:
            x = WIDTH - radius
        else:
            x = radius
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar círculo
    pygame.draw.circle(screen, RED, (int(x), y), radius)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()