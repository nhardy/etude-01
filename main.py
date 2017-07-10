#!/usr/bin/env python3
import sys

"""
Author(s): Kimberley Louw, Nathan Hardy
"""

class Ant:
    """
    Class for the ant
    """
    def __init__(self):
        self.x = 0 # Ant x position
        self.y = 0 # Ant y position
        self._vx = 0 # Ant was moving neither left nor right on arrival
        self._vy = 1 # Ant was moving in the positive-y direction on arrival

    def move(self):
        pass

class Scenario:
    def __init__(self, strands: list, steps: int):
        self.ant = Ant()
        self.strands = strands
        self.steps = steps

        for _ in range(steps):
            pass # Do something according to strands?

    def result(self) -> str:
        return '# {} {}'.format(self.ant.x, self.ant.y)

    def __str__(self):
        return '\n'.join([
            *self.strands,
            self.result(),
        ])


def main():
    lines = sys.stdin.readlines()
    # Turn lines into scenarios
    scenarios = [Scenario([], 0)] # Stub
    # Print Scenarios
    for scenario in scenarios:
        print(scenario)

if __name__ == '__main__':
    main()
