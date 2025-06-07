# player.py

class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.Surface((50, 30))  # Placeholder
        self.image.fill((0, 0, 255))
        self.rect = self.image.get_rect(center=(400, 550))
        self.speed = 5
        self.health = 3
        self.upgrades = []

    def update(self, keys):
        if keys[pygame.K_LEFT]:
            self.rect.x -= self.speed
        if keys[pygame.K_RIGHT]:
            self.rect.x += self.speed
        if keys[pygame.K_UP]:
            self.rect.y -= self.speed
        if keys[pygame.K_DOWN]:
            self.rect.y += self.speed

    def shoot(self):
        # Criar lógica de tiro
        pass
