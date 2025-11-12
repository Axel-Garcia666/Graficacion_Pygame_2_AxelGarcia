import pygame
import sys
import random
import math

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Espacial - Recolecta y Evita")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 100, 255)
YELLOW = (255, 255, 0)

# Clase para la nave espacial
class Nave:
    def __init__(self):
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.ancho = 40
        self.alto = 30
        self.velocidad = 5
        self.angulo = 0
        self.vidas = 3
        self.puntos = 0
    
    def mover(self, teclas):
        if teclas[pygame.K_LEFT]:
            self.x -= self.velocidad
        if teclas[pygame.K_RIGHT]:
            self.x += self.velocidad
        if teclas[pygame.K_UP]:
            self.y -= self.velocidad
        if teclas[pygame.K_DOWN]:
            self.y += self.velocidad
        
        # Limitar a la pantalla
        self.x = max(self.ancho // 2, min(WIDTH - self.ancho // 2, self.x))
        self.y = max(self.alto // 2, min(HEIGHT - self.alto // 2, self.y))
    
    def dibujar(self):
        # Crear puntos para el triángulo de la nave
        puntos = [
            (self.x, self.y - self.alto // 2),  # Punta
            (self.x - self.ancho // 2, self.y + self.alto // 2),  # Esquina inferior izquierda
            (self.x + self.ancho // 2, self.y + self.alto // 2)   # Esquina inferior derecha
        ]
        pygame.draw.polygon(screen, BLUE, puntos)
        
        # Detalles de la nave
        pygame.draw.circle(screen, YELLOW, (self.x, self.y), 5)  # Cabina
    
    def get_rect(self):
        return pygame.Rect(self.x - self.ancho // 2, self.y - self.alto // 2, 
                          self.ancho, self.alto)

# Clase para los objetos a recolectar
class Punto:
    def __init__(self):
        self.radio = 10
        self.x = random.randint(self.radio, WIDTH - self.radio)
        self.y = random.randint(self.radio, HEIGHT - self.radio)
        self.color = GREEN
    
    def dibujar(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radio)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, 
                          self.radio * 2, self.radio * 2)

# Clase para los obstáculos
class Obstaculo:
    def __init__(self):
        self.radio = 15
        self.x = random.randint(self.radio, WIDTH - self.radio)
        self.y = random.randint(self.radio, HEIGHT - self.radio)
        self.velocidad_x = random.choice([-2, -1, 1, 2])
        self.velocidad_y = random.choice([-2, -1, 1, 2])
        self.color = RED
    
    def mover(self):
        self.x += self.velocidad_x
        self.y += self.velocidad_y
        
        # Rebotar en los bordes
        if self.x - self.radio <= 0 or self.x + self.radio >= WIDTH:
            self.velocidad_x = -self.velocidad_x
        if self.y - self.radio <= 0 or self.y + self.radio >= HEIGHT:
            self.velocidad_y = -self.velocidad_y
    
    def dibujar(self):
        pygame.draw.circle(screen, self.color, (self.x, self.y), self.radio)
    
    def get_rect(self):
        return pygame.Rect(self.x - self.radio, self.y - self.radio, 
                          self.radio * 2, self.radio * 2)

# Inicializar juego
nave = Nave()
puntos = [Punto() for _ in range(3)]
obstaculos = [Obstaculo() for _ in range(4)]

# Fuentes
font = pygame.font.Font(None, 36)
font_grande = pygame.font.Font(None, 72)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
juego_activo = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_r and not juego_activo:
                # Reiniciar juego
                juego_activo = True
                nave = Nave()
                puntos = [Punto() for _ in range(3)]
                obstaculos = [Obstaculo() for _ in range(4)]
    
    if juego_activo:
        # Obtener teclas presionadas
        teclas = pygame.key.get_pressed()
        
        # Mover nave
        nave.mover(teclas)
        
        # Mover obstáculos
        for obstaculo in obstaculos:
            obstaculo.mover()
        
        # Detectar colisión con puntos
        puntos_a_eliminar = []
        for i, punto in enumerate(puntos):
            if nave.get_rect().colliderect(punto.get_rect()):
                puntos_a_eliminar.append(i)
                nave.puntos += 10
        
        # Eliminar puntos recolectados y crear nuevos
        for i in sorted(puntos_a_eliminar, reverse=True):
            del puntos[i]
            puntos.append(Punto())
        
        # Detectar colisión con obstáculos
        for obstaculo in obstaculos:
            if nave.get_rect().colliderect(obstaculo.get_rect()):
                nave.vidas -= 1
                # Reposicionar obstáculo
                obstaculo.x = random.randint(obstaculo.radio, WIDTH - obstaculo.radio)
                obstaculo.y = random.randint(obstaculo.radio, HEIGHT - obstaculo.radio)
                
                if nave.vidas <= 0:
                    juego_activo = False
    
    # Dibujar
    screen.fill(BLACK)
    
    # Dibujar estrellas de fondo
    for i in range(100):
        x = (i * 79) % WIDTH
        y = (i * 53) % HEIGHT
        pygame.draw.circle(screen, WHITE, (x, y), 1)
    
    # Dibujar elementos del juego
    if juego_activo:
        nave.dibujar()
        
        for punto in puntos:
            punto.dibujar()
        
        for obstaculo in obstaculos:
            obstaculo.dibujar()
    
    # Mostrar información
    texto_puntos = font.render(f"Puntos: {nave.puntos}", True, WHITE)
    texto_vidas = font.render(f"Vidas: {nave.vidas}", True, WHITE)
    
    screen.blit(texto_puntos, (10, 10))
    screen.blit(texto_vidas, (10, 50))
    
    # Mostrar mensaje si el juego terminó
    if not juego_activo:
        texto_game_over = font_grande.render("GAME OVER", True, RED)
        texto_reiniciar = font.render("Presiona R para reiniciar", True, WHITE)
        
        screen.blit(texto_game_over, (WIDTH // 2 - 150, HEIGHT // 2 - 50))
        screen.blit(texto_reiniciar, (WIDTH // 2 - 140, HEIGHT // 2 + 20))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()