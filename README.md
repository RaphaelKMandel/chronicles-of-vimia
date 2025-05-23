# Chronicles of Vimia (WIP)

A typing-tutor-style game where the user uses Vim motions to edit falling text strings before they hit the ground.
The game helps you practice Vim commands in a fun, interactive way.
This game focuses on using Vim motions to quickly edit text, rather than presenting puzzles to study.
As you progress and get better, using fewer keystrokes should happen naturally, and your scores will be higher.

Example Video(https://www.youtube.com/watch?v=yq6urNPjYEA)

This is a work in progress, so please forgive any bugs or missing features.

## Setup

1. Install the bundled monospace Agave Nerd Font (Optional)

2. Install the required python dependencies:

```bash
pip install -r requirements.txt
```

3. Run the game:

```bash
python3 src/run_arcade_mode.py
```

## How to Play

- Use Vim motions to move around in the falling buffers
- Use Vim commands to delete text in red and insert mode to add text in green
- Score points by correctly typing and editing the falling text before it hits the ground
- Your keystrokes are counted so use as few keystrokes as possible to get the highest score
- Don't let the buffers hit the ground, or they will disappear!
- Quit the game using :q
- Start a new game using :n

## Current Features

1. An Arcade mode, where users shoot for the highest score

## Planned Features

1. A campaign mode, where users can level up by acquiring motions; fight bosses (multiline puzzles?) at end
2. A training mode, where puzzles are generated to get practice on a certain motion or command
3. More than one falling buffer at a time
4. Better graphics, effects, etc...
5. A larger library of buffer spawners to teach certain chords/patterns
6. Adding new spawners as score increases
