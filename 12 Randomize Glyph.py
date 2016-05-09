#MenuTitle: 12 Randomize Glyph
from robofab.world import CurrentFont, CurrentGlyph
from robofab.objects.objectsRF import RGlyph
from fontTools.pens.basePen import BasePen

class MyPen(BasePen):
    
    # from fontTools.pens.basePen.BasePen:
    def __init__(self, glyphSet, writer_pen):
        self.glyphSet = glyphSet
        self.__currentPoint = None
        self.writer_pen = writer_pen
    
    def _moveTo(self, pt):
        self.writer_pen.moveTo(pt)
    
    def _lineTo(self, pt):
        self.writer_pen.lineTo(pt)
    
    def _curveToOne(self, bcp1, bcp2, pt):
        self.writer_pen.curveTo(bcp1, bcp2, pt)
    
    def _closePath(self):
        self.writer_pen.closePath()
    
    def _endPath(self):
        self.writer_pen.endPath()
    
    def addComponent(self, baseGlyphName, transformation):
        pass


source = CurrentGlyph()

# Save the anchors from the original glyph in a list
anchors = [a for a in source.anchors]

# Remove all anchors from the glyph so they don't interfere with our processing
for a in anchors:
    source.removeAnchor(a)

# Temporary glyph to which the pen is writing
target = RGlyph()
target_pen = target.getPen()

source_pen = MyPen(CurrentFont(), target_pen)
source.draw(source_pen)

# Clear the original glyph and add the modfied outline
source.clear()
source.appendGlyph(target)

# Restore the saved anchors
for a in anchors:
    source.appendAnchor(a.name, a.position)
