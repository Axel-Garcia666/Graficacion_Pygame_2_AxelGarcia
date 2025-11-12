import pygame
import sys
import random

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Evitar Obstáculos")

# Colores
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
BLACK = (0, 0, 0)

# Jugador
jugador = pygame.Rect(100, 100, 40, 40)
velocidad = 6

# Obstáculos
obstaculos = []
num_obstaculos = 5
obstaculo_radio = 20

# Fuente para el juego
font = pygame.font.Font(None, 48)

class Obstaculo:
    def __init__(self):
        self.radio = obstaculo_radio
        self.x = random.randint(self.radio, WIDTH - self.radio)
        self.y = random.randint(self.radio, HEIGHT - self.radio)
        self.velocidad_x = random.choice([-3, -2, 2, 3])
        self.color = RED
    
    def mover(self):
        self.x += self.velocidad_x
        
        # Rebotar en los bordes
        if self.x - self.radio <= 0 or self.x + self.radio >= WIDTH:
            self.velocidad_x = -self.velocidad_x
    
    def dibujar(self):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radio)

# Crear obstáculos iniciales
for _ in range(num_obstaculos):
    obstaculos.append(Obstaculo())

# Estado del juego
juego_activo = True

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not juego_activo:
                # Reiniciar juego
                juego_activo = True
                jugador.x = 100
                jugador.y = 100
                obstaculos = []
                for _ in range(num_obstaculos):
                    obstaculos.append(Obstaculo())
    
    if juego_activo:
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
        
        # Mover obstáculos
        for obstaculo in obstaculos:
            obstaculo.mover()
            
            # Detectar colisión
            distancia_x = abs(jugador.centerx - obstaculo.x)
            distancia_y = abs(jugador.centery - obstaculo.y)
            
            if (distancia_x <= jugador.width // 2 + obstaculo.radio and 
                distancia_y <= jugador.height // 2 + obstaculo.radio):
                juego_activo = False
    
    # Dibujar
    screen.fill(WHITE)
    
    # Dibujar jugador
    pygame.draw.rect(screen, BLUE, jugador)
    
    # Dibujar obstáculos
    for obstaculo in obstaculos:
        obstaculo.dibujar()
    
    # Mostrar mensaje si el juego terminó
    if not juego_activo:
        texto_game_over = font.render("¡GAME OVER! Presiona R para reiniciar", True, BLACK)
        screen.blit(texto_game_over, (WIDTH // 2 - 250, HEIGHT // 2 - 24))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()