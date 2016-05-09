#MenuTitle: 01 MyPen
from robofab.world import CurrentGlyph
from fontTools.pens.basePen import AbstractPen

class MyPen(AbstractPen):
    
    def moveTo(self, pt):
        print "pen.moveTo(%s)" % (pt,)
    
    def lineTo(self, pt):
        print "pen.lineTo(%s)" % (pt,)
    
    def curveTo(self, *pts):
        print "pen.curveTo%s" % (pts,)
    
    def qCurveTo(self, *pts):
        print "pen.qCurveTo%s" % (pts,)
    
    def closePath(self):
        print "pen.closePath()"
    
    def endPath(self):
        print "pen.endPath()"
    
    def addComponent(self, baseGlyphName, transformation):
        print "pen.addComponent(%r, %s)" % (baseGlyphName, tuple(transformation))


p = MyPen()
CurrentGlyph().draw(p)