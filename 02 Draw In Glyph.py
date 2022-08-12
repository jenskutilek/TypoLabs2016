# MenuTitle: 02 Draw In Glyph
from mojo.roboFont import CurrentGlyph

CurrentGlyph().clear()
p = CurrentGlyph().getPen()

# Draw a rectangle
p.moveTo((10, 0))
p.lineTo((540, 0))
p.lineTo((540, 432))
p.lineTo((10, 432))
p.closePath()
