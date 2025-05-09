# Chronicles of Vimia (WIP)


A typing-tutor-style game where the user uses Vim motions to edit falling text strings before they hit the ground. 
The game helps you practice Vim commands in a fun, interactive way.
This game focuses on using Vim motions to quickly edit text, rather than presenting puzzles to study.
As you progress and get better, using fewer keystrokes should happen naturally, and your scores will be higher.

## Why Python???
Before you ask, the game is implemented in python for a few reasons:
1. Because I wanted to
2. I am a hobbyist/aspiring software developer who is learning, and I wanted a medium sized (?) project where I could practice
   using Design Patterns, such as State, Command, Memento, Strategy, Template Methods, etc...
3. I wanted more game-style effects, such as falling buffers, explody effects, etc... which I dont think is possible in Vim
4. I thought it would be useful to have this library for other future vim-related games

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
- Use Vim motions to move around in the falling buffers
- Use Vim commands to delete text in red and insert mode to add text in green 
- Score points by correctly typing and editing the falling text before it hits the ground
- Your keystrokes are counted so use as few keystrokes as possible to get the highest score
- Dont let the buffers hit the ground, or your keystrokes will be penalized!
- Quit the game using :q
- Start a new game using :n


## Current Features
1. Motions (h, j, k, l, f, t, w, e, b) and Commands (d, .)
2. An Arcade mode, where users shoot for the highest score and new types of puzzles are added as score increases


## Planned Features
1. A campaign mode, where users can level up by acquiring motions
2. Text objects (iw, aw, ap) and associated spawners
3. More than one falling buffer at a time
4. Better graphics, effects, etc...
5. A larger library of buffer spawners to teach certain chords/patterns
6. Adding new spawners as score increases