# background.py
import pygame
import random

# Carrega o sprite da estrela (ou nave, planeta, etc.)
star_img = pygame.image.load("assets/star.png")

# Lista de estrelas com posições iniciais aleatórias
stars = [{'x': random.randint(0, 800), 'y': random.randint(0, 600)} for _ in range(30)]

def update_stars():
    for star in stars:
        star['y'] += 1
        if star['y'] > 600:
            star['y'] = 0
            star['x'] = random.randint(0, 800)

def draw_stars(screen):
    for star in stars:
        screen.blit(star_img, (star['x'], star['y']))
