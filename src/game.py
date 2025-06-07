# game.py

import pygame
from player import Player
from alien import Alien
from bullet import Bullet
import settings

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.bullets = pygame.sprite.Group()
        self.player = Player()
        self.all_sprites.add(self.player)
        self.running = True

        # Criar aliens
        for i in range(5):
            for j in range(3):
                alien = Alien(100 + i * 60, 50 + j * 50)
                self.aliens.add(alien)
                self.all_sprites.add(alien)

    def run(self):
        clock = pygame.time.Clock()
        while self.running:
            clock.tick(60)
            keys = pygame.key.get_pressed()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        bullet = Bullet(self.player.rect.centerx, self.player.rect.top, -1)
                        self.bullets.add(bullet)
                        self.all_sprites.add(bullet)

            # Atualiza
            self.all_sprites.update()
            self.player.update(keys)

            # Colisões
            for bullet in self.bullets:
                hit = pygame.sprite.spritecollideany(bullet, self.aliens)
                if hit:
                    hit.kill()
                    bullet.kill()
                    settings.settings["last_score"] += 10

            # Checa se todos morreram
            if not self.aliens:
                print("Todos aliens mortos!")
                self.running = False

            # Desenha
            self.screen.fill((0, 0, 0))
            self.all_sprites.draw(self.screen)
            pygame.display.flip()
