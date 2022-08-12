# MenuTitle: 19 Extremum Point Check
from mojo.roboFont import CurrentFont, CurrentGlyph
from fontTools.pens.basePen import BasePen


# helper functions from fontTools.misc.arrayTools


def normRect(rect):
    """Normalize the rectangle so that the following holds:
    xMin <= xMax and yMin <= yMax
    """
    (xMin, yMin, xMax, yMax) = rect
    return min(xMin, xMax), min(yMin, yMax), max(xMin, xMax), max(yMin, yMax)


def pointInRect(p, rect):
    """Return True when point (x, y) is inside rect."""
    (x, y) = p
    xMin, yMin, xMax, yMax = rect
    return (xMin <= x <= xMax) and (yMin <= y <= yMax)


class MyPen(BasePen):
    def _moveTo(self, pt):
        pass

    def _lineTo(self, pt):
        pass

    def _curveToOne(self, bcp1, bcp2, pt):
        curr = self._getCurrentPoint()

        rect = normRect((curr[0], curr[1], pt[0], pt[1]))

        if not pointInRect(bcp1, rect):
            print("Control point is out of bounding box:", bcp1)
            print("    ", rect)

        if not pointInRect(bcp2, rect):
            print("Control point is out of bounding box:", bcp2)
            print("    ", rect)

    def _closePath(self):
        pass

    def _endPath(self):
        pass

    def addComponent(self, baseGlyphName, transformation):
        pass


if __name__ == "__main__":
    p = MyPen(CurrentFont())
    CurrentGlyph().draw(p)
