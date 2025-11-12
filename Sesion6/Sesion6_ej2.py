import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Recolección de Objetos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Jugador
jugador = pygame.Rect(100, 100, 40, 40)
velocidad = 5

# Objetos a recolectar
objetos = []
objeto_radio = 15
max_objetos = 5
contador_objetos = 0

# Fuente para el contador
font = pygame.font.Font(None, 36)

def crear_objeto():
    """Crear un nuevo objeto en posición aleatoria"""
    x = random.randint(objeto_radio, WIDTH - objeto_radio)
    y = random.randint(objeto_radio, HEIGHT - objeto_radio)
    return [x, y]

# Crear objetos iniciales
for _ in range(max_objetos):
    objetos.append(crear_objeto())

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
    
    # Detectar colisiones con objetos
    objetos_a_eliminar = []
    
    for i, obj in enumerate(objetos):
        distancia_x = abs(jugador.centerx - obj[0])
        distancia_y = abs(jugador.centery - obj[1])
        
        if (distancia_x <= jugador.width // 2 + objeto_radio and 
            distancia_y <= jugador.height // 2 + objeto_radio):
            objetos_a_eliminar.append(i)
            contador_objetos += 1
    
    # Eliminar objetos recolectados y crear nuevos
    for i in sorted(objetos_a_eliminar, reverse=True):
        del objetos[i]
        objetos.append(crear_objeto())
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, jugador)
    
    # Dibujar objetos
    for obj in objetos:
        pygame.draw.circle(screen, GREEN, obj, objeto_radio)
    
    # Mostrar contador
    texto = font.render(f"Objetos recolectados: {contador_objetos}", True, RED)
    screen.blit(texto, (10, 10))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()