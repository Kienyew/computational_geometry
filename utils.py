import math
from typing import Optional
from world import Point, Line

"""
Returns wheter the point p is left to or right to an edge.
- -1 if left to
- +1 if right to
-  0 if colinear
"""
def point_direction_to_edge(e: Line, p: Point):
    a = e.start
    b = e.end
    determinant = (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x)

    if determinant > 0:
        return -1
    elif determinant < 0:
        return +1
    else:
        return 0


def line_intersection_point(a: Line, b: Line) -> Optional[Point]:
    x1, y1 = a.start.x, a.start.y
    x2, y2 = a.end.x, a.end.y
    x3, y3 = b.start.x, b.start.y
    x4, y4 = b.end.x, b.end.y

    denom = (y4-y3)*(x2-x1) - (x4-x3)*(y2-y1)
    if denom == 0: # parallel
        return None

    ua = ((x4-x3)*(y1-y3) - (y4-y3)*(x1-x3)) / denom
    if ua < 0 or ua > 1: # out of range
        return None

    ub = ((x2-x1)*(y1-y3) - (y2-y1)*(x1-x3)) / denom
    if ub < 0 or ub > 1: # out of range
        return None

    x = x1 + ua * (x2-x1)
    y = y1 + ua * (y2-y1)
    return Point(x,y)

