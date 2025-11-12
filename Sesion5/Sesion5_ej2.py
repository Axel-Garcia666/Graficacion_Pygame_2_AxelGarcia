import pygame
import sys
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Sprite Animado")

# Colores
WHITE = (255, 255, 255)

# Clase para el sprite animado
class SpriteAnimado:
    def __init__(self, hoja_sprites, filas, columnas, duracion_frame=100):
        self.hoja_sprites = hoja_sprites
        self.filas = filas
        self.columnas = columnas
        self.duracion_frame = duracion_frame
        self.tiempo_anterior = pygame.time.get_ticks()
        
        # Calcular dimensiones de cada frame
        self.ancho_frame = hoja_sprites.get_width() // columnas
        self.alto_frame = hoja_sprites.get_height() // filas
        
        # Crear lista de frames
        self.frames = []
        self.crear_frames()
        
        # Estado de animación
        self.frame_actual = 0
        self.total_frames = len(self.frames)
    
    def crear_frames(self):
        for fila in range(self.filas):
            for columna in range(self.columnas):
                x = columna * self.ancho_frame
                y = fila * self.alto_frame
                frame = self.hoja_sprites.subsurface(pygame.Rect(x, y, self.ancho_frame, self.alto_frame))
                self.frames.append(frame)
    
    def actualizar(self):
        tiempo_actual = pygame.time.get_ticks()
        if tiempo_actual - self.tiempo_anterior > self.duracion_frame:
            self.frame_actual = (self.frame_actual + 1) % self.total_frames
            self.tiempo_anterior = tiempo_actual
    
    def dibujar(self, superficie, x, y):
        frame = self.frames[self.frame_actual]
        rect = frame.get_rect(center=(x, y))
        superficie.blit(frame, rect)

# Crear hoja de sprites de ejemplo si no existe
def crear_hoja_sprites_ejemplo():
    """Crea una hoja de sprites de ejemplo con un personaje caminando"""
    ancho_frame = 64
    alto_frame = 64
    columnas = 4
    filas = 1
    
    hoja = pygame.Surface((ancho_frame * columnas, alto_frame * filas), pygame.SRCALPHA)
    
    # Colores
    color_cuerpo = (70, 130, 180)  # Azul acero
    color_piernas = (30, 80, 130)  # Azul más oscuro
    color_cabeza = (240, 200, 160)  # Color piel
    
    # Crear 4 frames de animación de caminata
    for i in range(columnas):
        x_offset = i * ancho_frame
        
        # Cuerpo (siempre en el centro)
        pygame.draw.rect(hoja, color_cuerpo, (x_offset + 20, 20, 24, 30))
        
        # Cabeza
        pygame.draw.circle(hoja, color_cabeza, (x_offset + 32, 15), 10)
        
        # Piernas - diferentes posiciones para cada frame
        if i == 0:  # Frame 1: piernas juntas
            pygame.draw.rect(hoja, color_piernas, (x_offset + 25, 50, 6, 14))
            pygame.draw.rect(hoja, color_piernas, (x_offset + 33, 50, 6, 14))
        elif i == 1:  # Frame 2: pierna derecha adelante
            pygame.draw.rect(hoja, color_piernas, (x_offset + 25, 50, 6, 10))
            pygame.draw.rect(hoja, color_piernas, (x_offset + 33, 48, 6, 12))
        elif i == 2:  # Frame 3: piernas juntas (opuesto al frame 1)
            pygame.draw.rect(hoja, color_piernas, (x_offset + 25, 50, 6, 14))
            pygame.draw.rect(hoja, color_piernas, (x_offset + 33, 50, 6, 14))
        else:  # Frame 4: pierna izquierda adelante
            pygame.draw.rect(hoja, color_piernas, (x_offset + 25, 48, 6, 12))
            pygame.draw.rect(hoja, color_piernas, (x_offset + 33, 50, 6, 10))
    
    return hoja

# Cargar o crear hoja de sprites
ruta_hoja_sprites = "spritesheet.png"  # Puedes reemplazar con tu propia hoja de sprites

if os.path.exists(ruta_hoja_sprites):
    try:
        hoja_sprites = pygame.image.load(ruta_hoja_sprites).convert_alpha()
        print("Hoja de sprites cargada exitosamente")
    except pygame.error as e:
        print(f"Error cargando hoja de sprites: {e}")
        print("Creando hoja de sprites de ejemplo...")
        hoja_sprites = crear_hoja_sprites_ejemplo()
else:
    print("Creando hoja de sprites de ejemplo...")
    hoja_sprites = crear_hoja_sprites_ejemplo()

# Crear sprite animado
sprite = SpriteAnimado(hoja_sprites, filas=1, columnas=4, duracion_frame=100)

# Posición del sprite
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
    
    # Actualizar animación
    sprite.actualizar()
    
    # Limpiar pantalla
    screen.fill(WHITE)
    
    # Dibujar sprite
    sprite.dibujar(screen, pos_x, pos_y)
    
    # Mostrar información
    font = pygame.font.Font(None, 36)
    texto = font.render("Sprite Animado - Personaje Caminando", True, (0, 0, 0))
    screen.blit(texto, (10, 10))
    
    texto_frame = font.render(f"Frame: {sprite.frame_actual + 1}/{sprite.total_frames}", True, (0, 0, 0))
    screen.blit(texto_frame, (10, 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()