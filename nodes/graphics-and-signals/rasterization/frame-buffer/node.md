---
tag: RBDXB5
kind: data-structure
slug: frame-buffer
name: Frame buffer
aliases:
- framebuffer
- color buffer
area: graphics-and-signals/rasterization
level: intro
summary: A block of memory that holds one color per pixel of the image on a display, stored row by row with a fixed row pitch, which the display reads at each refresh.
model: word-ram
complexity:
  vars: {W: the width in pixels, H: the height in pixels, C: the bytes per pixel, P: the row pitch in bytes}
  time: {worst: Θ(C)}
  space: {extra: Θ(H P)}
properties: {persistent: false, concurrent: false, external: false}
prereqs: [pixel, row-major-order]
see_also: [digital-image, viewport-transform, z-buffer, stencil-buffer, alpha-blending, gamma-correction, color-spaces, graphics-pipeline]
sources:
  - paper: doi:10.1145/362566.362567
    title: A. Michael Noll, Scanned-display computer graphics, Communications of the ACM 14(3), 143 to 150 (1971)
    locator: the whole paper (a scanned raster display whose picture is stored point by point in the memory of a computer)
  - paper: doi:10.1109/85.929909
    title: Richard Shoup, SuperPaint, an early frame buffer graphics system, IEEE Annals of the History of Computing 23(2), 32 to 37 (2001)
    locator: the whole paper (the frame buffer and paint system built at Xerox PARC in 1973, and the earlier frame buffers it names)
  - book: isbn:9780201121100
    title: James D. Foley, Andries van Dam, Steven K. Feiner and John F. Hughes, Computer Graphics, Principles and Practice, second edition, Addison-Wesley, 1990
    locator: Chapter 4, Graphics Hardware (raster-scan display systems, the frame buffer and the video controller)
---

A frame buffer is a block of memory that holds one color for each [pixel](/pixel/) of the image that a display shows. It stores a $W$ by $H$ grid of colors of $C$ bytes each, row by row in [row-major order](/row-major-order/), with a fixed number $P \ge WC$ of bytes from the start of one row to the start of the next. Renderers write colors into it, and the display controller reads it row by row at each refresh, so the bytes in the buffer are what the screen shows. Other buffers of the same shape hold other values per pixel, such as the depth of a [z-buffer](/z-buffer/) or the counts of a [stencil buffer](/stencil-buffer/).

## In plain words

Think of the screen as a grid of tiny lights, each with its own color. The frame buffer is the list of all those colors in the memory of the computer. It holds the first row from left to right, then the second row, and so on to the bottom.

To change what the screen shows, a program writes new colors into this list. Many times a second, the display reads the whole list from the start and sets each light to its color. To find the color of one light, you count the rows above it and the lights to its left. Sometimes each row has a few unused bytes at its end, so that each row starts at a convenient place in memory.

## The abstract type

The value is a map $A$ from the pixels $(i, j)$, with $0 \le i < W$ and $0 \le j < H$, to colors. A color is a tuple of $C$ channels, here one byte each, for example red, green, blue and alpha for $C = 4$. Pixel $(i, j)$ is the sample at the point $(i + \tfrac12, j + \tfrac12)$ of the window coordinates that the [viewport transform](/viewport-transform/) produces, and row 0 is the top row, the first that the display scans. The operations are:

- **WRITE-PIXEL(i, j, c)** sets $A(i, j) = c$ if $(i, j)$ is in the buffer, and does nothing otherwise.
- **READ-PIXEL(i, j)** returns $A(i, j)$.
- **FILL-RECT(x0, y0, x1, y1, c)** sets $A(i, j) = c$ for $x_0 \le i < x_1$ and $y_0 \le j < y_1$, clipped to the buffer.
- **CLEAR(c)** sets every pixel to $c$.
- **SCAN** reads the rows from $j = 0$ to $H - 1$, each from $i = 0$ to $W - 1$; this is what the display does.

## Representation

The buffer is an array $M$ of $HP$ bytes. Pixel $(i, j)$ is at the bytes $M[jP + iC]$ to $M[jP + iC + C - 1]$, so the bytes of each row are contiguous and the rows follow each other at the stride $P$. The last $P - WC$ bytes of each row are pad bytes that belong to no pixel. A pitch larger than $WC$ makes each row start on an aligned address, for example a multiple of 4, 64 or 256 bytes, which the hardware or the memory system prefers. The order of the channels in a pixel is part of the format: one system stores red, green, blue, alpha, and another blue, green, red, alpha.

Common formats have $C = 4$ (8 bits for each of four channels, or 10 bits for each color and 2 for alpha), $C = 2$ (5, 6 and 5 bits for red, green and blue), $C = 1$ (an index into a table of colors) or $C = 8$ (a 16-bit float per channel, for high dynamic range). The values are most often [sRGB](/gamma-correction/)-encoded, not linear light; see [color spaces](/color-spaces/).

**Invariant.** $P \ge WC$ and $|M| = HP$. Under these two conditions the address map is one to one, so writing one pixel changes no other pixel.

## Operations

```pseudo id=main
WRITE-PIXEL(i, j, c)                       ▷ c = (c0, ..., c(C−1))
L1  if 0 ≤ i < W and 0 ≤ j < H then        ▷ clip: a write outside the buffer is dropped
L2      a ← j·P + i·C
L3      M[a .. a + C − 1] ← c0, ..., c(C−1)
```

```pseudo id=read
READ-PIXEL(i, j)
R1  if not (0 ≤ i < W and 0 ≤ j < H) then return NIL
R2  a ← j·P + i·C; return M[a .. a + C − 1]
```

```pseudo id=fill
FILL-RECT(x0, y0, x1, y1, c)               ▷ the half-open rectangle [x0, x1) × [y0, y1)
F1  x0 ← max(x0, 0), x1 ← min(x1, W), y0 ← max(y0, 0), y1 ← min(y1, H); if x0 ≥ x1 or y0 ≥ y1 then return
F2  s ← c repeated x1 − x0 times            ▷ the bytes of one span
F3  for j ← y0 to y1 − 1 do M[j·P + x0·C .. j·P + x1·C − 1] ← s
```

CLEAR(c) is FILL-RECT(0, 0, W, H, c). The rectangle is half-open, like the rule that a pixel belongs to a shape when its center is inside: two rectangles that share an edge cover each pixel one time. In FILL-RECT, the span of each row is one contiguous block of memory, so line F3 is one block copy per row. A display or a program that copies the buffer reads row $j$ as the $WC$ bytes from $M[jP]$.

## Example

Take a buffer with $W = 3$, $H = 2$, $C = 3$ bytes for red, green and blue, and rows padded to a multiple of 4 bytes. Then $WC = 9$ and $P = 12$, so the buffer has 24 bytes. After CLEAR(0, 0, 0), WRITE-PIXEL(2, 1, red) and FILL-RECT(0, 0, 2, 1, blue), with red $= (255, 0, 0)$ and blue $= (0, 0, 255)$, the bytes in hexadecimal are:

| offsets | row | pixel (0, j) | pixel (1, j) | pixel (2, j) | pad |
|---|---|---|---|---|---|
| 0 to 11 | 0 | 00 00 ff | 00 00 ff | 00 00 00 | 00 00 00 |
| 12 to 23 | 1 | 00 00 00 | 00 00 00 | ff 00 00 | 00 00 00 |

WRITE-PIXEL(2, 1) wrote the bytes at offset $1 \cdot 12 + 2 \cdot 3 = 18$ to 20. FILL-RECT wrote the 6 bytes from offset 0 in row 0 as one span. WRITE-PIXEL(3, 0, c) does nothing, because $i = 3$ is outside the buffer; without the clip of line L1 it would write the pad bytes at offsets 9 to 11.

## Correctness

The address map $(i, j, k) \mapsto jP + iC + k$, for $k < C$, is one to one on the pixels and their channels, because $iC + k \le WC - 1 < P$: the row is $\lfloor u / P \rfloor$, the pixel is $\lfloor (u \bmod P) / C \rfloor$ and the channel is $u \bmod C$. So the $C$ bytes that WRITE-PIXEL writes belong to pixel $(i, j)$ only, and the clip of line L1 keeps each write inside the buffer. The span of line F3 is exactly the bytes of the pixels $x_0$ to $x_1 - 1$ of row $j$, in order. No operation writes a pad byte. The full proof is in [the correctness proof](proofs/correctness.md).

## Complexity

| operation | time | notes |
|---|---|---|
| WRITE-PIXEL, READ-PIXEL | $\Theta(C)$ | one multiply-add for the address, $C$ bytes, often one word |
| FILL-RECT of $w$ by $h$ pixels | $\Theta(h + whC)$ | one block copy per row |
| CLEAR | $\Theta(HP)$ | in hardware, often a fast clear that marks tiles as cleared |
| SCAN, one frame | $\Theta(HP)$ | at each refresh of the display |
| space | $HP$ bytes | |

At $C = 4$, a buffer of 1920 by 1080 pixels has 8,294,400 bytes, and one of 3840 by 2160 pixels has 33,177,600 bytes. At 60 frames per second, the display reads the first buffer at $8{,}294{,}400 \times 60 = 497{,}664{,}000$ bytes per second, about 0.5 GB per second, and the second at about 2 GB per second. The writes of the renderer come on top of this, and blending reads each pixel before it writes it. Pixels next to each other in a row are next to each other in memory, so a loop over $i$ inside a loop over $j$ reads memory in order, and a loop in the other order jumps $P$ bytes at each step.

## Variants

- **Double buffering and page flipping.** The renderer draws into a back buffer while the display reads the front buffer, and the two change roles at the vertical blank, so the display never shows a half-drawn frame. Triple buffering adds a third buffer so that the renderer need not wait.
- **Indexed color.** With $C = 1$, each pixel holds an index into a table of colors, which the video hardware looks up at scan time. Changing the table changes all pixels with that index at once.
- **Bit planes.** Early displays stored bit $k$ of each pixel in its own plane, so a pixel with $b$ bits was spread over $b$ separate arrays.
- **Tiled and swizzled layouts.** GPUs store pixels in small tiles, or in the order of a [Z-order curve](/z-order-curve/), so that pixels close in two dimensions are close in memory. The address map is then not $jP + iC$, but it is still one to one.
- **Multisample buffers.** A buffer for [multisample antialiasing](/multisample-antialiasing/) holds several samples per pixel, and a resolve step averages them into an ordinary frame buffer.
- **Several buffers per pixel.** A renderer keeps the color buffer next to a [z-buffer](/z-buffer/) and a [stencil buffer](/stencil-buffer/) of the same size, and the set of them is also called a frame buffer, as in the frame buffer objects of OpenGL.

## When to use it

Use a frame buffer whenever an image is drawn one pixel or one primitive at a time and then shown or saved: in a software renderer, an emulator, a paint program, a plotting library or a window system. It gives constant-time access to each pixel and a layout that the display reads in order. For an image that only goes to a file, the same layout is a [digital image](/digital-image/) in memory. For drawings with few shapes on a large area, a list of shapes that a renderer draws again at each frame uses less memory.

## Pitfalls

- **The pitch is not $WC$.** Writing line L2 as $a \leftarrow (jW + i)C$ is wrong when the rows are padded: the image comes out sheared, each row shifted by $j(P - WC)$ bytes. Use $a \leftarrow jP + iC$, with the pitch that the buffer reports.
- **No clip.** Without the test of line L1, a pixel with $i = W$ goes into the pad or into pixel $(0, j + 1)$, a negative $i$ goes into the row above, and $j \ge H$ writes past the end of the buffer.
- **The channel order.** Writing red, green, blue, alpha into a buffer in the order blue, green, red, alpha exchanges red and blue on the screen. Read the format of the buffer before line L3.
- **The origin.** Row 0 is the top in most window systems and in Direct3D, but window coordinates in OpenGL start at the bottom left, so `glReadPixels` returns the bottom row first. Flip the rows when you move an image between the two conventions.
- **Blending encoded values.** The bytes are most often sRGB values. Averaging or [alpha blending](/alpha-blending/) them directly gives colors that are too dark. Convert to linear light first; see [gamma correction](/gamma-correction/).
- **Tearing.** Writing the buffer that the display is reading shows the top of a new frame over the bottom of the old one. Draw into a back buffer and flip at the vertical blank.

## Implementations

## History

Many early computer displays drew lines with a moving beam, and the computer had to send the picture again for each refresh. A. Michael Noll described in 1971 a scanned display, like a television, whose picture was computed point by point and stored in the memory of a computer. Richard Shoup built the SuperPaint system with a frame buffer and a paint program at Xerox PARC in 1973, and in his 2001 account he notes that it was not the first frame buffer. As memory became cheaper, frame buffers became the normal display of workstations and personal computers, and GPUs today render into frame buffers in their own memory.

## References
