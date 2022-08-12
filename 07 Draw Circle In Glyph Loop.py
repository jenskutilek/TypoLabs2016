#MenuTitle: 07 Draw Circle In Glyph Loop
from mojo.roboFont import CurrentGlyph
from math import cos, degrees, pi, radians, sin


def draw_circle(pen, pt, diameter=50, clockwise=False, roundness=0.552, phi=0.0):
    x, y = pt
    radius = 0.5 * diameter
    ctrl   = 0.5 * diameter * roundness

    factor = -1 if clockwise else 1

    phi = radians(phi)

    pen.moveTo(
        (
            x + radius * sin(phi),
            y - radius * cos(phi)
        )
    )

    for i in range(4):
        rho = - factor * phi - i * 0.5 * pi
        ctrl1, ctrl2, pt = (
            (
                round(x - factor * radius * sin(rho) + factor * ctrl * cos(rho)),
                round(y -          radius * cos(rho) -          ctrl * sin(rho))
            ),
            (
                round(x + factor * radius * cos(rho) - factor * ctrl * sin(rho)),
                round(y -          radius * sin(rho) -          ctrl * cos(rho))
            ),
            (
                round(x + factor * radius * cos(rho)),
                round(y -          radius * sin(rho))
            )
        )
        pen.curveTo(ctrl1, ctrl2, pt)

    pen.closePath()


if __name__ == "__main__":
    g = CurrentGlyph()
    g.clear()
    p = g.getPen()

    r = 400
    rd = 0.95

    for i in range(14):
        clockwise = bool(i % 2)
        rd -= 0.06
        phi = 2 * i * pi
        draw_circle(p, (275, 216), r, clockwise, rd, phi)
        r -= 20
