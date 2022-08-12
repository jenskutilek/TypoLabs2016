# MenuTitle: 09 Randomize Glyph
from robofab.world import CurrentFont, CurrentGlyph
from fontTools.pens.basePen import BasePen


class MyPen(BasePen):
    def _moveTo(self, pt):
        print("pen.moveTo(%s)" % (pt,))

    def _lineTo(self, pt):
        print("pen.lineTo(%s)" % (pt,))

    def _curveToOne(self, bcp1, bcp2, pt):
        print("pen.curveTo(%s, %s, %s)" % (bcp1, bcp2, pt))

    def _closePath(self):
        print("pen.closePath()")

    def _endPath(self):
        print("pen.endPath()")

    def addComponent(self, baseGlyphName, transformation):
        pass


p = MyPen(CurrentFont())
CurrentGlyph().draw(p)
