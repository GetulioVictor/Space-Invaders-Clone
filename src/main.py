import pygame
import os
import sys
import pygame.gfxdraw
import settings  # Arquivo separado que armazena configurações

pygame.init()

# Configurações iniciais
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Space Invaders")

font = pygame.font.SysFont(None, 48)
small_font = pygame.font.SysFont(None, 36)

clock = pygame.time.Clock()

# Opções do menu
menu_options = ["Iniciar Jogo", "Selecionar Fase", "Configurações", "Sair"]
selected_option = 0

# Carregar imagem de fundo e fonte personalizada
base_path = os.path.dirname(__file__)
background_path = os.path.join(base_path, "../assets/images/Blue_Nebula_01-1024x1024.png")
background_img = pygame.image.load(background_path).convert()

# Carregar imagem de fundo do menu de configurações
config_background_path = os.path.join(base_path, "../assets/images/Purple_Nebula_01-1024x1024.png")
config_background_img = pygame.image.load(config_background_path).convert()

# Carregar fonte
font_path = os.path.join(base_path, "../assets/fonts/OpenSans-Bold.ttf")
title_font = pygame.font.Font(font_path, 60)
menu_font = pygame.font.Font(font_path, 40)

# Carregar ícones
icon_user = pygame.image.load("../assets/images/CelestialObjects.png").convert_alpha()

def draw_menu():
    """Desenha o menu principal com imagem de fundo e nova fonte."""
    screen.blit(background_img, (0, 0))  # Desenha o fundo

    # Título do jogo
    title_text = title_font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    # Opções de menu
    for idx, option in enumerate(menu_options):
        color = (255, 255, 255)
        if idx == selected_option:
            color = (255, 0, 0)  # Vermelho se selecionado
        option_text = menu_font.render(option, True, color)
        screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 180 + idx * 60))

    pygame.display.flip()

def draw_rounded_rect(surface, rect, color, radius):
    """Desenha retângulo arredondado com antialiasing."""
    x, y, w, h = rect
    pygame.gfxdraw.aacircle(surface, x + radius, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + radius, radius, color)

    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + radius, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + radius, radius, color)

    pygame.gfxdraw.aacircle(surface, x + radius, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + radius, y + h - radius - 1, radius, color)

    pygame.gfxdraw.aacircle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)
    pygame.gfxdraw.filled_circle(surface, x + w - radius - 1, y + h - radius - 1, radius, color)

    pygame.draw.rect(surface, color, (x + radius, y, w - 2 * radius, h))
    pygame.draw.rect(surface, color, (x, y + radius, w, h - 2 * radius))


def draw_volume_bar(screen, x, y, width, height, volume):
    radius = 12

    # Sombra atrás
    shadow_color = (20, 20, 20, 180)
    shadow_surf = pygame.Surface((width + 6, height + 6), pygame.SRCALPHA)
    draw_rounded_rect(shadow_surf, (3, 3, width, height), shadow_color, radius)
    screen.blit(shadow_surf, (x - 3, y - 3))

    # Barra fundo
    bg_color = (50, 50, 50)
    draw_rounded_rect(screen, (x, y, width, height), bg_color, radius)

    # Barra preenchida
    fill_width = int(width * volume)
    if fill_width > 0:
        fill_color = (50, 200, 50)

        fill_surf = pygame.Surface((fill_width, height), pygame.SRCALPHA)

        if volume >= 1.0:
            # volume cheio: arredondar todos os lados
            draw_rounded_rect(fill_surf, (0, 0, fill_width, height), fill_color, radius)
        else:
            # volume parcial: só arredondar lado esquerdo
            # desenha círculos arredondados só do lado esquerdo
            r = radius
            pygame.gfxdraw.aacircle(fill_surf, r, r, r, fill_color)
            pygame.gfxdraw.filled_circle(fill_surf, r, r, r, fill_color)
            pygame.gfxdraw.aacircle(fill_surf, r, height - r - 1, r, fill_color)
            pygame.gfxdraw.filled_circle(fill_surf, r, height - r - 1, r, fill_color)

            # retângulo que cobre o resto do fill_width
            pygame.draw.rect(fill_surf, fill_color, (r, 0, fill_width - r, height))

        screen.blit(fill_surf, (x, y))

    # Borda branca semitransparente
    border_color = (255, 255, 255, 100)
    border_surf = pygame.Surface((width, height), pygame.SRCALPHA)
    draw_rounded_rect(border_surf, (0, 0, width, height), border_color, radius)
    screen.blit(border_surf, (x, y))


def config_menu():
    global config_background_img
    in_config = True
    input_mode = False
    input_text = ""

    while in_config:
        screen.blit(config_background_img, (0, 0))

        config_texts = [
            f"Nome do Jogador: {settings.settings['player_name']}",
            f"Última Pontuação: {settings.settings['last_score']}",
            f"Volume: {settings.settings['volume']:.1f}"
        ]

        helper_texts = [
            "Pressione N para mudar nome",
            "Use as setas para ajustar o volume",
            "ESC para voltar ao menu"
        ]

        for idx, text in enumerate(config_texts):
            config_render = small_font.render(text, True, (255, 255, 255))
            overlay = pygame.Surface((SCREEN_WIDTH - 100, 50), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 150))
            screen.blit(overlay, (40, 50 + idx * 60))
            screen.blit(config_render, (50, 50 + idx * 60))

        # Desenha a barra de volume logo abaixo do texto "Volume"
        volume = settings.settings['volume']
        bar_x = 50
        bar_y = 50 + 2 * 60 + 40  # posição vertical um pouco abaixo do 3º texto
        bar_width = 300
        bar_height = 25
        draw_volume_bar(screen, bar_x, bar_y, bar_width, bar_height, volume)

        for idx, text in enumerate(helper_texts[::-1]):
            helper_render = small_font.render(text, True, (200, 200, 200))
            screen.blit(helper_render, (50, SCREEN_HEIGHT - 30 - idx * 30))

        if input_mode:
            input_prompt = small_font.render("Digite o nome: " + input_text, True, (0, 255, 0))
            screen.blit(input_prompt, (50, 350))

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if input_mode:
                    if event.key == pygame.K_RETURN:
                        if input_text.strip() != "":
                            settings.set_player_name(input_text.strip())
                        input_mode = False
                        input_text = ""
                    elif event.key == pygame.K_BACKSPACE:
                        input_text = input_text[:-1]
                    else:
                        if len(input_text) < 15:
                            input_text += event.unicode
                else:
                    match event.key:
                        case pygame.K_ESCAPE:
                            in_config = False
                        case pygame.K_LEFT:
                            settings.change_volume(-0.1)
                        case pygame.K_RIGHT:
                            settings.change_volume(0.1)
                        case pygame.K_n:
                            input_mode = True


# Loop principal
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            match event.key:
                case pygame.K_UP:
                    selected_option = (selected_option - 1) % len(menu_options)
                case pygame.K_DOWN:
                    selected_option = (selected_option + 1) % len(menu_options)
                case pygame.K_RETURN:
                    match menu_options[selected_option]:
                        case "Iniciar Jogo":
                            print("Iniciando jogo... (implementar depois)")
                            # game = Game(screen)
                            # game.run()
                        case "Selecionar Fase":
                            print("Selecionar fase... (implementar depois)")
                        case "Configurações":
                            config_menu()
                        case "Sair":
                            running = False

    draw_menu()

pygame.quit()
sys.exit()
