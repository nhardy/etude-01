#!/usr/bin/env python3

"""
Etude 1: Ants on a Plane
Authors: Kimberley Louw, Nathan Hardy
Simulation of creatures related to Langton's Ant.
"""

import re
import sys

# Mathematical convention of directional step to coordinate
_DIRECTIONS = {
    'N': (0, 1),
    'E': (1, 0),
    'S': (0, -1),
    'W': (-1, 0),
}

# Ordered direction list
_DIRS = ['N', 'E', 'S', 'W']
# Regular expressions
_DNA_STRAND = re.compile(r'(\S) ([NESW]{4}) (\S{4})', re.I)
_IS_NUMERIC = re.compile(r'^\d+$')

class Strand:
    """
    DNA Strand class used for abstraction
    """

    def __init__(self, initial: str, directions: str, states: str):
        self.initial = initial
        self._in_to_out_direction = {
            direction: directions[index] for index, direction in enumerate(_DIRS)
        }
        self._in_to_out_state = {
            direction: states[index] for index, direction in enumerate(_DIRS)
        }

    @classmethod
    def from_raw(cls, raw: str):
        """
        Returns a new Strand object, given its raw string representation
        """

        match = _DNA_STRAND.match(raw)
        initial = match.group(1)
        directions = match.group(2).upper()
        states = match.group(3)
        return cls(initial, directions, states)

    def out_direction(self, in_direction: str) -> str:
        """
        Given an in_direction, returns the corresponding out direction
        for the current strand
        """

        return self._in_to_out_direction[in_direction]

    def out_state(self, in_direction: str) -> str:
        """
        Given an in_direction, returns the corresponding out state
        for the current strand
        """

        return self._in_to_out_state[in_direction]

    def __str__(self) -> str:
        return '{} {} {}'.format(
            self.initial,
            ''.join(map(self.out_direction, _DIRS)),
            ''.join(map(self.out_state, _DIRS)),
        )

class Ant:
    """
    Class for the Ant
    """

    def __init__(self, plane, strands: list):
        self._plane = plane
        # Create a map of key-value pairs;
        # Key: Initial state that the strand applies to
        # Value: Strand (including rules)
        self._strands = {
            strand.initial: strand for strand in strands
        }
        self.x = 0 # Ant x position
        self.y = 0 # Ant y position
        # Assuming the Ant's initial step was to the North
        self._previous = 'N'

    def move(self):
        """
        Moves the Ant once, according to its internal rules
        """

        # Get current state
        state = self._plane.get_state(self.x, self.y)
        # Get relevant strand
        strand = self._strands[state]
        # Set Plane state for Ant's current position to the new
        # value, as determined by the strand
        self._plane.set_state(
            self.x,
            self.y,
            strand.out_state(self._previous),
        )
        # Get the appropriate direction from the strand
        # based on the previous step direction
        direction = strand.out_direction(self._previous)
        # Get the x and y delta for the new direction
        dx, dy = _DIRECTIONS[direction]
        # move ant
        self.x += dx
        self.y += dy
        self._previous = direction # update previous directional step

class Plane:
    """
    Infinite Plane class, helpful for abstracting away default cell state
    """

    def __init__(self, default: str):
        self.default = default
        # Initialise cells as a dictionary of coordinate tuples to states
        # This way, the plane can extend infinitely without having to worry
        # about allocating space in a list
        self._cells = {
            (0, 0): self.default,
        }

    def get_state(self, x: int, y: int) -> str:
        """
        Gets the current state for the point (x, y)
        """

        if (x, y) in self._cells:
            return self._cells[(x, y)]

        return self.default

    def set_state(self, x: int, y: int, state: str) -> str:
        """
        Sets the state at (x, y)
        """

        self._cells[(x, y)] = state

class Scenario:
    """
    Scenario class initialises the Ant, and provides a __str__ method
    which prints the Scenario in the format described in the etude
    """

    def __init__(self, strands: list, steps: int):
        default_state = strands[0].initial
        self.strands = strands
        self.ant = Ant(Plane(default_state), strands)
        self.steps = steps

        for _ in range(steps):
            self.ant.move()

    def result(self) -> str:
        """
        Method returns the final position of the Ant, in the
        format specified by the etude
        """

        return '# {} {}'.format(self.ant.x, self.ant.y)

    def __str__(self) -> str:
        return '\n'.join([
            *list(map(str, self.strands)),
            str(self.steps),
            self.result(),
        ])


def main():
    """
    Main program method
    """

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
        else: # DNA strand
            strands.append(Strand.from_raw(line))

    print('\n\n'.join(map(str, scenarios)))

if __name__ == '__main__':
    main()
