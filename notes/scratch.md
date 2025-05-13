1. Items that are directly connected by keybinds must execute immediately
   - Movements, InstantActions
2. Items that want to be reused later

Actions register() method must be called manually before doing the action


keybinds need their own class so that they can execute immediately


an action can do work on text or be a movement
an action can have a motion (optional)


change is a group of actions (previously CompoundAction)
all changes have a list of actions
