from abc import ABC, abstractmethod
import re
import pygame
from constants import *

class Movement(ABC):
    @abstractmethod
    def execute(self, text: str, cursor_pos: int) -> int:
        pass

class LeftMovement(Movement):
    def execute(self, text: str, cursor_pos: int) -> int:
        return max(0, cursor_pos - 1)

class RightMovement(Movement):
    def execute(self, text: str, cursor_pos: int) -> int:
        return min(len(text), cursor_pos + 1)

class WordStartMovement(Movement):
    def __init__(self, big_word=False):
        self.big_word = big_word

    def execute(self, text: str, cursor_pos: int) -> int:
        if self.big_word:
            pattern = r'\S+'
        else:
            pattern = r'[a-zA-Z0-9\'\-]+|[^\s]'
        
        boundaries = []
        for match in re.finditer(pattern, text):
            boundaries.append((match.start(), match.end()))
        
        for start, _ in boundaries:
            if start > cursor_pos:
                return start
        return len(text)

class WordEndMovement(Movement):
    def __init__(self, big_word=False):
        self.big_word = big_word

    def execute(self, text: str, cursor_pos: int) -> int:
        if self.big_word:
            pattern = r'\S+'
        else:
            pattern = r'[a-zA-Z0-9\'\-]+|[^\s]'
        
        boundaries = []
        for match in re.finditer(pattern, text):
            boundaries.append((match.start(), match.end()))
        
        for start, end in boundaries:
            if start <= cursor_pos < end:
                return end - 1
        for start, end in boundaries:
            if start > cursor_pos:
                return end - 1
        return len(text)

class BackWordStartMovement(Movement):
    def __init__(self, big_word=False):
        self.big_word = big_word

    def execute(self, text: str, cursor_pos: int) -> int:
        if self.big_word:
            pattern = r'\S+'
        else:
            pattern = r'[a-zA-Z0-9\'\-]+|[^\s]'
        
        boundaries = []
        for match in re.finditer(pattern, text):
            boundaries.append((match.start(), match.end()))
        
        for start, end in reversed(boundaries):
            if end <= cursor_pos:
                return start
        return 0

class EndOfLineMovement(Movement):
    def execute(self, text: str, cursor_pos: int) -> int:
        return len(text)

class FirstNonBlankMovement(Movement):
    def execute(self, text: str, cursor_pos: int) -> int:
        for i, char in enumerate(text):
            if not char.isspace():
                return i
        return 0

class FindCharMovement(Movement):
    def __init__(self, char: str, backward=False, till=False):
        self.char = char
        self.backward = backward
        self.till = till

    def execute(self, text: str, cursor_pos: int) -> int:
        if self.backward:
            if self.till:
                pos = text.rfind(self.char, 0, cursor_pos)
                return pos + 1 if pos != -1 else cursor_pos
            else:
                pos = text.rfind(self.char, 0, cursor_pos)
                return pos if pos != -1 else cursor_pos
        else:
            if self.till:
                pos = text.find(self.char, cursor_pos + 1)
                return pos - 1 if pos != -1 else cursor_pos
            else:
                pos = text.find(self.char, cursor_pos + 1)
                return pos if pos != -1 else cursor_pos

class State(ABC):
    @abstractmethod
    def handle_input(self, event, game) -> 'State':
        pass

    @abstractmethod
    def draw(self, game):
        pass

class NormalState(State):
    def handle_input(self, event, game) -> State:
        if event.type == pygame.KEYDOWN:
            if event.unicode == ':':
                return CommandState()
            elif event.unicode == 'h':
                return MovementState(LeftMovement())
            elif event.unicode == 'l':
                return MovementState(RightMovement())
            elif event.unicode == 'w':
                return MovementState(WordStartMovement())
            elif event.unicode == 'W':
                return MovementState(WordStartMovement(big_word=True))
            elif event.unicode == 'e':
                return MovementState(WordEndMovement())
            elif event.unicode == 'E':
                return MovementState(WordEndMovement(big_word=True))
            elif event.unicode == 'b':
                return MovementState(BackWordStartMovement())
            elif event.unicode == 'B':
                return MovementState(BackWordStartMovement(big_word=True))
            elif event.unicode == '$':
                return MovementState(EndOfLineMovement())
            elif event.unicode == '^' or event.unicode == '_':
                return MovementState(FirstNonBlankMovement())
            elif event.unicode == 'f':
                return FindState(backward=False, till=False)
            elif event.unicode == 'F':
                return FindState(backward=True, till=False)
            elif event.unicode == 't':
                return FindState(backward=False, till=True)
            elif event.unicode == 'T':
                return FindState(backward=True, till=True)
        return self

    def draw(self, game):
        pass

class MovementState(State):
    def __init__(self, movement: Movement):
        self.movement = movement

    def handle_input(self, event, game) -> State:
        game.text.cursor_pos = self.movement.execute(game.text.text, game.text.cursor_pos)
        return NormalState()

    def draw(self, game):
        pass

class FindState(State):
    def __init__(self, backward=False, till=False):
        self.backward = backward
        self.till = till

    def handle_input(self, event, game) -> State:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return NormalState()
            elif event.unicode.isprintable():
                return MovementState(FindCharMovement(event.unicode, self.backward, self.till))
        return self

    def draw(self, game):
        mode_text = ""
        if self.backward:
            mode_text += "F" if not self.till else "T"
        else:
            mode_text += "f" if not self.till else "t"
        mode_surface = game.font.render(mode_text, True, CURSOR_COLOR)
        game.screen.blit(mode_surface, (10, 10))

class CommandState(State):
    def __init__(self):
        self.buffer = ""

    def handle_input(self, event, game) -> State:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                return NormalState()
            elif event.unicode.isprintable():
                self.buffer += event.unicode
            elif event.key == pygame.K_RETURN:
                if self.buffer == "q":
                    game.running = False
                return NormalState()
        return self

    def draw(self, game):
        command_text = game.font.render(f":{self.buffer}", True, CURSOR_COLOR)
        game.screen.blit(command_text, (10, 10)) 