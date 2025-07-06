import pygame
import random
from bullet import Bullet

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y, image, speed=2):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = speed
        self.direction = 1  # 1 = vai p/ direita, -1 = vai p/ esquerda
        self.shoot_probability = 0.002  # chance de atirar a cada frame
        self.shoot_cooldown = 2000      # tempo mínimo entre tiros em ms (2s)
        self.last_shot_time = 0          # guarda o último tempo que atirou

    def update(self):
        # Movimento horizontal
        self.rect.x += self.speed * self.direction

        # Muda direção e desce se tocar na borda da tela
        if self.rect.right >= 800:
            self.direction = -1
            self.rect.y += 20
        elif self.rect.left <= 0:
            self.direction = 1
            self.rect.y += 20

    def try_to_shoot(self, bullets_group, bullet_image):
        current_time = pygame.time.get_ticks()
        if current_time - self.last_shot_time >= self.shoot_cooldown:
            if random.random() < self.shoot_probability:
                bullet = Bullet(self.rect.centerx, self.rect.bottom, 5, bullet_image, direction="down")
                bullets_group.add(bullet)
                self.last_shot_time = current_time  # atualiza o tempo do último tiro

    def kill_alien(self):
        self.kill()
