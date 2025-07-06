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

        # Grupos de sprites
        self.all_sprites = pygame.sprite.Group()
        self.aliens = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.alien_bullets = pygame.sprite.Group()

        # Caminho base
        base_path = os.path.dirname(__file__)

        # Carregar imagens
        player_image = pygame.image.load(os.path.join(base_path, "../assets/images/player.png")).convert_alpha()
        alien_image = pygame.image.load(os.path.join(base_path, "../assets/images/alien.png")).convert_alpha()
        bullet_image = pygame.image.load(os.path.join(base_path, "../assets/images/bullet.png")).convert_alpha()
        self.background_img = pygame.image.load(os.path.join(base_path, "../assets/images/star.png")).convert()
        self.background_img = pygame.transform.scale(self.background_img, (800, 600))

        # Carregar sons (.ogg)
        self.shoot_sound = pygame.mixer.Sound(os.path.join(base_path, "../assets/sounds/shoot.ogg"))
        self.explosion_sound = pygame.mixer.Sound(os.path.join(base_path, "../assets/sounds/explosion.ogg"))
        pygame.mixer.music.load(os.path.join(base_path, "../assets/sounds/music.ogg"))
        pygame.mixer.music.set_volume(settings.settings["volume"])
        pygame.mixer.music.play(-1)  # Loop infinito da música de fundo

        # Criar jogador
        self.player = Player(player_image, bullet_image, self.player_bullets)
        self.all_sprites.add(self.player)

        # Criar aliens
        for i in range(5):
            for j in range(3):
                alien = Alien(100 + i * 100, 50 + j * 70, alien_image)
                self.aliens.add(alien)
                self.all_sprites.add(alien)

        self.bullet_image = bullet_image
        settings.settings["last_score"] = 0  # Resetar pontuação

    def run(self):
        while self.running:
            self.clock.tick(60)
            self.handle_events()
            self.update()
            self.draw()

        self.show_game_over()
        pygame.mixer.music.stop()
        return settings.settings["last_score"]

    def handle_events(self):
        keys = pygame.key.get_pressed()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.player.shoot()
                    self.shoot_sound.play()
        self.player.update(keys)

    def update(self):
        for alien in self.aliens:
            alien.update()
            alien.try_to_shoot(self.alien_bullets, self.bullet_image)

        self.player_bullets.update()
        self.alien_bullets.update()

        # Colisão: bala do player atinge alien
        for bullet in self.player_bullets:
            hit = pygame.sprite.spritecollideany(bullet, self.aliens)
            if hit:
                hit.kill_alien()
                bullet.kill()
                self.explosion_sound.play()
                settings.settings["last_score"] += 10

        # Colisão: bala do alien atinge player
        for bullet in self.alien_bullets:
            if bullet.rect.colliderect(self.player.rect):
                self.player.take_damage()
                bullet.kill()

        # Colisão: player colide com alien
        collided_alien = pygame.sprite.spritecollideany(self.player, self.aliens)
        if collided_alien:
            self.player.take_damage()
            # Opcional: eliminar o alien após colisão
            # collided_alien.kill_alien()

        # Fim do jogo
        if self.player.health <= 0:
            self.running = False
        if not self.aliens:
            self.running = False

    def draw(self):
        self.screen.blit(self.background_img, (0, 0))
        self.all_sprites.draw(self.screen)
        self.player_bullets.draw(self.screen)
        self.alien_bullets.draw(self.screen)
        pygame.display.flip()

    def show_game_over(self):
        font = pygame.font.Font(None, 72)
        small_font = pygame.font.Font(None, 48)

        game_over_text = font.render("GAME OVER", True, (255, 0, 0))
        score_text = small_font.render(f"Pontuação: {settings.settings['last_score']}", True, (255, 255, 255))
        continue_text = small_font.render("Voltando ao menu...", True, (180, 180, 180))

        self.screen.blit(self.background_img, (0, 0))
        self.screen.blit(game_over_text, (400 - game_over_text.get_width() // 2, 200))
        self.screen.blit(score_text, (400 - score_text.get_width() // 2, 300))
        self.screen.blit(continue_text, (400 - continue_text.get_width() // 2, 400))

        pygame.display.flip()
        pygame.time.delay(3000)
