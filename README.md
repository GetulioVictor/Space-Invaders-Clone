# Space Invaders Clone

Um clone customizado do jogo Space Invaders

Feito por Getúlio Victor.

## Estrutura do Projeto

space-invaders-clone/
│
├── assets/
│   ├── images/          # Sprites do jogador, aliens, fundo etc.
│   └── sounds/          # Sons (.ogg): música, tiro, explosão
|   └── fonts/           # Fontes (.ttf)
│
├── src/
│   ├── main.py          # Loop principal e menu
│   ├── game.py          # Lógica do jogo
│   ├── player.py        # Classe do jogador
│   ├── alien.py         # Classe dos inimigos
│   ├── bullet.py        # Tiros do jogador e inimigos
│   ├── settings.py      # Configurações salvas (nome, volume, pontuação)
│   └── background.py    # Fundo animado (opcional, não usado atualmente)
│
└── requirements.txt     # Lista de dependências Python

## Instalação

```
cd space-invaders-clone

python -m venv venv
source venv/bin/activate # Linux/macOS
venv\Scripts\activate    # Windows

pip install -r requirements.txt # com o pipx também funciona

python3 src/main.py
```
