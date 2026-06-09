# 🏁 Python Checkers Game

A fully featured, interactive 8x8 Checkers board game built from scratch in Python using the `graphics.py` library for desktop visual rendering and `pygame` for responsive, ambient background audio management. 

This game comes packed with customizable setting presets including multiple high-contrast board visual themes, multi-track audio playlists, dynamic valid-move indicators, and toggleable competitive rulesets.

---

## ✨ Features

- **Custom Color Theme Presets:** Choose from 6 distinct aesthetic themes seamlessly injected into the board render pipeline:
  - *Default:* Classic light brown and chocolate board with red and black pieces.
  - *Tournament:* High-visibility khaki/green board with white and crimson firebrick pieces.
  - *Cyberpunk:* Striking near-black/slate board with glowing neon cyan and magenta pieces.
  - *Ocean:* Relaxing soft-teal gradients with ice-blue and deep-teal pieces.
  - *Autumn:* Warm tan and dark brown board with sandy and dark red pieces.
  - *Minimalist:* Clean light/charcoal grey board with sharp off-white and matte black pieces.
- **Dynamic Move Indicators:** Click a piece to highlight it in yellow and preview gray indicator dots detailing all valid move paths (normal diagonal steps and/or jump paths).
- **Intelligent Rules Enforcement:** Fully implements fundamental checkers algorithms including:
  - Backwards-movement blocking for standard pieces.
  - Omnidirectional 360° fluid moving and jumping for promoted Kings (indicated with distinct thick gold outlines).
  - Optional or strict forced-capture rules (`req_jumps`) preventing regular moves if an opponent can be jumped.
  - Look-ahead sequential multi-jump handling for combo capture chains.
- **Asynchronous Ambient Audio:** Layered background tracks handled seamlessly using `pygame.mixer` to ensure music loops fluidly without blocking input threads or freezing the Tkinter-based graphics framework.

---

## 🛠️ Project Structure

Ensure your local development environment mimics the folder hierarchy below so paths parse correctly:

```text
checkers/
│
├── music/                     # Dedicated directory for audio presets
│   ├── wethands.mp3
│   ├── pigstep.mp3
│   ├── cereal.mp3
│   ├── chilllofi.mp3
│   ├── mountains.mp3
│   └── clairedelune.mp3
│
├── graphics.py                # The standard Tkinter wrapper file
├── settings.py                # Houses theme and music preset dictionaries
├── startingscreen.py          # Entry point (Main menu GUI and settings config)
└── game.py                    # Core checkers logic, board matrices, and loop

### 🧩 Bonus Feature: Chess Notation Trainer
Included in the repository is a standalone speed-training mini-game (`notation_trainer.py`) designed to help players master coordinate visualization (e.g., tracking locations like `e4`, `g6`, or `b2`).
* **Interactive Challenges:** The console prompts you with a random coordinate. Your goal is to click the correct matching tile on the board as fast as possible.
* **Smart Feedback Loop:** A correct click flashes the square **Green** and grows your point streak. A wrong click turns your mistake **Red**, flashes the actual answer **Green**, and displays a "Game Over" score overlay screen.
