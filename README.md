# Tank Attack 3 (TATH)

Tank Attack 3 (TATH) is an engaging 2D arcade-style game built using Python and Pygame. The game features a dynamic battle between a player-controlled "Blue Dot" and multiple AI-controlled tanks. Players must navigate, shoot lasers, and utilize power boosts to defeat the tanks while avoiding incoming attacks.

## Features

- **Player-Controlled Blue Dot**:
  - Move up and down using arrow keys.
  - Shoot lasers with the spacebar.
  - Fire powerful fireballs after collecting 10 power boosts (press `F`).

- **AI-Controlled Tanks**:
  - Tanks shoot lasers towards the Blue Dot.
  - Tanks have individual health that decreases when hit by lasers or fireballs.

- **Power Boosts**:
  - Randomly spawn on the screen.
  - Collect power boosts by hitting them with lasers to charge fireball attacks.

- **Dynamic Gameplay**:
  - Health management for both the Blue Dot and tanks.
  - Infinite spawning of power boosts.
  - Game resets when the Blue Dot's health drops to zero or all tanks are defeated.

- **Visual Effects**:
  - Dashed lasers for both the Blue Dot and tanks.
  - Fireball animations for powerful attacks.

## Controls

- **Arrow Keys**: Move the Blue Dot up and down.
- **Spacebar**: Shoot lasers.
- **F Key**: Fire a fireball (requires 10 power boosts).

## How to Play

1. Start the game by running the `tath.py` file.
2. Use the arrow keys to move the Blue Dot and avoid incoming tank lasers.
3. Shoot lasers (spacebar) to destroy tanks and collect power boosts.
4. Once 10 power boosts are collected, press `F` to fire a powerful fireball.
5. Survive as long as possible and defeat all tanks to win the game.

## Requirements

- Python 3.x
- Pygame library

To install Pygame, run the following command:

```bash
pip install pygame
```

## File Structure

tath.py: Main game logic and implementation.
assets/: Contains game assets such as music files.

## How to Run

Ensure Python and Pygame are installed on your system.
Place the tath.py file and the assets folder in the same directory.
Run the game using the following command: python [tath.py]

## License

This project is under MIT license.

## Author

Praveen Rai & Krishang Rai