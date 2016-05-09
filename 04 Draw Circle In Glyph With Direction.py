#MenuTitle: 04 Draw Circle In Glyph With Direction
from robofab.world import CurrentGlyph

def draw_circle(pen, (x, y), diameter=50, clockwise=False, roundness=0.552):
    
    radius = 0.5 * diameter
    ctrl   = 0.5 * diameter * roundness
    
    points = [
        [
            (
                (x + ctrl,   y - radius),
                (x + radius, y - ctrl),
                (x + radius, y)
            ),
            (
                (x + radius, y + ctrl),
                (x + ctrl,   y + radius),
                (x,          y + radius)
            ),
            (
                (x - ctrl,   y + radius),
                (x - radius, y + ctrl),
                (x - radius, y)
            ),
            (
                (x - radius, y - ctrl),
                (x - ctrl,   y - radius),
                (x,          y - radius)
            ),
        ],
        [
            (
                (x - ctrl,   y - radius),
                (x - radius, y - ctrl),
                (x - radius, y)
            ),
            (
                (x - radius, y + ctrl),
                (x - ctrl,   y + radius),
                (x,          y + radius)
            ),
            (
                (x + ctrl,   y + radius),
                (x + radius, y + ctrl),
                (x + radius, y)
            ),
            (
                (x + radius, y - ctrl),
                (x + ctrl,   y - radius),
                (x,          y - radius)
            ),
        ],
    ][clockwise]
    # False/True is used as index of the list here.
    # Python automatically uses the Integer representation of the Boolean values:
    # False = 0
    # True  = 1
    
    pen.moveTo((x, y - radius))
    
    for ctrl1, ctrl2, pt in points:
        pen.curveTo(ctrl1, ctrl2, pt)
    
    pen.closePath()


p = CurrentGlyph().getPen()
draw_circle(p, (275, 216), 400, False)