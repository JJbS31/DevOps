import pygame
import random
import os
import sys
import time

# Inicializar Pygame
pygame.init()

# Dimensiones de la pantalla
WIDTH, HEIGHT = 1000, 800
WIN = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Memorama de Rizzelrs")

# Colores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 120, 215)
GREEN = (0, 200, 0)
RED = (255, 0, 0)
CARD_BACK_COLOR = (70, 130, 180)  # Azul acero

# Fuentes
FONT = pygame.font.SysFont('comicsans', 40)
TITLE_FONT = pygame.font.SysFont('comicsans', 60)
SMALL_FONT = pygame.font.SysFont('comicsans', 25)

# Configuración de las cartas
CARD_WIDTH = 120
CARD_HEIGHT = 120
CARD_MARGIN = 20  # Espacio entre cartas
GRID_WIDTH = 4    # Número de cartas horizontalmente
GRID_HEIGHT = 4   # Número de cartas verticalmente

# Calculamos el espacio total que ocuparán las cartas
TOTAL_CARD_WIDTH = GRID_WIDTH * CARD_WIDTH + (GRID_WIDTH - 1) * CARD_MARGIN
TOTAL_CARD_HEIGHT = GRID_HEIGHT * CARD_HEIGHT + (GRID_HEIGHT - 1) * CARD_MARGIN

# Calculamos las coordenadas iniciales para centrar las cartas
START_X = (WIDTH - TOTAL_CARD_WIDTH) // 2
START_Y = (HEIGHT - TOTAL_CARD_HEIGHT) // 2 + 30  # +30 para dejar espacio para la información superior

# Cargar imágenes
def load_images():
    images = []
    try:
        for i in range(1, 9):
            image = pygame.image.load(os.path.join('images', f'{i}.png'))
            # Optimizar tamaño para mejorar rendimiento
            images.append(pygame.transform.scale(image, (CARD_WIDTH, CARD_HEIGHT)))
        return images * 2  # Duplicar para crear pares
    except pygame.error as e:
        print(f"No se pudieron cargar las imágenes: {e}")
        print("Asegúrate de tener una carpeta 'images' con imágenes numeradas del 1 al 8.")
        pygame.quit()
        sys.exit()

# Estados del juego
MENU = 0
PLAYING = 1
GAME_OVER = 2

class Game:
    def __init__(self):
        self.state = MENU
        self.reset_game()
        
    def reset_game(self):
        self.images = load_images()
        random.shuffle(self.images)
        
        # Crear cartas
        self.cards = []
        for i in range(GRID_HEIGHT):
            row = []
            for j in range(GRID_WIDTH):
                x = START_X + j * (CARD_WIDTH + CARD_MARGIN)
                y = START_Y + i * (CARD_HEIGHT + CARD_MARGIN)
                row.append({
                    'image': self.images.pop(), 
                    'revealed': False, 
                    'matched': False,
                    'rect': pygame.Rect(x, y, CARD_WIDTH, CARD_HEIGHT),
                    'flip_progress': 0,  # Para animación de volteo
                    'flipping': False
                })
            self.cards.append(row)
            
        self.first_card = None
        self.second_card = None
        self.matches = 0
        self.attempts = 0
        self.start_time = None
        self.end_time = None
        self.can_click = True  # Para evitar clicks durante animaciones
        
    def start_game(self):
        self.state = PLAYING
        self.start_time = time.time()
        
    def handle_menu_click(self, pos):
        # Botón de inicio
        start_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2, 200, 50)
        if start_button.collidepoint(pos):
            self.start_game()
    
    def handle_game_click(self, pos):
        if not self.can_click:
            return
            
        for i in range(GRID_HEIGHT):
            for j in range(GRID_WIDTH):
                card = self.cards[i][j]
                if card['rect'].collidepoint(pos) and not card['revealed'] and not card['matched']:
                    # Asegurarse de que no estamos intentando seleccionar una tercera carta
                    if self.first_card is not None and self.second_card is not None:
                        return
                        
                    self.flip_card(card)
                    
                    if self.first_card is None:
                        self.first_card = card
                    elif self.second_card is None and card != self.first_card:
                        self.second_card = card
                        self.attempts += 1
                        self.can_click = False  # Deshabilitar clicks durante la comparación
                        pygame.time.set_timer(pygame.USEREVENT, 1000)  # Timer para comparar cartas
                    return  # Solo voltear una carta por click
    
    def handle_game_over_click(self, pos):
        # Botón de reinicio
        restart_button = pygame.Rect(WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50)
        if restart_button.collidepoint(pos):
            self.reset_game()
            self.state = MENU
            
    def flip_card(self, card):
        card['revealed'] = True
        card['flipping'] = True
            
    def check_match(self):
        if self.first_card['image'] == self.second_card['image']:
            self.first_card['matched'] = True
            self.second_card['matched'] = True
            self.matches += 1
                
            # Verificar si el juego terminó
            if self.matches == 8:
                self.end_time = time.time()
                self.state = GAME_OVER
            
            # Resetear las cartas seleccionadas después de un match
            self.first_card = None
            self.second_card = None
        else:
            # Programar el volteo de regreso de las cartas que no coinciden
            pygame.time.set_timer(pygame.USEREVENT + 1, 1000)
            
        self.can_click = True  # Permitir clicks después de la comparación
                
    def handle_card_flip_back(self):
        # Verificar que ambas cartas existen antes de intentar manipularlas
        if self.first_card and self.second_card:
            self.first_card['revealed'] = False
            self.first_card['flipping'] = True
            self.second_card['revealed'] = False
            self.second_card['flipping'] = True
            self.first_card = None
            self.second_card = None
        else:
            # Si por alguna razón llegamos aquí sin cartas seleccionadas, asegurémonos de que todo esté limpio
            self.first_card = None
            self.second_card = None
        
    def update_animations(self):
        for row in self.cards:
            for card in row:
                if card['flipping']:
                    if card['revealed']:
                        card['flip_progress'] += 10
                        if card['flip_progress'] >= 100:
                            card['flip_progress'] = 100
                            card['flipping'] = False
                    else:
                        card['flip_progress'] -= 10
                        if card['flip_progress'] <= 0:
                            card['flip_progress'] = 0
                            card['flipping'] = False
                            
    def draw_menu(self):
        WIN.fill(BLUE)
        
        # Título
        title = TITLE_FONT.render("MEMORAMA", 1, WHITE)
        WIN.blit(title, (WIDTH//2 - title.get_width()//2, 100))
        
        # Instrucciones
        instructions = SMALL_FONT.render("Encuentra todos los pares de cartas", 1, WHITE)
        WIN.blit(instructions, (WIDTH//2 - instructions.get_width()//2, 200))
        
        # Botón de inicio
        pygame.draw.rect(WIN, GREEN, (WIDTH//2 - 100, HEIGHT//2, 200, 50))
        start_text = FONT.render("INICIAR", 1, WHITE)
        WIN.blit(start_text, (WIDTH//2 - start_text.get_width()//2, HEIGHT//2 + 5))
        
    def draw_card(self, card):
        x, y = card['rect'].x, card['rect'].y
        width, height = card['rect'].width, card['rect'].height
        
        if card['matched']:
            # Cartas emparejadas tienen un borde verde
            pygame.draw.rect(WIN, GREEN, (x-3, y-3, width+6, height+6))
            WIN.blit(card['image'], (x, y))
        elif card['revealed']:
            # Cartas volteadas muestran la imagen
            if card['flip_progress'] < 50:
                # Primera mitad de la animación (encogimiento horizontal)
                scaled_width = int(width * (1 - card['flip_progress']/50))
                pygame.draw.rect(WIN, CARD_BACK_COLOR, (x + (width - scaled_width)//2, y, scaled_width, height))
            else:
                # Segunda mitad de la animación (crecimiento horizontal con imagen)
                scaled_width = int(width * ((card['flip_progress'] - 50)/50))
                scaled_image = pygame.transform.scale(card['image'], (scaled_width, height))
                WIN.blit(scaled_image, (x + (width - scaled_width)//2, y))
        else:
            # Cartas ocultas muestran el dorso
            if card['flip_progress'] > 50:
                # Primera mitad de la animación de vuelta (encogimiento horizontal)
                scaled_width = int(width * (1 - (card['flip_progress'] - 50)/50))
                scaled_image = pygame.transform.scale(card['image'], (scaled_width, height))
                WIN.blit(scaled_image, (x + (width - scaled_width)//2, y))
            else:
                # Segunda mitad de la animación o estado normal
                pygame.draw.rect(WIN, CARD_BACK_COLOR, card['rect'])
                # Agregar decoración al dorso de la carta
                pygame.draw.rect(WIN, BLACK, card['rect'], 2)
                pygame.draw.rect(WIN, WHITE, (x+10, y+10, width-20, height-20), 2)
    
    def draw_game(self):
        WIN.fill(WHITE)
        
        # Dibujar tablero
        for row in self.cards:
            for card in row:
                self.draw_card(card)
                
        # Información del juego
        attempts_text = FONT.render(f'Intentos: {self.attempts}', 1, BLACK)
        WIN.blit(attempts_text, (10, 10))
        
        matches_text = FONT.render(f'Pares: {self.matches}/8', 1, BLACK)
        WIN.blit(matches_text, (WIDTH - matches_text.get_width() - 10, 10))
        
        # Mostrar tiempo transcurrido
        if self.start_time:
            elapsed = int(time.time() - self.start_time)
            minutes = elapsed // 60
            seconds = elapsed % 60
            time_text = SMALL_FONT.render(f'Tiempo: {minutes:02d}:{seconds:02d}', 1, BLACK)
            WIN.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 10))
    
    def draw_game_over(self):
        self.draw_game()  # Dibujar el tablero en el fondo
        
        # Panel semi-transparente
        s = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        s.fill((0, 0, 0, 128))
        WIN.blit(s, (0, 0))
        
        # Mensaje de victoria
        win_text = TITLE_FONT.render("¡VICTORIA!", 1, WHITE)
        WIN.blit(win_text, (WIDTH//2 - win_text.get_width()//2, 100))
        
        # Estadísticas
        elapsed = int(self.end_time - self.start_time)
        minutes = elapsed // 60
        seconds = elapsed % 60
        
        time_text = FONT.render(f'Tiempo: {minutes:02d}:{seconds:02d}', 1, WHITE)
        WIN.blit(time_text, (WIDTH//2 - time_text.get_width()//2, 200))
        
        attempts_text = FONT.render(f'Intentos: {self.attempts}', 1, WHITE)
        WIN.blit(attempts_text, (WIDTH//2 - attempts_text.get_width()//2, 250))
        
        # Botón de reinicio
        pygame.draw.rect(WIN, GREEN, (WIDTH//2 - 100, HEIGHT//2 + 50, 200, 50))
        restart_text = FONT.render("REINICIAR", 1, WHITE)
        WIN.blit(restart_text, (WIDTH//2 - restart_text.get_width()//2, HEIGHT//2 + 55))
    
    def draw(self):
        if self.state == MENU:
            self.draw_menu()
        elif self.state == PLAYING:
            self.draw_game()
        elif self.state == GAME_OVER:
            self.draw_game_over()
        
        pygame.display.update()

def main():
    game = Game()
    clock = pygame.time.Clock()
    run = True
    
    while run:
        clock.tick(60)  # FPS
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if game.state == MENU:
                    game.handle_menu_click(pygame.mouse.get_pos())
                elif game.state == PLAYING:
                    game.handle_game_click(pygame.mouse.get_pos())
                elif game.state == GAME_OVER:
                    game.handle_game_over_click(pygame.mouse.get_pos())
            elif event.type == pygame.USEREVENT:
                # Timer para comparar cartas
                if game.first_card is not None and game.second_card is not None:
                    game.check_match()
                pygame.time.set_timer(pygame.USEREVENT, 0)  # Detener el timer
            elif event.type == pygame.USEREVENT + 1:
                # Timer para voltear cartas que no coinciden
                game.handle_card_flip_back()
                pygame.time.set_timer(pygame.USEREVENT + 1, 0)  # Detener el timer
        
        # Actualizar animaciones
        game.update_animations()
        
        # Dibujar
        game.draw()
        
    pygame.quit()

if __name__ == "__main__":
    main()