# alien.py

class Alien(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((40, 30))  # Placeholder
        self.image.fill((0, 255, 0))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.speed = 2
        self.alive = True

    def update(self):
        self.rect.x += self.speed
        if self.rect.right >= 800 or self.rect.left <= 0:
            self.speed *= -1
            self.rect.y += 10  # Desce ao bater na borda

    def shoot(self):
        # Criar lógica de tiro dos aliens
        pass
