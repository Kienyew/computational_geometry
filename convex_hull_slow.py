import pyray
import itertools
import random
import math

import world
from world import Point, Line
from utils import point_direction_to_edge

def generate_random_points(num_points: int) -> list[Point]:
    points = []

    for _ in range(num_points):
        radians = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 0.4)

        x = radius * math.cos(radians) + 0.5
        y = radius * math.sin(radians) + 0.5

        point = world.Point(x, y)
        points.append(point)

    return points


class convex_hull_slow:
    def __init__(self, points: list[Point]):
        self.points = points
        self.edges: list[Line] = []

    def create_current_state(self) -> world.World:
        _world = world.World()
        _world.game_objects = []
        _world.game_objects.extend(self.points)
        _world.game_objects.extend(self.edges)

        colors = {}
        for game_object in _world.game_objects:
            colors[game_object] = pyray.BLACK

        _world.colors = colors

        return _world


    def run(self):
        for p, q in itertools.product(self.points, self.points):
            if p == q:
                continue

            for r in self.points:
                if r == p or r == q:
                    continue

                edge = Line(p, q)
                direction = point_direction_to_edge(edge, r)
                if direction == -1:
                    break
            else:
                yield self.create_current_state()
                self.edges.append(Line(p, q))

        print('Finish')

