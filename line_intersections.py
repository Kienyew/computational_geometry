from typing import Optional, Tuple
import pprint
import pyray
import random
import math
from world import Point, Line, World
from dataclasses import dataclass
from sortedcontainers import SortedList, SortedKeyList
from utils import line_intersection_point
from bisect import bisect_left, bisect_right

# Assume segments have no coincide points


@dataclass
class EventPoint:
    point: Point
    segment: Optional[Line]
    is_upper_point: bool
    intersect_segments: Optional[Tuple[Line, Line]]

    def __lt__(self, other: 'EventPoint'):
        return self.point.y < other.point.y

    def __gt__(self, other):
        return not (self < other)

    def __eq__(self, other):
        return self.point.near(other.point) or self is other


def generate_random_lines(num_lines: int) -> list[Line]:
    points = []

    for _ in range(num_lines * 2):
        radians = random.uniform(0, 2 * math.pi)
        radius = random.uniform(0, 0.4)

        x = radius * math.cos(radians) + 0.5
        y = radius * math.sin(radians) + 0.5

        point = Point(x, y)
        points.append(point)

    lines = []
    for i in range(len(points) // 2):
        line = Line(points[2 * i], points[2 * i + 1])
        lines.append(line)

    return lines


class line_intersections:
    def __init__(self, lines: list[Line]):
        self.lines = lines

        # Ensure line.start is the top-left node of line
        for line in self.lines:
            if line.end.y < line.start.y:
                line.start, line.end = line.end, line.start
            elif line.start.y == line.end.y and line.start.x > line.end.x:
                line.start, line.end = line.end, line.start

        self.Q = SortedList([])
        self.height = 0
        self.lines = lines
        self.intersection_points: list[Point] = []
        self.checking_segment_pair: Optional[Tuple[Line, Line]] = None
        self.status: list[Line] = []

    def status_key(self, segment: Line):
        intersection = line_intersection_point(segment, self.get_current_sweeping_line())
        assert intersection is not None
        return intersection.x

    def create_current_state(self) -> World:
        world = World()
        world.game_objects.extend(self.lines)

        for line in self.lines:
            if line in self.status:
                world.colors[line] = pyray.RED
            else:
                world.colors[line] = pyray.BLACK

        sweep_line = self.get_current_sweeping_line()
        world.game_objects.append(sweep_line)
        world.colors[sweep_line] = pyray.RED

        world.game_objects.extend(self.intersection_points)
        for point in self.intersection_points:
            world.colors[point] = pyray.BLUE

        for ep in self.Q:
            world.game_objects.append(ep.point)
            world.colors[ep.point] = pyray.ORANGE

        if self.checking_segment_pair:
            world.game_objects.extend(self.checking_segment_pair)
            world.colors[self.checking_segment_pair[0]] = pyray.BLUE
            world.colors[self.checking_segment_pair[1]] = pyray.BLUE

        return world

    def run(self):
        for line in self.lines:
            self.Q.add(EventPoint(line.start, line, True, None))
            self.Q.add(EventPoint(line.end, line, False, None))

        while len(self.Q) > 0:
            p: EventPoint = self.Q.pop(0)
            self.handle_event_point(p)
            yield self.create_current_state()

    def get_current_sweeping_line(self):
        horizontal_line = Line(Point(0.0, self.height), Point(1.0, self.height))
        return horizontal_line

    def handle_event_point(self, p: EventPoint):
        self.height = p.point.y

        if p.is_upper_point:
            assert p.segment is not None
            self_index = bisect_left(self.status, self.status_key(p.segment), key=self.status_key)
            self.status.insert(self_index, p.segment)
            s = p.segment
            if self_index - 1 >= 0:
                r = self.status[self_index - 1]
            else:
                r = None

            if self_index + 1 < len(self.status):
                t = self.status[self_index + 1]
            else:
                t = None

            if r:
                self.find_new_event(r, p.segment)

            if t:
                self.find_new_event(p.segment, t)

        elif p.segment:
            self_index = self.status.index(p.segment)

            s = p.segment
            if self_index - 1 >= 0:
                r = self.status[self_index - 1]
            else:
                r = None

            if self_index + 1 < len(self.status):
                t = self.status[self_index + 1]
            else:
                t = None

            self.status.pop(self_index)

            if r and t:
                self.find_new_event(r, t)


        else:
            assert p.intersect_segments
            self.intersection_points.append(p.point)
            s, t = p.intersect_segments
            self.status.remove(s)
            self.status.remove(t)
            self.height += 1e-5
            s_index = bisect_left(self.status, self.status_key(s), key=self.status_key)
            self.status.insert(s_index, s)
            t_index = bisect_left(self.status, self.status_key(t), key=self.status_key)
            self.status.insert(t_index, t)

            s_index = self.status.index(s)
            t_index = self.status.index(t)

            if s_index > t_index:
                s_index, t_index = t_index, s_index

            if s_index - 1 >= 0:
                r = self.status[s_index - 1]
            else:
                r = None

            if t_index + 1 < len(self.status):
                u = self.status[t_index + 1]
            else:
                u = None

            s = self.status[s_index]
            t = self.status[t_index]

            if r:
                self.find_new_event(r, s)

            if u:
                self.find_new_event(t, u)


        # self.status.sort(key=self.status_key)


        ## sweeping_intersection_xs = [self.status_key(status) for status in self.status]
        ## diffs = [sweeping_intersection_xs[i + 1] - sweeping_intersection_xs[i] for i in range(len(sweeping_intersection_xs) - 1)]
        ## for diff in diffs:
        ##     if diff < 0 and abs(diff) > 0.01:
        ##         pprint.pprint(diffs)
        ##         pprint.pprint(p)
        ##         raise RuntimeError("Error")

    def find_new_event(self, segment_left: Line, segment_right: Line):
        self.checking_segment_pair = (segment_left, segment_right)
        intersection = line_intersection_point(segment_left, segment_right)
        if intersection is not None and intersection.y > self.height and intersection not in self.intersection_points:
            new_event_point = EventPoint(intersection, None, False, (segment_left, segment_right))
            for ep in self.Q:
                if ep.point.near(intersection):
                    print('Found duplicate event point, in self.Q check:', EventPoint(intersection, None, False, None) in self.Q)
                    return

            self.Q.add(new_event_point)
