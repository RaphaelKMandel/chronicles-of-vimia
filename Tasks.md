# Tasks
- [x] Game is global?
- [x] Rename Game to Editor?
- [ ] Syntax Highlighting?
- [ ] Coloring? Treat each char/word as its own class/color?
- [ ] Render cursor in Modes directly; going to be required for visual mode
- [ ] Insert mode saves inserted text as action
- [ ] Make Action class?
- [ ] Undo/Redo?


# Approach
- How to handle states/modes and operations
- At present, states take focus, overwriting current state of editor
- Command pattern? ; repeats a search, . repeats an action
  - Save all inputs to a command except the text to operate on (as that can be different)
- Should state be a stack?
  - Need to repeat Everything from Normal mode insert mode, and back to normal mode
- Should each composite command have internal states?
- Want to be able to write pressed keys as part of a command on the fly in bottom right


# Action 
- Uses command pattern to encapsulate an action
- __init__ method starts everything off; does not change to OperatorState
- activate method contains parent class logic while execute method contains logic for child classes
- activate method will be called when OperatorState deactivates