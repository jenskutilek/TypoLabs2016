def draw_circle(pen, (x, y), diameter=50, clockwise=False, roundness=0.552):
    
    radius = 0.5 * diameter
    ctrl   = 0.5 * diameter * roundness
    
    factor = -1 if clockwise else 1
    
    points = [
        (
            (x + factor * ctrl,   y - radius),
            (x + factor * radius, y - ctrl),
            (x + factor * radius, y)
        ),
        (
            (x + factor * radius, y + ctrl),
            (x + factor * ctrl,   y + radius),
            (x,                   y + radius)
        ),
        (
            (x - factor * ctrl,   y + radius),
            (x - factor * radius, y + ctrl),
            (x - factor * radius, y)
        ),
        (
            (x - factor * radius, y - ctrl),
            (x - factor * ctrl,   y - radius),
            (x,                   y - radius)
        ),
    ]
    
    pen.moveTo((x, y - radius))
    
    for ctrl1, ctrl2, pt in points:
        pen.curveTo(ctrl1, ctrl2, pt)
    
    pen.closePath()


g = CurrentGlyph()
g.clear()
p = g.getPen()
rd = 0.7
draw_circle(p, (275, 216), 400, False, rd)
draw_circle(p, (275, 216), 300, True,  rd)
draw_circle(p, (275, 216), 200, False, rd)
draw_circle(p, (275, 216), 100, True,  rd)