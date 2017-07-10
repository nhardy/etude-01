#!/usr/bin/env python3
import sys

"""
Author(s): Kimberley Louw, Nathan Hardy
"""

class Ant:
    """
    Class for the ant
    """
    def __init__(self, plane):
        self._plane = plane
        self.x = 0 # Ant x position
        self.y = 0 # Ant y position
        self._vx = 0 # Ant was moving neither left nor right on arrival
        self._vy = 1 # Ant was moving in the positive-y direction on arrival

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
    lines = sys.stdin.readlines()
    # Turn lines into scenarios
    scenarios = [Scenario([], 0)] # TODO: Parse and produce a list of Scenarios
    # Print Scenarios
    for scenario in scenarios:
        print(scenario)

if __name__ == '__main__':
    main()
