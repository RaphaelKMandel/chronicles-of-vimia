# Chronicles of Vimia (WIP)


A typing-tutor-style game where the user uses Vim motions to edit falling text strings before they hit the ground. 
The game helps you practice Vim commands in a fun, interactive way.
This game focuses on using Vim motions to quickly edit text, 
rather than studying the optimal way to edit text with the minimum possible keystrokes.
As you progress and get better, using fewer keystrokes should happen naturally, and your scores will be higher.


This is a work in progress, so please forgive any bugs or missing features.


## Setup

1. Install the bundled monospace Agave Nerd Font (Optional)

2. Install the required python dependencies:
```bash
pip install -r requirements.txt
```

3. Run the game:
```bash
python main.py
```

## How to Play
- Use Vim motions to move around the falling buffers
- Use Vim commands to delete text in red and insert mode to add text in green 
- Score points by correctly typing and editing the falling text
- Use as few keystrokes as possible to get the highest score
- Quit the game using :q
- Start a new game using :n


## Current Features
1. Motions (h, j, k, l, f, t, w, e, b) and Commands (d, :, )
2. An Arcade mode, where users shoot for the highest score


## Planned Features
1. A campaign mode, where users can level up by purchasing motions
2. Text objects (iw, aw, ap) and associated spawners
3. ...
