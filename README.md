# Dino Run

A simple and engaging recreation of the classic Google Chrome dinosaur game. Jump over cacti and avoid obstacles in this endless runner game!


## Getting Started

### Prerequisites

- Python 3.6 or higher
- Pygame 1.9.6 or higher

### Installation

1. **Clone the Repository:**

   ```bash
   git clone https://github.com/jaylann/DinoGame.git
   cd dino-run
   ```

2. **Install Required Packages:**

   Install the necessary packages using the `requirements.txt` file:

   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the game using the following command:

```bash
python dino_run.py
```

## Game Features

- **Jumping:** Spacebar
- **Scoring:** Increases over time
- **Speed:** Gradually increases
- **Ending:** Game over on collision


## Customization

You can easily customize various aspects of the game by modifying certain variables.

### Changing Background Color

In the `World` class, you can change the background color by modifying the `background_color` variable:

```python
self.background_color = (247, 247, 247) # Change the RGB values
```

### Adjusting Cactus Size

In the `Cactus` class, you can adjust the scale factor of the cactus by modifying the `SCALE_FACTOR` variable:

```python
self.SCALE_FACTOR = 5 # Change the value to adjust the size
```

### Modifying Game Speed

In the `World` class, you can adjust the initial speed of the game by changing the `speed` variable:

```python
self.speed = 6 # Change the value to set a different speed
```

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

<p align="center">
  Made with ❤️ by <a href="https://lanfermann.dev">Justin Lanfermann</a>
</p>

