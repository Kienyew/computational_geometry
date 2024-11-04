import math
from world import Point, Edge

"""
Returns wheter the point p is left to or right to an edge.
- -1 if left to
- +1 if right to
-  0 if colinear
"""
def point_direction_to_edge(e: Edge, p: Point):
    a = e.start
    b = e.end
    determinant = (b.x - a.x) * (p.y - a.y) - (b.y - a.y) * (p.x - a.x)

    if determinant > 0:
        return -1
    elif determinant < 0:
        return +1
    else:
        return 0

