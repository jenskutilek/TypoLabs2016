# MenuTitle: 08 Draw Polygon In Glyph
from mojo.roboFont import CurrentGlyph
from math import cos, pi, radians, sin


def draw_polygon(pen, x, y, diameter=50, n=8, phi=0.0, clockwise=False):
    """
    pen:       a RoboFab pen.
    (x, y):    center coordinates
    diameter:  diameter of the polygon
    n:         number of corners
    phi:       rotation in degrees
    clockwise: direction of the path
    """

    radius = 0.5 * diameter
    phi = radians(phi)

    # Start point
    pen.moveTo((x - radius * sin(phi), y - radius * cos(phi)))

    # Draw the segments
    if clockwise:
        for i in range(1, n):
            rho = 2 * pi * i / n
            pen.lineTo(
                (x - radius * sin(phi + rho), y - radius * cos(phi + rho))
            )
    else:
        for i in range(n - 1, 0, -1):
            rho = 2 * pi * i / n
            pen.lineTo(
                (x - radius * sin(phi + rho), y - radius * cos(phi + rho))
            )

    # Close the path
    pen.closePath()


if __name__ == "__main__":
    g = CurrentGlyph()
    g.clear()
    p = g.getPen()

    diameter = 600
    n = 8

    for i in range(10):
        clockwise = bool(i % 2)
        phi = 1.2 * i * pi
        draw_polygon(p, 275, 216, diameter, n, phi, clockwise)
        # n -= 1
        diameter -= 50
