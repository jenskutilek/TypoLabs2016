# MenuTitle: SVG Pen
from fontTools.pens.basePen import BasePen

# (C) 2016 by Jens Kutilek
# https://raw.githubusercontent.com/jenskutilek/TypoLabs2016/master/penCollection/svgPen.py

# See also:
# http://www.w3.org/TR/SVG/paths.html#PathDataBNF
# https://developer.mozilla.org/en-US/docs/Web/SVG/Tutorial/Paths


# SVG path parsing code from:
# http://codereview.stackexchange.com/questions/28502/svg-path-parsing


def parse_svg_path(path_data):
    digit_exp = "0123456789eE"
    comma_wsp = ", \t\n\r\f\v"
    drawto_command = "MmZzLlHhVvCcSsQqTtAa"
    sign = "+-"
    exponent = "eE"
    float = False
    entity = ""
    for char in path_data:
        if char in digit_exp:
            entity += char
        elif char in comma_wsp and entity:
            yield entity
            float = False
            entity = ""
        elif char in drawto_command:
            if entity:
                yield entity
                float = False
                entity = ""
            yield char
        elif char == ".":
            if float:
                yield entity
                entity = "."
            else:
                entity += "."
                float = True
        elif char in sign:
            if entity and entity[-1] not in exponent:
                yield entity
                float = False
                entity = char
            else:
                entity += char
    if entity:
        yield entity


def drawSVGPath(pen, path=""):
    """
    Draw an SVG path that is supplied as a string. This is limited to SVG paths
    that contain only elements that can be matched to the usual path elements
    found in a glyph.
    """
    path_data = list(parse_svg_path(path))
    # print(path_data)
    i = 0
    prev_x: int | float = 0
    prev_y: int | float = 0
    while i < len(path_data):
        # print(i, path_data[i])
        v = path_data[i]
        if v in "Cc":
            # Cubic curve segment
            x1, y1, x2, y2, x3, y3 = path_data[i + 1 : i + 7]
            # print("    ", x1, y1, x2, y2, x3, y3)
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
            x3 = float(x3)
            y3 = float(y3)
            if v == "c":
                x1 += prev_x
                y1 += prev_y
                x2 += prev_x
                y2 += prev_y
                x3 += prev_x
                y3 += prev_y
            pen.curveTo(
                (x1, y1),
                (x2, y2),
                (x3, y3),
            )
            prev_x = x3
            prev_y = y3
            i += 7
        elif v in "Hh":
            # Horizontal line segment
            x = path_data[i + 1]
            # print("    ", x)
            x = float(x)
            if v == "h":
                x += prev_x
            pen.lineTo((x, prev_y))
            prev_x = x
            i += 2
        elif v in "LlMm":
            # Move or Line segment
            x, y = path_data[i + 1 : i + 3]
            # print("    ", x, y)
            x = float(x)
            y = float(y)
            if v in "lm":
                x += prev_x
                y += prev_y
            if v in "Ll":
                pen.lineTo((x, y))
            else:
                pen.moveTo((x, y))
            prev_x = x
            prev_y = y
            i += 3
        elif v in "Qq":
            # Quadratic curve segment
            x1, y1, x2, y2 = path_data[i + 1 : i + 5]
            # print("    ", x1, y1, x2, y2)
            x1 = float(x1)
            y1 = float(y1)
            x2 = float(x2)
            y2 = float(y2)
            if v == "q":
                x1 += prev_x
                y1 += prev_y
                x2 += prev_x
                y2 += prev_y
            pen.qCurveTo(
                (x1, y1),
                (x2, y2),
            )
            prev_x = x2
            prev_y = y2
            i += 5
        elif v in "Vv":
            # Vertical line segment
            y = path_data[i + 1]
            # print(y)
            y = float(y)
            if v == "v":
                y += prev_y
            pen.lineTo((prev_x, y))
            prev_y = y
            i += 2
        elif v in "Zz":
            pen.closePath()
            i += 1
        else:
            print(
                "SVG path element '%s' is not supported for glyph paths."
                % path_data[i]
            )
            break


class SVGpen(BasePen):
    def __init__(
        self,
        glyphSet,
        round_coordinates=False,
        force_relative_coordinates=False,
        optimize_output=False,
    ):
        """
        A pen that converts a glyph outline to an SVG path. After drawing,
        SVGPen.d contains the path as string. This corresponds to the SVG path
        element attribute "d".

        :param glyphSet: The font object
        :type glyphSet: :py:class:`fontParts.RFont`

        :param round_coordinates: Round all coordinates to integer. Default is
            False.
        :type round_coordinates: bool

        :param force_relative_coordinates: Store all coordinates as relative.
            Default is False, i.e. choose whichever notation (absolute or
            relative) produces shorter output for each individual segment.
        :type force_relative_coordinates: bool

        :param optimize_output: Make the output path string as short as
            possible. Default is True. Setting this to False also overrides the
            relative_coordinates option.
        :type optimize_output: bool
        """
        self._rnd = round_coordinates
        self._rel = force_relative_coordinates
        self._opt = optimize_output
        BasePen.__init__(self, glyphSet)
        self.reset()

    def reset(self):
        self.prev_x: int | float = 0  # previous point
        self.prev_y: int | float = 0
        self._set_first_point((0, 0))
        self._set_previous_point((0, 0))
        self._set_previous_cubic_control(None)
        self._set_previous_quadratic_control(None)
        self._prev_cmd = None
        self.relative = False
        self.d = ""

    def _append_shorter(self, absolute, relative):
        # Check if relative output is smaller
        if not self._rel and len(absolute) <= len(relative) or not self._opt:
            cmd_str = absolute
            self.relative = False
        else:
            cmd_str = relative
            self.relative = True

        if cmd_str[0] == self._prev_cmd:
            rest = cmd_str[1:]
            if rest.startswith("-"):
                self.d += rest
            else:
                self.d += " " + rest
        else:
            self.d += cmd_str

    def _get_shorter_sign(self, value):
        if value < 0 and self._opt:
            return "%g" % value
        else:
            return " %g" % value

    def _round_pt(self, pt):
        # Round the point based on the current rounding settings
        if self._rnd:
            x, y = pt
            return (int(round(x)), int(round(y)))
        return pt

    def _set_first_point(self, pt):
        self.first_x, self.first_y = pt

    def _set_previous_point(self, pt):
        self.prev_x, self.prev_y = pt

    def _set_previous_cubic_control(self, pt):
        if pt is None:
            self.prev_cx = None
            self.prev_cy = None
        else:
            self._set_previous_quadratic_control(None)
            self.prev_cx, self.prev_cy = pt

    def _set_previous_quadratic_control(self, pt):
        if pt is None:
            self.prev_qx = None
            self.prev_qy = None
        else:
            self._set_previous_cubic_control(None)
            self.prev_qx, self.prev_qy = pt

    def _reset_previous_controls(self):
        self._set_previous_cubic_control(None)
        self._set_previous_quadratic_control(None)

    def _moveTo(self, pt):
        x, y = self._round_pt(pt)
        cmd = "Mm"
        a = "M%g" % x
        a += self._get_shorter_sign(y)
        r = "m%g" % (x - self.prev_x)
        r += self._get_shorter_sign(y - self.prev_y)
        self._append_shorter(a, r)
        self._set_first_point((x, y))
        self._set_previous_point((x, y))
        self._reset_previous_controls()
        self._prev_cmd = cmd[self.relative]

    def _lineTo(self, pt):
        x, y = self._round_pt(pt)
        if y == self.prev_y:
            cmd = "Hh"
            a = "H%g" % x
            r = "h%g" % (x - self.prev_x)
        elif x == self.prev_x:
            cmd = "Vv"
            a = "V%g" % y
            r = "v%g" % (y - self.prev_y)
        else:
            cmd = "Ll"
            a = "L%g" % x
            a += self._get_shorter_sign(y)
            r = "l%g" % (x - self.prev_x)
            r += self._get_shorter_sign(y - self.prev_y)
        self._append_shorter(a, r)
        self._set_previous_point((x, y))
        self._reset_previous_controls()
        self._prev_cmd = cmd[self.relative]

    def _curveToOne(self, p1, p2, pt):
        x1, y1 = self._round_pt(p1)
        x2, y2 = self._round_pt(p2)
        x3, y3 = self._round_pt(pt)
        if self.prev_cx is None:
            self._set_previous_cubic_control((self.prev_x, self.prev_x))
        if (
            self.prev_y - y1 + self.prev_y == self.prev_cy
            and self.prev_x - x1 + self.prev_x == self.prev_cx
        ):
            # Control point p1 is mirrored, use S command and omit p1
            cmd = "Ss"
            a = "S%g" % x2
            for coord in [y2, x3, y3]:
                a += self._get_shorter_sign(coord)
            r = "s%g" % (x2 - self.prev_x)
            for coord in [
                y2 - self.prev_y,
                x3 - self.prev_x,
                y3 - self.prev_y,
            ]:
                r += self._get_shorter_sign(coord)
        else:
            cmd = "Cc"
            a = "C%g" % x1
            for coord in [y1, x2, y2, x3, y3]:
                a += self._get_shorter_sign(coord)
            r = "c%g" % (x1 - self.prev_x)
            for coord in [
                y1 - self.prev_y,
                x2 - self.prev_x,
                y2 - self.prev_y,
                x3 - self.prev_x,
                y3 - self.prev_y,
            ]:
                r += self._get_shorter_sign(coord)
        self._append_shorter(a, r)
        self._set_previous_point((x3, y3))
        self._set_previous_cubic_control((x2, y2))
        self._prev_cmd = cmd[self.relative]

    def _qCurveToOne(self, p1, p2):
        x1, y1 = self._round_pt(p1)
        x2, y2 = self._round_pt(p2)
        if self.prev_qx is None:
            self._set_previous_quadratic_control((self.prev_x, self.prev_x))
        if (
            self.prev_y - y1 + self.prev_y == self.prev_qy
            and self.prev_x - x1 + self.prev_x == self.prev_qx
        ):
            # Control point p1 is mirrored, use T command and omit p1
            cmd = "Tt"
            a = "T%g" % x2
            a += self._get_shorter_sign(y2)
            r = "t%g" % (x2 - self.prev_x)
            r += self._get_shorter_sign(y2 - self.prev_y)
        else:
            cmd = "Qq"
            a = "Q%g" % x1
            for coord in [y1, x2, y2]:
                a += self._get_shorter_sign(coord)
            r = "q%g" % (x1 - self.prev_x)
            for coord in [
                y1 - self.prev_y,
                x2 - self.prev_x,
                y2 - self.prev_y,
            ]:
                r += self._get_shorter_sign(coord)
        self._append_shorter(a, r)
        self._set_previous_point((x2, y2))
        self._set_previous_quadratic_control((x1, y1))
        self._prev_cmd = cmd[self.relative]

    def _closePath(self):
        cmd = "z" if self._rel else "Z"
        self.d += cmd
        self._set_previous_point((self.first_x, self.first_y))
        self._reset_previous_controls()
        self._prev_cmd = cmd
