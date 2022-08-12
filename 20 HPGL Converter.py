# MenuTitle: 20 HPGL Converter
from mojo.roboFont import CurrentGlyph
from fontTools.pens.basePen import BasePen


class HPGLPen(BasePen):
    def __init__(self, glyphSet, scale=1):
        BasePen.__init__(self, glyphSet)
        self._scale = scale
        self._init_seq = self._get_init_sequence()
        self._hpgl = ""
        self._end_seq = self._get_end_sequence()
        self._pen_down = False
        self._prev_segment = None

    def _get_init_sequence(self):
        seq = "IN;"  # IN = Initialize
        # IP = Scaling Point x1, y1, x2, y2
        seq += "IP%s,%s,%s,%s;" % (0, 0, 16158, 11040)  # reported by plotter
        # SC = Scale
        seq += "SC%s,%s,%s,%s;" % (0, 0, 1190, 842)  # A3 in points (1/72 inch)
        # the rest of the init sequence
        seq += "PU;"  # PU = Pen Up
        seq += "SP1;"  # SP1 = Select Pen 1
        seq += "LT;\n"  # LT = Line Type solid
        return seq

    def _get_end_sequence(self):
        seq = "PU;"  # PU = Pen Up
        seq += "SP;"  # Put down the pen
        seq += "EC;"  # EC = ?
        # seq += "PG1;"  # PG = Page Feed
        # seq += "EC1;"  # EC = ?
        seq = "PA0,0;"  # Move head to 0, 0
        seq += "OE;\n"  # OE = ?
        return seq

    def _get_scaled_pt(self, pt):
        x, y = pt
        if self._scale != 1:
            return (x * self._scale, y * self._scale)
        else:
            return (int(round(x)), int(round(y)))

    def _moveTo(self, pt):
        pt = self._get_scaled_pt(pt)
        self._hpgl += "PU%s,%s" % pt
        self._pen_down = False
        self.lastMove = pt
        self._prev_segment = "move"

    def _lineTo(self, pt):
        if self._prev_segment not in ["line", "curve"]:
            self._hpgl += ";PD"
        else:
            self._hpgl += ","
        pt = self._get_scaled_pt(pt)
        self._hpgl += "%s,%s" % pt
        self._prev_segment = "line"

    def _curveToOne(self, bcp1, bcp2, pt):
        bcp1 = self._get_scaled_pt(bcp1)
        bcp2 = self._get_scaled_pt(bcp2)
        pt = self._get_scaled_pt(pt)

        if self._prev_segment not in ["line", "curve"]:
            self._hpgl += ";PD"
        else:
            self._hpgl += ","
        self._hpgl += "%s,%s,%s,%s,%s,%s" % (
            bcp1[0],
            bcp1[1],
            bcp2[0],
            bcp2[1],
            pt[0],
            pt[1],
        )
        self._prev_segment = "curve"

    def _closePath(self):
        if self._prev_segment not in ["line", "curve"]:
            self._hpgl += ";PD"
            self._hpgl += "%s,%s\n" % pt
        else:
            self._hpgl += ","
            pt = self._get_scaled_pt(self.lastMove)
            self._hpgl += "%s,%s;\n" % pt
        self._prev_segment = "close"

    def _endPath(self):
        self._hpgl += u"PU;\n"
        self._prev_segment = "end"

    @property
    def hpgl(self):
        return self._init_seq + self._hpgl + self._end_seq


def glyph_to_hpgl(glyph):
    # Drawing limits: (left 0; bottom 0; right 16158; top 11040)
    anchors = [a for a in glyph.anchors]
    glyph.clear(contours=False, components=False, anchors=True)
    pen = HPGLPen(glyph.font)
    glyph.draw(pen)
    for a in anchors:
        glyph.appendAnchor(a.name, a.position)
    return pen.hpgl


if __name__ == "__main__":
    g = CurrentGlyph()
    print(glyph_to_hpgl(g))
