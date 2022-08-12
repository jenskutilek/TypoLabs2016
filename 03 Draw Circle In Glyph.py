#MenuTitle: 03 Draw Circle In Glyph
from mojo.roboFont import CurrentGlyph

def draw_circle(pen, pt, diameter=50, roundness=0.552):
    x, y = pt
    radius = 0.5 * diameter
    ctrl   = 0.5 * diameter * roundness

    # Start point (bottom of circle)
    pen.moveTo((x, y - radius))

    # First quarter circle segment
    pen.curveTo(
        (x + ctrl,   y - radius),
        (x + radius, y - ctrl),
        (x + radius, y)
    )

    # Second quarter circle segment
    pen.curveTo(
        (x + radius, y + ctrl),
        (x + ctrl,   y + radius),
        (x,          y + radius)
    )

    # Third quarter circle segment
    pen.curveTo(
        (x - ctrl,   y + radius),
        (x - radius, y + ctrl),
        (x - radius, y)
    )

    # Fourth quarter circle segment
    pen.curveTo(
        (x - radius, y - ctrl),
        (x - ctrl,   y - radius),
        (x,          y - radius)
    )

    # Close the path (required)
    pen.closePath()


if __name__ == "__main__":
    g = CurrentGlyph()
    g.clear()
    p = g.getPen()

    # Draw a rectangle
    p.moveTo((10, 0))
    p.lineTo((540, 0))
    p.lineTo((540, 432))
    p.lineTo((10, 432))
    p.closePath()

    # Draw a circle with our circle function
    draw_circle(p, (275, 216), 400)
