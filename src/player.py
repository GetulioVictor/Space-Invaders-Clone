import pygame
from bullet import Bullet

class Player(pygame.sprite.Sprite):
    def __init__(self, player_image, bullet_image, bullets_group):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect(midbottom=(400, 580))  # Posição inicial
        self.speed = 5
        self.health = 3
        self.bullet_image = bullet_image
        self.bullets_group = bullets_group
        self.last_shot = 0
        self.shoot_cooldown = 500  # ms

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed
            
        # Limita movimento dentro da tela
        self.rect.clamp_ip(pygame.Rect(0, 0, 800, 600))

    def shoot(self):
        now = pygame.time.get_ticks()
        if now - self.last_shot >= self.shoot_cooldown:
            # Cria a bala indo para cima (speed positiva e direção "up")
            bullet = Bullet(self.rect.centerx, self.rect.top, speed=7, image=self.bullet_image, direction="up")
            self.bullets_group.add(bullet)
            self.last_shot = now

    def take_damage(self):
        self.health -= 1
        if self.health <= 0:
            self.kill()