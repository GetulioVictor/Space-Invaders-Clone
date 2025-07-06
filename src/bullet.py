import pygame

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, speed, image, direction="up"):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = speed  # Deve ser positivo
        self.direction = direction  # "up" ou "down"

    def update(self):
        if self.direction == "up":
            self.rect.y -= self.speed  # Sobe na tela
        elif self.direction == "down":
            self.rect.y += self.speed  # Desce na tela

        # Remove a bala quando sair da tela
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()

    def check_collision(self, target_group):
        return pygame.sprite.spritecollideany(self, target_group)