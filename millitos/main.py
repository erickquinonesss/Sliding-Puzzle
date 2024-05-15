import pygame
from sprites import *
from ajustes import *
import random

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption(titulo)
        self.previous_choice = ""
        self.start_game = False
        self.first_move = False

    def crear_juego(self):
        grid = [[x + y * juego_size for x in range(1, juego_size + 1)] for y in range(juego_size)]
        grid[-1][-1] = 0
        return grid
    
    def moves(self):
        possible_moves = []
        for row, tiles in enumerate(self.tiles):
            for col, tile in enumerate(tiles):
                if tile.text == "empty":
                    if tile.right():
                        possible_moves.append("right")
                    if tile.left():
                        possible_moves.append("left")
                    if tile.up():
                        possible_moves.append("up")
                    if tile.down():
                        possible_moves.append("down")
                    break
            if len(possible_moves) > 0:
                break

        if self.previous_choice == "right":
            possible_moves.remove("left") if "left" in possible_moves else possible_moves
        elif self.previous_choice == "left":
            possible_moves.remove("right") if "right" in possible_moves else possible_moves
        elif self.previous_choice == "up":
            possible_moves.remove("down") if "down" in possible_moves else possible_moves
        elif self.previous_choice == "down":
            possible_moves.remove("up") if "up" in possible_moves else possible_moves

        choice = random.choice(possible_moves)
        self.previous_choice = choice
        if choice == "right":
            self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "left":
            self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], \
                                                                       self.tiles_grid[row][col]
        elif choice == "up":
            self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], \
                                                                       self.tiles_grid[row][col]
        elif choice == "down":
            self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], \
                                                                       self.tiles_grid[row][col]
    def dceldas(self):
        self.tiles = []
        for row, x in enumerate(self.tiles_grid):
            self.tiles.append([])
            for col, tile in enumerate(x):
                if tile != 0: 
                    image_path = f"imagenes/{tile}.jpg"  
                    self.tiles[row].append(Tile(self, col, row, image_path))
                else:
                    image_path = "imagenes/empty.jpg"  
                    self.tiles[row].append(Tile(self, col, row, image_path))
               

    def nuevo(self):
        self.all_sprites = pygame.sprite.Group()
        self.tiles_grid = self.crear_juego()
        self.tiles_grid_completed = self.crear_juego()
        self.start_game = False
        self.dceldas()

    def run(self):
        self.playing = True
        while self.playing:
            self.eventos()
            self.update()
            self.dibujar()

            if self.check_win():
                        self.display_win_message() 
                        self.start_game = False  # Detener el juego después de ganar

    def update(self):
        if self.start_game:
            if self.tiles_grid == self.tiles_grid_completed:
                self.start_game = False
        self.all_sprites.update()

    def cuadricula(self):
        for row in range(-1, juego_size * celda, celda):
            pygame.draw.line(self.screen, BLUE, (row, 0), (row, juego_size * celda))
        for col in range(-1, juego_size * celda, celda):
            pygame.draw.line(self.screen, BLUE, (0, col), (juego_size * celda, col))

    def dibujar(self):
        self.all_sprites.draw(self.screen)
        self.cuadricula()
        pygame.display.flip()

    def eventos(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                self.first_move=True
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for row, tiles in enumerate(self.tiles):
                    for col, tile in enumerate(tiles):
                        if tile.click(mouse_x, mouse_y):
                            if tile.right() and self.tiles_grid[row][col + 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col + 1] = self.tiles_grid[row][col + 1], self.tiles_grid[row][col]

                            if tile.left() and self.tiles_grid[row][col - 1] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row][col - 1] = self.tiles_grid[row][col - 1], self.tiles_grid[row][col]

                            if tile.up() and self.tiles_grid[row - 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row - 1][col] = self.tiles_grid[row - 1][col], self.tiles_grid[row][col]

                            if tile.down() and self.tiles_grid[row + 1][col] == 0:
                                self.tiles_grid[row][col], self.tiles_grid[row + 1][col] = self.tiles_grid[row + 1][col], self.tiles_grid[row][col]

                            self.dceldas()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r:
                    self.barajar()  

                    
    def barajar(self):
        all_tiles = [tile for row in self.tiles_grid for tile in row]
        random.shuffle(all_tiles)
        all_tiles.sort(key=lambda i: i == 0)
        self.tiles_grid = [all_tiles[i:i+juego_size] for i in range(0, len(all_tiles), juego_size)]     # divide las celdas barajadas en filas y columnas :p
        self.dceldas()

    def check_win(self):
        return self.tiles_grid == self.tiles_grid_completed and self.first_move == True
    
    def display_win_message(self):
        font = pygame.font.SysFont("Consolas", 36)
        text = font.render("¡Ganaste!", True, (255, 255, 255))
        text_rect = text.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        self.screen.blit(text, text_rect)
        pygame.display.flip()

game = Game()
while True:
    game.nuevo()
    game.run()