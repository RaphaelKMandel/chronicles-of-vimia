# Tasks
- [x] Game is global?
- [x] Rename Game to Editor?
- [x] Coloring? Treat each char/word as its own class/color?
- [x] Render cursor in Modes directly; going to be required for visual mode
- [x] Insert mode saves inserted text as action
- [x] Make Action class?
- [x] Undo/Redo?
- Buffer class:
  - [x] method to determine x,y location given row,col
  - [x] give it a name, and allow navigation with :e <file> with tabs
- [x] Buffer spawner class
- [x] Change Action class to Change class?
- [x] Make demo file to demonstrate concept
- [x] Insert mode creates list of actions (like a macro)?
  - [x] Insert Action to insert a char?
- [x] Classes for move actions, like delete, change, etc..
- [x] show keys at bottom
- [x] f,dt.
- [x] split buffer into odd lines and put inserted text on new line
- [x] Make Editor.state a stack, with properties to get and set the state stack
- [ ] Add counts to actions/motions
- [ ] Arcade vs Campaign mode

# Approach

## States
  - State pattern to control inputs
  - Editor state is a stack, with the last value handling inputs
  - Editor has properties to handle current state and setting of new state
  - Editor.pop backs up one state
  - States receive parent as input, and call parent.finish when state exits


## Motions
  - Motions contain all information needed to perform the motion
  - Motions contain an `evaluate()` method which computes the motion 
  - `evaluate()` takes in a buffer and any other arguments needed, such as `reversed` in `Find`
  - If a motion requires further inputs, the __init__() method should change the state
  - The motion should be finished setting up with the finish() method


## Actions
- Actions obey the command pattern, encapsulating an action
- have a `motion` property, which is used in `execute()` to compute the domain of the command
- `execute()` executes the encapsulated action
- Can be a movement or a single change


## Movements
- have a `motion` property, which is used in `execute()` to move the cursor
  - `execute()` executes the movement


## Changes 
  - Changes are a group of actions or changes that are counted as one when undoing/redoing
  - They are run by calling the `execute()` method

## Finds and Changes
  - Have a LAST class variable to store the last find or action, to be reused
  - The `;` and `,` keys build a new find using the LAST class variable
