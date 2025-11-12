import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simulación de Gravedad")

# Colores
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)

# Parámetros del círculo
x = WIDTH // 2
y = 100
radius = 30
velocity_y = 0
gravity = 0.5
energy_loss = 0.8  # Pérdida de energía del 20% por rebote
floor = HEIGHT - 50

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Aplicar gravedad
    velocity_y += gravity
    
    # Actualizar posición
    y += velocity_y
    
    # Rebotar en el suelo
    if y + radius > floor:
        y = floor - radius
        velocity_y = -velocity_y * energy_loss  # Invertir dirección y perder energía
        
        # Si la velocidad es muy pequeña, detener el movimiento
        if abs(velocity_y) < 0.5:
            velocity_y = 0
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar suelo
    pygame.draw.rect(screen, (100, 100, 100), (0, floor, WIDTH, HEIGHT - floor))
    
    # Dibujar círculo
    pygame.draw.circle(screen, GREEN, (int(x), int(y)), radius)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()