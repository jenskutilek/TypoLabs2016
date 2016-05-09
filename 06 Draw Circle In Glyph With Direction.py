from math import cos, degrees, pi, radians, sin


def draw_circle(pen, (x, y), diameter=50, clockwise=False, roundness=0.552, phi=0):
    
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


g = CurrentGlyph()
g.clear()
p = g.getPen()
rd = 0.552
draw_circle(p, (275, 216), 400, False, rd)
draw_circle(p, (275, 216), 300, True,  rd)
draw_circle(p, (275, 216), 200, False, rd)
draw_circle(p, (275, 216), 100, True,  rd)