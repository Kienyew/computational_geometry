from dataclasses import dataclass
from pprint import pprint
import pyray

@dataclass
class GameObject:
    def draw(self, color: pyray.Color, screen_width: int, screen_height: int):
        raise NotImplementedError()

@dataclass
class Point(GameObject):
    x: float
    y: float

    def __hash__(self):
        return hash(self.x) ^ hash(self.y)

    def draw(self, color: pyray.Color, screen_width: int, screen_height: int):
        radius = 0.003
        x = int(self.x * screen_width)
        y = int(self.y * screen_width)
        r = int(radius * (screen_width + screen_height) / 2)

        pyray.draw_circle(x, y, r, color)


@dataclass
class Edge(GameObject):
    start: Point
    end: Point

    def __hash__(self):
        return hash(self.start) ^ hash(self.end)

    def draw(self, color: pyray.Color, screen_width: int, screen_height: int):
        sx = int(self.start.x * screen_width)
        sy = int(self.start.y * screen_width)
        ex = int(self.end.x * screen_height)
        ey = int(self.end.y * screen_height)
        pyray.draw_line(sx, sy, ex, ey, color)

class World:
    def __init__(self):
        self.game_objects: list[GameObject] = []
        self.colors: dict[GameObject, pyray.Color] = {}

    def draw(self, screen_width: int, screen_height: int):
        for game_object in self.game_objects:
            game_object.draw(self.colors[game_object], screen_width, screen_height)

