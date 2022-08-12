# MenuTitle: 17 SVG Export

# SVG pen implementation (C) 2012 by Andreas Eigendorf
# MIT license
# https://github.com/fontfont/RoboChrome/blob/master/RoboChrome.roboFontExt/lib/colorfont/svgPen.py

import codecs

from mojo.roboFont import CurrentGlyph
from fontTools.pens.basePen import BasePen
from os import system
from os.path import expanduser


class SVGpen(BasePen):
    def __init__(self, glyphSet):
        BasePen.__init__(self, glyphSet)
        self.d = ""

    def _moveTo(self, pt):
        x, y = pt
        self.d += "M%s %s" % (int(round(x)), int(round(y)))

    def _lineTo(self, pt):
        x, y = pt
        self.d += "L%s %s" % (int(round(x)), int(round(y)))

    def _curveToOne(self, pt1, pt2, pt3):
        x1, y1 = pt1
        x2, y2 = pt2
        x3, y3 = pt3
        self.d += "C%d %d %d %d %d %d" % (
            int(round(x1)),
            int(round(y1)),
            int(round(x2)),
            int(round(y2)),
            int(round(x3)),
            int(round(y3)),
        )

    def _closePath(self):
        self.d += "Z"


# functions

# Return an SVG document for a glyph
def svg(glyph, color="#000", group=False, scale=0.5):
    upm = glyph.font.info.unitsPerEm
    svg_doctype = """<?xml version="1.0" encoding="utf-8"?><!DOCTYPE svg PUBLIC '-//W3C//DTD SVG 1.1//EN' 'http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd'>"""
    svg_doc = (
        """<svg enable-background="new 0 0 64 64" id="glyph_%s" width="%d" height="%d" version="1.1" xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">"""
        % (glyph.name, (glyph.width + upm * 0.2) * scale, upm * scale)
    )
    pen = SVGpen(glyph)
    glyph.draw(pen)
    if pen.d:
        if group:
            svg_doc += '<g fill="%s">' % (color)
        svg_doc += (
            '<path transform="translate(%d, %d) scale(%s -%s)" d="%s"/>'
            % (
                upm * 0.1 * scale,
                (upm + glyph.font.info.descender) * scale,
                scale,
                scale,
                pen.d,
            )
        )
        if group:
            svg_doc += "</g>"
    svg_doc += "</svg>"
    return svg_doctype, svg_doc


if __name__ == "__main__":
    html = """<!DOCTYPE html>
    <html>
        <head>
            <title>SVG Export Demo</title>
            <style>
                svg {
                    border: 2px dashed red;
                    background: #fff7e3;
                }
            </style>
        </head>
        <body>
            <h1>%(title)s</h1>
            %(svg)s
        </body>
    </html>
    """

    g = CurrentGlyph()
    file_path = expanduser("~/Desktop/svg_export.html")

    with codecs.open(file_path, "wb", "utf-8") as f:
        svg_doctype, svg_doc = svg(g)
        f.write(
            html
            % {
                "title": g.name,
                "svg": svg_doc,
            }
        )
        f.close()

    system('open "%s"' % file_path)
