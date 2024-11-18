## Introduction
Implementation and visualization of "Computational Geometry Algorithms and Applications" in python

## Requirement
1. [pyray](https://github.com/ryu577/pyray)

## How to Run
in `main.py`:
```py
import convex_hull
import pyray

screen_width = 800
screen_height = 800

task = convex_hull.ConvexHull(convex_hull.generate_random_points(300))

def main():
    pyray.init_window(screen_width, screen_height, "Hello")
    task_iter = task.run()
    pyray.set_target_fps(24)

    while not pyray.window_should_close() and not pyray.is_key_pressed(pyray.KeyboardKey.KEY_Q):
        pyray.begin_drawing()
        pyray.clear_background(pyray.RAYWHITE)

        try:
            world = next(task_iter)
        except StopIteration:
            world = task.create_current_state()

        world.draw(screen_width, screen_height)

        pyray.end_drawing()

    pyray.close_window()

main()
```
change the first line `import convex_hull` and the line of `task = ..` to corresponding algorithm.

## Chapter 1: Computational Geometry
### i. Convex Hull
- file: `convex_hull.py`

## Chapter 2: Line Segment Intersections
### i. Line Intersections
- file: `line_intersections.py`
