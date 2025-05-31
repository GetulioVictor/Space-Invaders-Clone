import pygame
import sys

# Inicializa o Pygame
pygame.init()

# Configurações da janela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
FPS = 60

# Cores
WHITE = (255, 255, 255)

# Cria a janela
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

# Carrega imagem de fundo
background = pygame.image.load('assets/images/black.png').convert()

# Relógio para controlar o FPS
clock = pygame.time.Clock()

# Loop principal
running = True
while running:
    clock.tick(FPS)

    # Eventos
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # Desenho
    screen.blit(background, (0, 0))
    
    # Atualiza a tela
    pygame.display.flip()

# Sai do Pygame
pygame.quit()
sys.exit()
