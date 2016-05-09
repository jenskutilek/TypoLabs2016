#MenuTitle: 18 Extremum Point Check
from robofab.world import CurrentFont, CurrentGlyph
from fontTools.pens.basePen import BasePen

class MyPen(BasePen):
    
    def _moveTo(self, pt):
        pass
    
    def _lineTo(self, pt):
        pass
    
    def _curveToOne(self, bcp1, bcp2, pt):
        print "CURVE %s, %s, %s, %s" % (self._getCurrentPoint(), bcp1, bcp2, pt)
    
    def _closePath(self):
        pass
    
    def _endPath(self):
        pass
    
    def addComponent(self, baseGlyphName, transformation):
        pass


p = MyPen(CurrentFont())
CurrentGlyph().draw(p)