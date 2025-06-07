# bullet.py

class Bullet(pygame.sprite.Sprite):
    def __init__(self, x, y, direction):
        super().__init__()
        self.image = pygame.Surface((5, 10))  # Placeholder
        self.image.fill((255, 255, 0))
        self.rect = self.image.get_rect(center=(x, y))
        self.speed = 7 * direction  # direção: -1 para cima, 1 para baixo

    def update(self):
        self.rect.y += self.speed
        if self.rect.bottom < 0 or self.rect.top > 600:
            self.kill()
