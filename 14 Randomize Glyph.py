# MenuTitle: 14 Randomize Glyph
from mojo.roboFont import CurrentFont, RGlyph
from fontTools.pens.basePen import BasePen
from random import randint


class MyPen(BasePen):

    # from fontTools.pens.basePen.BasePen:
    def __init__(self, glyphSet, writer_pen, max_move=0):
        self.glyphSet = glyphSet
        self.__currentPoint = None
        self.writer_pen = writer_pen
        self.max_move = max_move

    def randomize(self, pt):
        dx = randint(-self.max_move, self.max_move)
        dy = randint(-self.max_move, self.max_move)
        return (pt[0] + dx, pt[1] + dy)

    def _moveTo(self, pt):
        self.writer_pen.moveTo(self.randomize(pt))

    def _lineTo(self, pt):
        self.writer_pen.lineTo(self.randomize(pt))

    def _curveToOne(self, bcp1, bcp2, pt):
        self.writer_pen.curveTo(
            self.randomize(bcp1), self.randomize(bcp2), self.randomize(pt)
        )

    def _closePath(self):
        self.writer_pen.closePath()

    def _endPath(self):
        self.writer_pen.endPath()

    def addComponent(self, baseGlyphName, transformation):
        pass


def randomize_glyph(glyph):
    source = glyph
    font = glyph.font

    # Save the anchors from the original glyph in a list
    anchors = [a for a in source.anchors]

    # Remove all anchors from the glyph so they don't interfere with our processing
    for a in anchors:
        source.removeAnchor(a)

    # Temporary glyph to which the pen is writing
    target = RGlyph()
    target_pen = target.getPen()

    source_pen = MyPen(font, target_pen, 10)
    source.draw(source_pen)

    # Clear the original glyph and add the modfied outline
    source.clear(components=False)
    source.appendGlyph(target)

    # Restore the saved anchors
    for a in anchors:
        source.appendAnchor(a.name, a.position)


if __name__ == "__main__":
    font = CurrentFont()

    for glyph_name in font.selection:
        randomize_glyph(font[glyph_name])
