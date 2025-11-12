import pygame
import sys
import math
import os

# Inicializar Pygame
pygame.init()

# Configuración de la pantalla
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Nave Espacial Controlable")

# Colores
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 100, 255)
RED = (255, 50, 50)
YELLOW = (255, 255, 0)

# Clase para la nave espacial
class Nave:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.velocidad = 0
        self.velocidad_max = 5
        self.aceleracion = 0.2
        self.friccion = 0.95
        self.angulo = 0
        
        # Crear imagen de la nave
        self.imagen_original = self.crear_nave_imagen()
        self.imagen = self.imagen_original
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
    
    def crear_nave_imagen(self):
        """Crear una imagen de nave espacial si no existe una"""
        # Intentar cargar imagen externa
        ruta_imagen = "nave.png"
        if os.path.exists(ruta_imagen):
            try:
                imagen = pygame.image.load(ruta_imagen).convert_alpha()
                # Escalar a tamaño adecuado
                imagen = pygame.transform.scale(imagen, (60, 40))
                return imagen
            except pygame.error as e:
                print(f"Error cargando imagen: {e}")
                print("Creando nave de ejemplo...")
        
        # Crear nave de ejemplo
        superficie = pygame.Surface((60, 40), pygame.SRCALPHA)
        
        # Cuerpo principal de la nave (triángulo)
        puntos = [
            (0, 20),      # Punta izquierda
            (50, 0),      # Esquina superior derecha
            (50, 40),     # Esquina inferior derecha
        ]
        pygame.draw.polygon(superficie, BLUE, puntos)
        
        # Detalles de la nave
        pygame.draw.polygon(superficie, (0, 70, 200), [(50, 10), (60, 20), (50, 30)])
        
        # Ventana de la cabina
        pygame.draw.circle(superficie, YELLOW, (35, 20), 8)
        
        # Propulsores
        pygame.draw.rect(superficie, RED, (15, 15, 10, 10))
        
        return superficie
    
    def rotar_hacia_punto(self, punto_x, punto_y):
        """Rotar la nave hacia un punto (generalmente la posición del ratón)"""
        dx = punto_x - self.x
        dy = punto_y - self.y
        self.angulo = math.degrees(math.atan2(-dy, dx)) - 90
        
        # Rotar imagen
        self.imagen = pygame.transform.rotate(self.imagen_original, self.angulo)
        self.rect = self.imagen.get_rect(center=(self.x, self.y))
    
    def acelerar(self):
        """Acelerar la nave en la dirección actual"""
        if self.velocidad < self.velocidad_max:
            self.velocidad += self.aceleracion
    
    def actualizar(self):
        """Actualizar posición de la nave"""
        # Aplicar fricción
        self.velocidad *= self.friccion
        
        # Calcular movimiento basado en el ángulo
        if self.velocidad > 0.1:
            angulo_rad = math.radians(self.angulo + 90)
            self.x += math.cos(angulo_rad) * self.velocidad
            self.y -= math.sin(angulo_rad) * self.velocidad
            
            # Limitar a los bordes de la pantalla
            self.x = max(30, min(WIDTH - 30, self.x))
            self.y = max(30, min(HEIGHT - 30, self.y))
            
            # Actualizar rectángulo
            self.rect.center = (self.x, self.y)
    
    def dibujar(self, superficie):
        """Dibujar la nave en la superficie"""
        superficie.blit(self.imagen, self.rect)
        
        # Dibujar propulsor cuando se está acelerando
        if self.velocidad > 0.5:
            self.dibujar_propulsor(superficie)
    
    def dibujar_propulsor(self, superficie):
        """Dibujar efecto de propulsor"""
        angulo_rad = math.radians(self.angulo + 90)
        # Posición del propulsor (parte trasera de la nave)
        propulsor_x = self.x - math.cos(angulo_rad) * 25
        propulsor_y = self.y + math.sin(angulo_rad) * 25
        
        # Dibujar llamas del propulsor
        for i in range(3):
            longitud = 10 + i * 5
            ancho = 5 - i
            offset_x = -math.sin(angulo_rad) * (i * 3 - 3)
            offset_y = -math.cos(angulo_rad) * (i * 3 - 3)
            
            start_pos = (propulsor_x + offset_x, propulsor_y + offset_y)
            end_pos = (
                propulsor_x - math.cos(angulo_rad) * longitud + offset_x,
                propulsor_y + math.sin(angulo_rad) * longitud + offset_y
            )
            
            color = (255, 200 - i * 50, 0)
            pygame.draw.line(superficie, color, start_pos, end_pos, ancho)

# Crear nave
nave = Nave(WIDTH // 2, HEIGHT // 2)

# Fuente para texto
font = pygame.font.Font(None, 36)

# Reloj para controlar FPS
clock = pygame.time.Clock()

# Bucle principal
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    
    # Obtener estado del teclado y ratón
    teclas = pygame.key.get_pressed()
    pos_raton = pygame.mouse.get_pos()
    
    # Rotar nave hacia el ratón
    nave.rotar_hacia_punto(pos_raton[0], pos_raton[1])
    
    # Acelerar con ESPACIO o W
    if teclas[pygame.K_SPACE] or teclas[pygame.K_w]:
        nave.acelerar()
    
    # Actualizar nave
    nave.actualizar()
    
    # Dibujar
    screen.fill(BLACK)
    
    # Dibujar estrellas de fondo
    for i in range(50):
        x = (i * 123) % WIDTH
        y = (i * 321) % HEIGHT
        tamaño = (i % 3) + 1
        pygame.draw.circle(screen, WHITE, (x, y), tamaño)
    
    # Dibujar nave
    nave.dibujar(screen)
    
    # Dibujar información de controles
    controles_texto = font.render("Controles: RATÓN - Apuntar | ESPACIO/W - Acelerar", True, WHITE)
    screen.blit(controles_texto, (10, 10))
    
    velocidad_texto = font.render(f"Velocidad: {nave.velocidad:.1f}", True, WHITE)
    screen.blit(velocidad_texto, (10, 50))
    
    # Actualizar pantalla
    pygame.display.flip()
    
    # Controlar FPS
    clock.tick(60)

pygame.quit()
sys.exit()