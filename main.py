#!/usr/bin/env python3

import re
import sys

"""
Etude 1: Ants on a Plane
Authors: Kimberley Louw, Nathan Hardy
Simulation of creatures related to Langton's Ant.
"""

# Mathematical convention of directional step to coordinate
_DIRECTIONS = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}

_DIRS = ['N', 'E', 'S', 'W']
# Regular expressions
_DNA_STRAND = re.compile(r'(\S) ([NSEW]{4}) (\S{4})', re.I)
_IS_NUMERIC = re.compile(r'^\d+$')

class Strand:
    def __init__(self, initial: str, directions: str, states: str):
        self.initial = initial
        self._in_to_out_direction = {
            'N': directions[0],
            'E': directions[1],
            'S': directions[2],
            'W': directions[3],
        }
        self._in_to_out_state = {
            'N': states[0],
            'E': states[1],
            'S': states[2],
            'W': states[3],
        }

    @classmethod
    def from_raw(cls, raw: str):
        match = _DNA_STRAND.match(raw)
        initial, directions, states = match.group(1), match.group(2).upper(), match.group(3)
        return cls(initial, directions, states)

    def out_direction(self, in_direction: str):
        return self._in_to_out_direction[in_direction]

    def out_state(self, in_state: str):
        return self._in_to_out_state[in_state]

    def __str__(self): #TODO: line too long
        return '{} {} {}'.format(self.initial, ''.join(map(lambda d: self.out_direction(d), _DIRS)), ''.join(map(lambda d: self.out_state(d), _DIRS)))

class Ant:
    """
    Class for the ant
    """
    def __init__(self, plane, strands: list):
        self._plane = plane
        self._strands = { strand.initial: strand for strand in strands }
        self.x = 0 # Ant x position
        self.y = 0 # Ant y position
        self._previous = 'N'

    def move(self):
        # Get current state
        state = self._plane.get_state(self.x, self.y)
        # Get relevant strand
        strand = self._strands[state]
        # Set Plane state for Ant's current position to value determined by the strand
        self._plane.set_state(self.x, self.y, strand.out_state(self._previous))
        # Get the appropriate direction from the strand based on the previous step
        direction = strand.out_direction(self._previous)
        dx, dy = _DIRECTIONS[direction]
        # move ant
        self.x += dx
        self.y += dy
        self._previous = direction # update previous directional step

class Plane:
    def __init__(self, default: str):
        self.default = default
        # Initialise cells as a dictionary of coordinate tuples to states
        # This way, the plane can extend infinitely without having to worry
        # about allocating space in a list
        self._cells = {
            (0, 0): self.default,
        }

    def get_state(self, x: int, y: int) -> str:
        return self.default if (x, y) not in self._cells else self._cells[(x, y)]

    def set_state(self, x: int, y: int, state: str) -> str:
        self._cells[(x, y)] = state

class Scenario:
    def __init__(self, strands: list, steps: int):
        default_state = strands[0].initial
        self.strands = strands
        self.ant = Ant(Plane(default_state), strands)
        self.steps = steps

        for _ in range(steps):
            self.ant.move()

    def result(self) -> str:
        return '# {} {}'.format(self.ant.x, self.ant.y)

    def __str__(self):
        return '\n'.join([
            *list(map(str, self.strands)),
            str(self.steps),
            self.result(),
        ])


def main():
    scenarios = []
    strands = []

    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()
        if line == '': # ignore blank lines
            continue

        if line.startswith('#'): # ignore comments
            continue

        if _IS_NUMERIC.match(line): # number of steps ending scenario
            steps = int(line)
            scenarios.append(Scenario(strands, steps))
            strands = []
        else:
            strands.append(Strand.from_raw(line))

    print('\n\n'.join(map(str, scenarios)))

if __name__ == '__main__':
    main()
