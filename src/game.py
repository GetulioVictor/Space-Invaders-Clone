import pygame
from player import Player
from alien import Alien
from bullet import Bullet
import settings
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.running = True

        # Grupos
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # Carregar imagens
        base_path = os.path.dirname(__file__)
        player_image = pygame.image.load(os.path.join(base_path, "../assets/images/player.png")).convert_alpha()
        alien_image = pygame.image.load(os.path.join(base_path, "../assets/images/alien.png")).convert_alpha()
        bullet_image = pygame.image.load(os.path.join(base_path, "../assets/images/bullet.png")).convert_alpha()

        # Carregar fundo star.png e redimensionar para a tela
        self.background_img = pygame.image.load(os.path.join(base_path, "../assets/images/star.png")).convert()
        self.background_img = pygame.transform.scale(self.background_img, (800, 600))

        # Criar jogador (passa grupo de balas para o player)
        self.player = Player(player_image, bullet_image, self.player_bullets)
        self.all_sprites.add(self.player)

        # Criar aliens
        for i in range(5):
            for j in range(3):
                alien = Alien(100 + i * 100, 50 + j * 70, alien_image)
                self.aliens.add(alien)
                self.all_sprites.add(alien)

        self.bullet_image = bullet_image  # Para tiros dos aliens

        # Zera a pontuação ao iniciar o jogo
        settings.settings["last_score"] = 0

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        # Ao sair do loop do jogo, retorna a pontuação final
        return settings.settings["last_score"]

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()

        self.player.update(keys)

    def update(self):
        # Atualiza aliens e tenta atirar
        for alien in self.aliens:
            alien.update()
            alien.try_to_shoot(self.alien_bullets, self.bullet_image)

        # Atualiza balas
        self.player_bullets.update()
        self.alien_bullets.update()

        # Colisão: bala do player atinge alien
        for bullet in self.player_bullets:
            hit = pygame.sprite.spritecollideany(bullet, self.aliens)
            if hit:
                hit.kill_alien()
                bullet.kill()
                settings.settings["last_score"] += 10

        # Colisão: bala do alien atinge player
        for bullet in self.alien_bullets:
            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage()
                bullet.kill()

        # Fim do jogo
        if self.player.health <= 0:
            print("Game Over!")
            self.running = False
        if not self.aliens:
            print("Todos os aliens foram derrotados!")
            self.running = False

    def draw(self):
        # Desenha o fundo antes de desenhar sprites
        self.screen.blit(self.background_img, (0, 0))

        self.all_sprites.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.alien_bullets.draw(self.screen)
        pygame.display.flip()
