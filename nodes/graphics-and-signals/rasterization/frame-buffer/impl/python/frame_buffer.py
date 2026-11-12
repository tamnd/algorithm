# SPDX-License-Identifier: MIT
# Part of https://algorithm.tamnd.com/frame-buffer/. The authors are listed in prov/RBDXB5.jsonl.

"""A software frame buffer: a W by H array of pixels with C bytes each, stored row by row
in one flat bytearray with a row pitch P >= W * C bytes.

Row 0 is the top row, as the display scans it, and the byte offset of pixel (i, j) is
j * P + i * C. The P - W * C pad bytes at the end of each row belong to no pixel.
Writes outside the buffer are clipped.
"""

from typing import Optional, Sequence

Color = tuple[int, ...]


class FrameBuffer:
    def __init__(self, width: int, height: int, channels: int = 4, pitch: Optional[int] = None, align: int = 4):
        """An empty buffer of width x height pixels with `channels` bytes each, all bytes zero.

        With no pitch given, each row is padded to a multiple of `align` bytes.
        """
        if width < 0 or height < 0 or channels < 1 or align < 1:
            raise ValueError("bad frame buffer size")
        if pitch is None:
            pitch = -(-width * channels // align) * align
        if pitch < width * channels:
            raise ValueError("the pitch must be at least width * channels bytes")
        self.width, self.height, self.channels, self.pitch = width, height, channels, pitch
        self.data = bytearray(height * pitch)

    def _color(self, color: Sequence[int]) -> bytes:
        if len(color) != self.channels or any(not 0 <= v <= 255 for v in color):
            raise ValueError("a color is one byte per channel")
        return bytes(color)

    def offset(self, i: int, j: int) -> int:
        """The byte offset of pixel (i, j)."""
        return j * self.pitch + i * self.channels

    def write_pixel(self, i: int, j: int, color: Sequence[int]) -> bool:
        """Store color at pixel (i, j) and return True, or return False if (i, j) is outside. O(C)."""
        c = self._color(color)
        if 0 <= i < self.width and 0 <= j < self.height:  # @line L1
            a = j * self.pitch + i * self.channels  # @line L2
            self.data[a:a + self.channels] = c  # @line L3
            return True
        return False

    def read_pixel(self, i: int, j: int) -> Optional[Color]:
        """The color of pixel (i, j), or None if (i, j) is outside. O(C)."""
        if not (0 <= i < self.width and 0 <= j < self.height):  # @line R1
            return None
        a = j * self.pitch + i * self.channels  # @line R2
        return tuple(self.data[a:a + self.channels])

    def fill_rect(self, x0: int, y0: int, x1: int, y1: int, color: Sequence[int]) -> int:
        """Store color at each pixel (i, j) with x0 <= i < x1 and y0 <= j < y1, clipped. Returns the pixel count."""
        c = self._color(color)
        x0, x1 = max(x0, 0), min(x1, self.width)  # @line F1
        y0, y1 = max(y0, 0), min(y1, self.height)
        if x0 >= x1 or y0 >= y1:
            return 0
        span = c * (x1 - x0)  # @line F2
        for j in range(y0, y1):  # @line F3
            a = j * self.pitch + x0 * self.channels
            self.data[a:a + len(span)] = span
        return (x1 - x0) * (y1 - y0)

    def clear(self, color: Sequence[int]) -> None:
        """Store color at every pixel. The pad bytes stay as they are. O(H P)."""
        self.fill_rect(0, 0, self.width, self.height, color)

    def row(self, j: int) -> bytes:
        """The W * C pixel bytes of row j, in the order the display reads them."""
        if not 0 <= j < self.height:
            raise IndexError("row outside the buffer")
        a = j * self.pitch
        return bytes(self.data[a:a + self.width * self.channels])

    def check_invariant(self) -> None:
        assert self.pitch >= self.width * self.channels
        assert len(self.data) == self.height * self.pitch
