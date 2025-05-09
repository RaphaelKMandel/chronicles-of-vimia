# State
- handle_events(event):
  - calls some function or class that:
    1. must do some work
    2. must change state to defer the doing of work
  - must provide the parent state as an input so that it can return to the parent state


maybe __call__ takes parent, but __init__() takes initial input parameters

evaluate(buffer) only argument is buffer; all other parameters must be given at instantiation


# Classes:
- horizontal movements
- vertical movements
- finds
