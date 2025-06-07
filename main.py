import pygame
import sys
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

def draw_menu():
    """Desenha o menu principal."""
    screen.fill((0, 0, 0))  # Fundo preto
    title_text = font.render("SPACE INVADERS", True, (255, 255, 255))
    screen.blit(title_text, (SCREEN_WIDTH // 2 - title_text.get_width() // 2, 50))

    for idx, option in enumerate(menu_options):
        color = (255, 255, 255)
        if idx == selected_option:
            color = (255, 0, 0)  # Vermelho se selecionado
        option_text = small_font.render(option, True, color)
        screen.blit(option_text, (SCREEN_WIDTH // 2 - option_text.get_width() // 2, 150 + idx * 50))

    pygame.display.flip()

def config_menu():
    """Menu de configurações com input de nome e ajuste de volume."""
    in_config = True
    input_mode = False
    input_text = ""

    while in_config:
        screen.fill((30, 30, 30))
        
        config_texts = [
            f"Nome do Jogador: {settings.settings['player_name']}",
            f"Pontuação Última Partida: {settings.settings['last_score']}",
            f"Volume: {settings.settings['volume']:.1f}",
            "Pressione N para mudar nome",
            "Seta Esquerda/Direita para mudar volume",
            "ESC para voltar"
        ]

        for idx, text in enumerate(config_texts):
            config_render = small_font.render(text, True, (255, 255, 255))
            screen.blit(config_render, (50, 50 + idx * 40))

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
                        if len(input_text) < 15:  # Limite de caracteres
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
