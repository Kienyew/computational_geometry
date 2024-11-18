import line_intersections
import convex_hull
import pyray
from world import Point, Line
import numpy as np

screen_width = 800
screen_height = 800

lines = [ ]
for x in np.arange(0.1, 0.9, 0.05):
    lines.append(Line(Point(x, 0.1), Point(0.9, 1.0 - x)))

for x in np.arange(0.1, 0.9, 0.05):
    lines.append(Line(Point(x, 0.9), Point(0.878, x)))


# lines = line_intersections.generate_random_lines(100)
task = line_intersections.line_intersections(lines)

def main():
    pyray.init_window(screen_width, screen_height, "Hello")
    task_iter= task.run()
    pyray.set_target_fps(10)

    world = None

    while not pyray.window_should_close() and not pyray.is_key_pressed(pyray.KeyboardKey.KEY_Q):
        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)
        try:
            world= next(task_iter)
        except StopIteration as e:
            world = task.create_current_state()

        world.draw(screen_width, screen_height)
        pyray.end_drawing()

    pyray.close_window()

main()
