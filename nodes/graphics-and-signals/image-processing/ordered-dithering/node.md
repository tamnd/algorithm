---
tag: ZXEC5M
kind: algorithm
slug: ordered-dithering
name: Ordered dithering
aliases:
- Bayer dithering
- threshold dithering
- threshold map dithering
area: graphics-and-signals/image-processing
level: advanced
summary: Compare each pixel with a threshold from a small matrix tiled over the image, such as the Bayer matrix, so that a constant gray k/n^2 turns on exactly k pixels of every n by n tile.
solves: [halftoning]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, n: the side of the threshold matrix}
  time: {worst: Θ(W H + n^2), average: Θ(W H + n^2), best: Θ(W H + n^2)}
  space: {extra: Θ(n^2)}
properties: {deterministic: true, exact: false, parallel: true, pointwise: true, in_place: true}
history:
  year: 1973
  people: [Bryce E. Bayer]
  note: Bayer described index matrices of side 2^K for the two-level display of continuous-tone pictures, with the thresholds spread so that the patterns of each level are as fine as possible.
prereqs: [halftoning, image-thresholding]
see_also: [floyd-steinberg-dithering, color-quantization, gamma-correction, digital-image, scalar-quantization, morton-encoding, median-cut, octree-color-quantization]
sources:
  - paper: "Bryce E. Bayer, An optimum method for two-level rendition of continuous-tone pictures, IEEE International Conference on Communications, Conference Record, 1973"
    locator: the whole paper (the dispersed index matrices of side 2^K and the criterion for their order)
  - book: isbn:9780262210096
    title: Robert Ulichney, Digital Halftoning, MIT Press, 1987
    locator: the chapters on ordered dither (the clustered and dispersed dot matrices, the recursive Bayer matrices and their spectra)
  - paper: doi:10.1016/S0146-664X(76)80003-2
    title: J. F. Jarvis, C. N. Judice and W. H. Ninke, A survey of techniques for the display of continuous tone pictures on bilevel displays, Computer Graphics and Image Processing 5(1), 1976, 13 to 40
    locator: the section on ordered dither, with the dither matrices of side 2, 4 and 8 and their comparison with error diffusion
---

Ordered dithering turns a gray image into black and white pixels by comparing each pixel with a threshold that depends only on its position. The thresholds come from a small $n \times n$ matrix, tiled over the image like a pattern of floor tiles. If the matrix holds each of the values $0, 1, \ldots, n^2 - 1$ once, and the threshold of the value $m$ is $(m + 1/2)/n^2$, then a constant gray $k/n^2$ turns on exactly $k$ pixels of every tile, so the mean brightness is right at every tile. The *Bayer matrix* orders the values so that each such pattern is spread out as evenly as possible. Each pixel is decided on its own, so the method is fully parallel, unlike [Floyd-Steinberg dithering](/floyd-steinberg-dithering/), and it solves the [halftoning](/halftoning/) problem with a regular, visible texture.

## In plain words

Draw a small grid of numbers, say 4 by 4, holding each number from 0 to 15 once. Lay copies of it over the whole image like tiles. For each pixel, look at the number under it. A dark pixel turns white only where the number is small, and a light pixel turns white even where the number is large. So a gray that is a quarter of white turns on the 4 places with the smallest numbers in every tile, and from a distance the tiles look a quarter bright. The Bayer grid puts the small numbers far apart, so that each gray makes a fine, even dot pattern rather than clumps. Each pixel needs only its own value and its own number, so all pixels can be done at once.

## The problem

The input is a gray [digital image](/digital-image/) $v$ with $H$ rows and $W$ columns of values in $[0, 1]$, linear in light intensity, and the side $n = 2^K$ of the matrix. The output is an image $q$ of zeros and ones whose local mean matches $v$, as on the [halftoning](/halftoning/) page. Ordered dithering restricts the answer to the form $q(x, y) = [\, v(x, y) > T(x \bmod n,\ y \bmod n) \,]$ for a fixed threshold matrix $T$.

## The algorithm

```pseudo id=main
ORDERED-DITHER(v, n)                                    ▷ n = 2^K
L1  M ← (0);  s ← 1                                     ▷ the 1 × 1 matrix
L2  while s < n do
L3      M′(x, y) ← 4 M(x mod s, y mod s) + D(⌊x/s⌋, ⌊y/s⌋) for 0 ≤ x, y < 2s;  M ← M′;  s ← 2s
L4  T(x, y) ← (M(x, y) + 1/2) / n²
L5  for each pixel (x, y) do
L6      q(x, y) ← 1 if v(x, y) > T(x mod n, y mod n) else 0
L7  return q
```

Here $D(0, 0) = 0$, $D(1, 0) = 2$, $D(0, 1) = 3$ and $D(1, 1) = 1$, with the first argument the column. Line L3 is the block recursion, with rows written from top to bottom

$$
M_{2s} = \begin{pmatrix} 4 M_s & 4 M_s + 2 \\ 4 M_s + 3 & 4 M_s + 1 \end{pmatrix},
\qquad
M_2 = \begin{pmatrix} 0 & 2 \\ 3 & 1 \end{pmatrix},
\qquad
M_4 = \begin{pmatrix} 0 & 8 & 2 & 10 \\ 12 & 4 & 14 & 6 \\ 3 & 11 & 1 & 9 \\ 15 & 7 & 13 & 5 \end{pmatrix}.
$$

The same matrix has a closed form: with $x_i$ and $y_i$ the binary digits of $x$ and $y$, the base-4 digits of $M(x, y)$ from the most significant down are $2(x_i \oplus y_i) + y_i$ for $i = 0, 1, \ldots, K - 1$, so the lowest digits of the coordinates decide the highest digit of the index, as in a bit-reversed [Morton code](/morton-encoding/). The matrix is built once; lines L5 and L6 are one comparison per pixel.

## Example

**Gray 5/16 with the 4 by 4 matrix.** The thresholds are $(m + 1/2)/16$, and $5/16 > (m + 1/2)/16$ exactly when $m \le 4$. The values 0 to 4 of $M_4$ sit at $(0, 0)$, $(2, 2)$, $(2, 0)$, $(0, 2)$ and $(1, 1)$, so every tile is

$$
\begin{pmatrix} 1 & 0 & 1 & 0 \\ 0 & 1 & 0 & 0 \\ 1 & 0 & 1 & 0 \\ 0 & 0 & 0 & 0 \end{pmatrix},
$$

with 5 ones of 16. The first four ones form the lattice of even coordinates, and the fifth is in the middle of a gap.

**Other levels.** Gray $1/2$ gives a checkerboard. Gray $1/4$ gives the pixels with both coordinates even, and gray $1/16$ gives one pixel per tile. A gray of $0.3$ with $n = 4$ turns on the indices below $0.3 \cdot 16 - 1/2 = 4.3$, so again 5 of 16, which is $4.8$ rounded to the nearest integer.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts. First, the recursion of line L3 gives a matrix that holds each of $0, \ldots, n^2 - 1$ exactly once, and it equals the closed form by digits. Second, for any gray $g \in [0, 1]$, every aligned tile has exactly $\#\{m \in [0, n^2) : m < g n^2 - 1/2\}$ ones, which is within $1/2$ of $g n^2$ and equals $k$ when $g = k/n^2$. Third, the pattern of each level contains the pattern of every lower level. Fourth, for $j \le K$, the indices below $n^2 / 4^j$ are exactly the pixels whose two coordinates are multiples of $2^j$, so each level of the form $4^{-j}$ is a square lattice. The tests check the permutation, the digit formula, the counts per tile and the lattice for $n$ up to 16 in exact fractions.

## Complexity

- **Time.** Building $M$ costs $\Theta(n^2)$, since the sizes $4 + 16 + \cdots + n^2$ add up to less than $\frac{4}{3} n^2$. The loop of lines L5 and L6 costs $\Theta(W H)$ in the [real RAM](/real-ram/), so the total is $\Theta(W H + n^2)$.
- **Space.** The matrix, $\Theta(n^2)$; the output can overwrite the input.
- **Parallel.** No pixel depends on another, so the loop runs in $O(1)$ parallel time on $W H$ processors, in a shader, or in the hardware of a display.

## Properties

- **Exact mean per tile.** A constant gray $k/n^2$ turns on exactly $k$ pixels in every tile, and any gray is off by at most half a pixel per tile.
- **Pointwise.** Each output pixel depends only on its own input and position, so a change of one input pixel changes at most one output pixel, which suits animation and video.
- **Nested patterns.** The pattern of a level contains that of every darker level, which avoids jumps in a smooth ramp.
- **Regular texture.** The patterns repeat with period $n$ and show a cross-hatch texture, and only $n^2 + 1$ distinct mean levels are available.
- **Dispersed dots.** In the Bayer matrix, the levels $4^{-j}$ form square lattices, and the other levels fill the gaps between them evenly.

## Variants and improvements

- **Clustered-dot matrices.** Order the thresholds in a spiral from the center of the tile, so that the ones form round dots that grow with the gray. Printers use them because isolated pixels do not print reliably.
- **Several output levels.** For $L + 1$ levels, scale the value to $[0, L]$, keep the integer part, and use the matrix to round the fractional part up or down.
- **Color.** Dither each channel with the same or with shifted matrices, or add the threshold offset to the color before a nearest-color search in a palette from [color quantization](/color-quantization/).
- **Blue noise masks.** A large matrix with no regular period, such as Ulichney's void-and-cluster array, gives the fine texture of error diffusion with the parallel decision of ordered dithering.
- **Error diffusion.** For still images where the regular texture is a problem, [Floyd-Steinberg dithering](/floyd-steinberg-dithering/) gives irregular patterns at the cost of a sequential scan.

## When to use it

Use ordered dithering when each pixel must be decided on its own: in a shader, in display hardware, for video and animation where error diffusion flickers, or when an image is dithered in tiles. It also suits images with large flat areas of a few levels, such as user interfaces. Use clustered-dot matrices for printers, and [error diffusion](/floyd-steinberg-dithering/) for still photographs on screens where the finer texture matters.

## Pitfalls

- **Gamma.** The thresholds assume values linear in light. Dithering values coded with [gamma correction](/gamma-correction/) shifts every level.
- **Off by one in the thresholds.** A threshold of $(m + 1)/n^2$ with the test $v > T$ turns on $k - 1$ pixels for the gray $k/n^2$ instead of $k$, and never turns on a full tile. A threshold of $m/n^2$ gives $k$ for these grays but rounds every other gray up. The half step in line L4 rounds to the nearest count. A value of exactly a threshold stays off with the strict test.
- **Wrong recursion.** A matrix built in another order, such as the plain row order, is still a permutation but makes lines and clumps instead of dispersed dots.
- **Too few levels.** A matrix of side 2 gives only 5 mean levels, which shows false contours on smooth ramps; side 8 or 16 is usual.
- **Visible tiling.** The period $n$ shows as a grid texture, which is stronger when the image is scaled after dithering. Dither at the output resolution.

## Implementations

## History

Dither matrices for two-level displays were studied in the early 1970s. Bayer in 1973 described the index matrices of side $2^K$ that spread the thresholds as evenly as possible, now called Bayer matrices. Jarvis, Judice and Ninke compared ordered dither with error diffusion in their survey of 1976. Ulichney's book of 1987 analyzed the spectra of the dispersed and clustered matrices, and his void-and-cluster method of 1993 built large threshold arrays with blue noise patterns.

## References
