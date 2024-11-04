import pyray
import itertools
import random
import math
from dataclasses import dataclass

import world
from world import Point, Edge
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


class ConvexHull:
    def __init__(self, points: list[Point]):
        self.points = points
        self.edges: list[Edge] = []

    def create_current_state_slow(self) -> world.World:
        _world = world.World()
        _world.game_objects = []
        _world.game_objects.extend(self.points)
        _world.game_objects.extend(self.edges)

        colors = {}
        for game_object in _world.game_objects:
            colors[game_object] = pyray.BLACK

        _world.colors = colors

        return _world

    def create_current_state(self) -> world.World:
        _world = world.World()
        _world.game_objects = []
        _world.game_objects.extend(self.points)
        hull = self.l_upper + self.l_lower[1:]
        edges = []
        for i in range(len(hull) - 1):
            edges.append(Edge(hull[i], hull[i + 1]))

        _world.game_objects.extend(edges)

        colors = {}
        for game_object in _world.game_objects:
            colors[game_object] = pyray.BLACK

        _world.colors = colors

        return _world


    def run_slow(self):
        for p, q in itertools.product(self.points, self.points):
            if p == q:
                continue

            for r in self.points:
                if r == p or r == q:
                    continue

                edge = Edge(p, q)
                direction = point_direction_to_edge(edge, r)
                if direction == -1:
                    break
            else:
                yield self.create_current_state()
                self.edges.append(Edge(p, q))

        print('Finish')

    def run(self):
        self.l_lower = []
        self.l_upper = []

        self.points.sort(key=lambda p: p.x)
        self.l_upper = [self.points[0], self.points[1]]
        yield self.create_current_state()
        for i in range(2, len(self.points)):
            self.l_upper.append(self.points[i])
            yield self.create_current_state()
            while len(self.l_upper) > 2 and point_direction_to_edge(Edge(self.l_upper[-3], self.l_upper[-2]), self.l_upper[-1]) != +1:
                self.l_upper.pop(len(self.l_upper) - 2)
                yield self.create_current_state()

        self.l_lower = [self.points[-1], self.points[-2]]
        yield self.create_current_state()
        for i in reversed(range(0, len(self.points) - 2)):
            self.l_lower.append(self.points[i])
            yield self.create_current_state()
            while len(self.l_lower) > 2 and point_direction_to_edge(Edge(self.l_lower[-3], self.l_lower[-2]), self.l_lower[-1]) != +1:
                self.l_lower.pop(len(self.l_lower) - 2)
                yield self.create_current_state()

        print('Finish')
