import pygame
import sys

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Colisión con Cambio de Color")

# Colores
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Jugador (rectángulo)
jugador = pygame.Rect(100, 100, 50, 50)
color_jugador = BLUE
velocidad = 5

# Objetivo (círculo)
objetivo_pos = [400, 300]
objetivo_radio = 30

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Movimiento del jugador
    teclas = pygame.key.get_pressed()
    if teclas[pygame.K_LEFT]:
        jugador.x -= velocidad
    if teclas[pygame.K_RIGHT]:
        jugador.x += velocidad
    if teclas[pygame.K_UP]:
        jugador.y -= velocidad
    if teclas[pygame.K_DOWN]:
        jugador.y += velocidad
    
    # Limitar al área de la pantalla
    jugador.x = max(0, min(WIDTH - jugador.width, jugador.x))
    jugador.y = max(0, min(HEIGHT - jugador.height, jugador.y))
    
    # Detectar colisión
    distancia_x = abs(jugador.centerx - objetivo_pos[0])
    distancia_y = abs(jugador.centery - objetivo_pos[1])
    
    if (distancia_x <= jugador.width // 2 + objetivo_radio and 
        distancia_y <= jugador.height // 2 + objetivo_radio):
        color_jugador = GREEN  # Cambiar color al colisionar
    else:
        color_jugador = BLUE   # Color normal
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar jugador
    pygame.draw.rect(screen, color_jugador, jugador)
    
    # Dibujar objetivo
    pygame.draw.circle(screen, RED, objetivo_pos, objetivo_radio)
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()