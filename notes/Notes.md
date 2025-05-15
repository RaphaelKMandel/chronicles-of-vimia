# Tasks

- [ ] Home screen with commands
- [ ] Arcade vs Campaign mode
- [ ] Way to remove certain keybinds

# Approach

## Modes

- Modes are taken from the nvim child process
- Each mode has regular expressions to determine if pending commands are being issued to prevent game freezing

## Buffers

- Simple class to automate process of creating and manipulating buffers in the nvim child process

## Puzzle

- Contain a buffer
- Determine completion criteria e.g. lines must equal some target
- Contain logic for moving and drawing the buffer

## Spawners

- Classes to spawn puzzles
