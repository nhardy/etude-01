#!/usr/bin/env python3

import re
import sys

"""
Etude 1
Authors: Kimberley Louw, Nathan Hardy
"""

_DIRECTIONS = {
    'N': (0, 1),
    'S': (0, -1),
    'E': (1, 0),
    'W': (-1, 0),
}

_DIRS = ['N', 'E', 'S', 'W']
_DNA_STRAND = re.compile(r'(\S) ([NSEW]{4}) (\S{4})')
_IS_NUMERIC = re.compile(r'^\d+$')

class Strand:
    def __init__(self, initial: str, directions: list, states: list):
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
        initial, directions, states = match.group(1), match.group(2), match.group(3)
        return cls(initial, directions, states)

    def out_direction(self, in_direction: str):
        return self._in_to_out_direction[in_direction]

    def out_state(self, in_state: str):
        return self._in_to_out_state[in_state]

    def __str__(self):
        return '{} {} {}'.format(self.initial, ''.join(map(lambda d: self.out_direction(d), _DIRS)), ''.join(map(lambda d: self.out_state(d), _DIRS)))

class Ant:
    """
    Class for the ant
    """
    def __init__(self, plane):
        self._plane = plane
        self.x = 0 # Ant x position
        self.y = 0 # Ant y position
        self._previous = 'N'

    def move(self):
        # TODO: Moving should modify the grid where necessary
        pass

class Plane:
    def __init__(self, default: str):
        # Initialise cells as a dictionary of coordinate tuples to states
        # This way, the plane can extend infinitely without having to worry
        # about allocating space in a list
        self._cells = {
            (0, 0): default,
        }

    def get_state(self, x: int, y: int) -> str:
        return default if (x, y) not in self._cells else self._cells[(x, y)]

    def set_state(self, x: int, y: int, state: str) -> str:
        self._cells[(x, y)] = state

class Scenario:
    def __init__(self, strands: list, steps: int):
        self.ant = Ant(Plane('w')) # TODO: Correct initial state
        self.strands = strands
        self.steps = steps

        for _ in range(steps):
            self.ant.move()

    def result(self) -> str:
        return '# {} {}'.format(self.ant.x, self.ant.y)

    def __str__(self):
        return '\n'.join([
            *self.strands,
            str(self.steps),
            self.result(),
        ])


def main():
    strands = []

    for unstripped_line in sys.stdin.readlines():
        line = unstripped_line.strip()
        if line == '':
            continue

        if line.startswith('#'):
            continue

        if _IS_NUMERIC.match(line):
            steps = int(line)
            print(Scenario(strands, steps))
            strands = []

        strands.append(Strand.from_raw(line))

if __name__ == '__main__':
    main()
