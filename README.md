### README.md
# Coin Collector Game

A modular Python/Pygame casual game where the player collects coins to earn points, navigates obstacles (bombs) which reduce health, and aims to achieve the highest session score. Includes:

- **Character Selection Lobby**: Browse through available skins using left/right arrows, then start or exit.
- **Gameplay**: Move the character with WASD keys, collect coins (+1 point), avoid bombs (-1 health). Health is visualized and game ends when health reaches zero.
- **High Score Tracking**: Displays session high and persists the all-time high score to `high_score.txt`.
- **Modular Codebase**: Separated into `settings.py`, `character.py`, `game_elements.py`, `hud.py`, `collisions.py`, `lobby.py`, `level.py`, and `main.py`.

### How to Run
Copy and run in your terminal: 

pip install pygame pyinstaller
python main.py

### Build Executable
Copy and run in your terminal: 

pyinstaller --name CoinGame --onefile --windowed --add-data "src;src" main.py
./dist/CoinGame.exe

