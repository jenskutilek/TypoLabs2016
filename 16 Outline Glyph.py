# MenuTitle: 16 Outline Glyph
from mojo.roboFont import CurrentGlyph, RGlyph
from penCollection.outlinePen import OutlinePen

"""
OutlinePen:
    def __init__(self,
        glyphSet,
        offset=10,
        contrast=0,
        contrastAngle=0,
        connection="square",
        cap="round",
        miterLimit=None,
        closeOpenPaths=True,
        preserveComponents=False
    ):
"""


def outline_glyph(glyph):
    source = glyph
    font = glyph.font

    # Save the anchors from the original glyph in a list
    anchors = [a for a in source.anchors]

    # Remove all anchors from the glyph so they don't interfere with our processing
    source.clear(contours=False, components=False, anchors=True)

    # Temporary glyph to which the pen is writing
    target = RGlyph()
    target_pen = target.getPointPen()

    source_pen = OutlinePen(font, contrast=1, offset=5, connection="round")
    source.draw(source_pen)
    source_pen.drawSettings(drawInner=True, drawOuter=True)
    source_pen.drawPoints(target_pen)

    # Clear the original glyph and add the modfied outline
    source.clear()
    source.appendGlyph(target)

    # Restore the saved anchors
    for a in anchors:
        source.appendAnchor(a.name, a.position)


if __name__ == "__main__":
    g = CurrentGlyph()
    outline_glyph(g)
