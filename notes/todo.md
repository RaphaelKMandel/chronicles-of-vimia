- Make motions stand alone:
    - Contain evaluate() method, and any other properties to run the motion
    - For finds, contain the required logic for
        - Building the find
        - Saving the last find

- Movement is a class that is created with a single input: the instantiated motion
  - execute() method executes the movement
- OperatorMovements are their own class - dont need to use inheritence to call execute() on movement, but not actions


# Features:
- show keys at bottom
- action/movement counts?
- f,dt.
- split buffer into odd lines and put inserted text on new line