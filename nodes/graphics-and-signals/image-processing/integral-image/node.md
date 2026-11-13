---
tag: 863FHC
kind: data-structure
slug: integral-image
name: Integral image
aliases:
- summed-area table
area: graphics-and-signals/image-processing
level: advanced
summary: The table of sums of the top-left rectangles of an image. It gives the sum and the mean over any axis-aligned rectangle in constant time, so box filters of any size cost O(1) per pixel.
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {build: Θ(W H), query: Θ(1)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, static: true, exact: true}
history:
  year: 1984
  people: [Franklin C. Crow]
  note: Crow introduced the summed-area table to filter textures over rectangles of any size. Viola and Jones (2001) named it the integral image and used it for their rectangle features.
prereqs: [two-dimensional-prefix-sums, digital-image]
see_also: [range-sum-query-2d, box-blur, haar-features, viola-jones-detector, guided-filter, non-local-means, normalized-cross-correlation, mipmap]
sources:
  - paper: doi:10.1145/800031.808600
    title: Franklin C. Crow, Summed-area tables for texture mapping, SIGGRAPH 1984, Computer Graphics 18(3), 207 to 212
    locator: the whole paper (the table, the sum over a rectangle from four entries, and the use for texture filtering)
  - paper: doi:10.1109/CVPR.2001.990517
    title: Paul Viola and Michael Jones, Rapid object detection using a boosted cascade of simple features, CVPR 2001
    locator: Section 2.1, Integral Image (one pass with a cumulative row sum, and the rectangle sum from four array references)
  - paper: "Paul Viola and Michael J. Jones, Robust real-time face detection, International Journal of Computer Vision 57(2), 137 to 154, 2004"
    locator: the section on the integral image
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering (summed area tables)
---

An integral image of a gray image $f$ with $W$ columns and $H$ rows is the table $S$ of $(H+1) \times (W+1)$ numbers with $S[y][x] = \sum_{j < y} \sum_{i < x} f[j][i]$, the sum of the pixels above and to the left of the grid corner $(x, y)$. One pass over the image builds it, and then the sum of the pixels in any axis-aligned rectangle is $S[y_1][x_1] - S[y_0][x_1] - S[y_1][x_0] + S[y_0][x_0]$, three additions for any rectangle size. It is the [two-dimensional prefix sum](/two-dimensional-prefix-sums/) of the image, the answer to the static [2D range sum query](/range-sum-query-2d/), seen as a tool of image processing. Its main use is the mean over a window of any size in constant time: [box filters](/box-blur/) whose radius changes from pixel to pixel, the rectangle [Haar features](/haar-features/) of the [Viola-Jones detector](/viola-jones-detector/), local means and variances, and the fast forms of the [guided filter](/guided-filter/) and [non-local means](/non-local-means/).

## In plain words

Make a second picture of the same size, where each cell holds the total brightness of all the pixels above it and to its left. Filling it takes one sweep: keep a running total along the current row, and add the cell just above.

To get the total brightness of any rectangle, read four cells at its corners. Take the big corner region that ends at the bottom right corner of the rectangle, cut away the region above the rectangle and the region to its left, and add back the small corner region that was cut away twice. Four reads give the total for a rectangle of four pixels or of four million. Divide by the number of pixels, and you have the mean brightness of the rectangle.

## The abstract type

The integral image is a static structure over one image $f$. It supports:

- **BUILD(f)** makes the table.
- **RECT-SUM$(x_0, y_0, x_1, y_1)$** returns $\sum_{y_0 \le y < y_1} \sum_{x_0 \le x < x_1} f[y][x]$ for $0 \le x_0 \le x_1 \le W$ and $0 \le y_0 \le y_1 \le H$. The rectangle is half-open, so an empty rectangle has the sum $0$.
- **BOX-MEAN$(x, y, r)$** returns the mean over the $(2r+1) \times (2r+1)$ window centered at the pixel $(x, y)$, cut at the image border.

An update of one pixel changes $\Theta(WH)$ entries in the worst case, so the structure is for images that do not change between queries. A [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) supports updates at a cost of $O(\log W \log H)$ per operation.

## Representation

The table has one row and one column more than the image. Row $0$ and column $0$ are zero, which removes the special cases at the top and left borders. Entry $S[y][x]$ sits at the grid corner between pixels, not at a pixel center: with pixel centers at the integers, it is the sum over the quarter plane up to the corner $(x - 1/2, y - 1/2)$. For pixels of $b$ bits the entries reach $WH(2^b - 1)$, so they need about $b + \log_2(WH)$ bits; a $4096 \times 4096$ image of 8-bit pixels needs 32-bit entries. Unsigned machine words that wrap around still give exact rectangle sums whenever the true sum fits in the word, because the wrap is arithmetic modulo $2^{32}$. The page on [two-dimensional prefix sums](/two-dimensional-prefix-sums/) treats the overflow and the floating point issues in more detail.

## Operations

```pseudo id=main
BUILD(f, W, H)
L1  S ← an (H + 1) × (W + 1) table of zeros
L2  for y ← 0 to H − 1 do
L3      run ← 0                          ▷ sum of f[y][0 .. x]
L4      for x ← 0 to W − 1 do
L5          run ← run + f[y][x]
L6          S[y + 1][x + 1] ← S[y][x + 1] + run
L7  return S
```

Line L5 keeps the sum of the current row up to column $x$, and line L6 adds it to the entry above, which holds the sum of all the rows above up to the same column. This is the one-pass build of Viola and Jones. It does one addition per pixel fewer than the recurrence $S[y+1][x+1] = f[y][x] + S[y][x+1] + S[y+1][x] - S[y][x]$, and it gives the same table.

```pseudo id=query
RECT-SUM(S, x0, y0, x1, y1)              ▷ the half-open rectangle [x0, x1) × [y0, y1)
L8  return S[y1][x1] − S[y0][x1] − S[y1][x0] + S[y0][x0]

BOX-MEAN(S, x, y, r)                     ▷ the window is cut at the image border
L9  x0 ← max(0, x − r), x1 ← min(W, x + r + 1), y0 ← max(0, y − r), y1 ← min(H, y + r + 1)
L10 return RECT-SUM(S, x0, y0, x1, y1) / ((x1 − x0)(y1 − y0))
```

Line L8 is inclusion and exclusion over four quarter planes. Line L9 cuts the window at the border, and line L10 divides by the number of pixels that are really in the window, so a constant image has a constant mean up to the border. This border rule, the window cut and renormalized, is the natural one for an integral image; the clamp or mirror rules need a padded image or extra terms.

Two tables, one of $f$ and one of $f^2$, give the local variance: $\mathrm{BOX\text{-}MEAN}_{f^2} - (\mathrm{BOX\text{-}MEAN}_f)^2$. Tables of products $f g$ give local covariances in the same way, which is how the guided filter gets its coefficients.

## Example

Take the $4 \times 3$ image

| | $x = 0$ | 1 | 2 | 3 |
|---|---|---|---|---|
| $y = 0$ | 3 | 1 | 4 | 1 |
| $y = 1$ | 5 | 9 | 2 | 6 |
| $y = 2$ | 5 | 3 | 5 | 8 |

BUILD fills the table row by row. For the image row $y = 1$, the running row sums of line L5 are $5, 14, 16, 22$, and line L6 adds them to the row above:

| table row | $x = 0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $S[0]$ | 0 | 0 | 0 | 0 | 0 |
| $S[1]$ | 0 | 3 | 4 | 8 | 9 |
| $S[2]$ | 0 | 8 | 18 | 24 | 31 |
| $S[3]$ | 0 | 13 | 26 | 37 | 52 |

The entry $S[3][4] = 52$ is the sum of the whole image. The sum over the rectangle $1 \le x < 3$, $1 \le y < 3$, the pixels $9, 2, 3, 5$, is $S[3][3] - S[1][3] - S[3][1] + S[1][1] = 37 - 8 - 13 + 3 = 19$. The box mean at $(1, 1)$ with $r = 1$ covers the $3 \times 3$ block in the top-left corner, $37 / 9$. The box mean at the corner pixel $(0, 0)$ with $r = 1$ is cut to the $2 \times 2$ block, $S[2][2] / 4 = 18 / 4$.

## Correctness

BUILD keeps two invariants. Inside a row, after line L5, $\mathrm{run}$ is the sum $f[y][0] + \dots + f[y][x]$. Across rows, row $y + 1$ of the table is the sum of the image rows $0$ to $y$ up to each column, because line L6 adds the prefix of row $y$ to the entry above. RECT-SUM is correct because the four quarter planes cover the rectangle once and every other pixel either zero times or once with each sign. BOX-MEAN is RECT-SUM over the cut window divided by its size. The full proof is below.

## Complexity

- **BUILD.** Two additions per pixel and the zero border, $\Theta(WH)$ time.
- **RECT-SUM and BOX-MEAN.** Three additions, at most one division and a few comparisons, $\Theta(1)$ for any rectangle.
- **Space.** $(W+1)(H+1)$ entries, each with $\log_2(WH)$ more bits than a pixel.
- **A box filter of any radius.** $WH$ calls of BOX-MEAN, so $\Theta(WH)$ in total, against $\Theta(WH r^2)$ for the direct sum.

## Variants

- **Running sums without a table.** For one fixed radius, the [box blur](/box-blur/) by running sums needs only one intermediate image of window sums and has the same cost.
- **Squares and products.** Tables of $f^2$ and of $f g$ give local variances and covariances in $O(1)$ per window. These drive the [guided filter](/guided-filter/), the normalization of [normalized cross-correlation](/normalized-cross-correlation/), and local thresholding.
- **Per-offset tables.** Fast [non-local means](/non-local-means/) builds one table of squared differences for each search offset, so every patch distance for that offset costs $O(1)$.
- **Rotated tables.** A table summed along diagonals gives the sums of rectangles turned by 45 degrees. See [two-dimensional prefix sums](/two-dimensional-prefix-sums/).
- **Repeated integration.** Integrating twice or more gives piecewise polynomial kernels, the continuous form of repeated boxes, and an approximation of the Gaussian.
- **Texture filtering.** Crow's original use filters a texture over the bounding rectangle of the pixel footprint; the [mipmap](/mipmap/) became the standard method for that, at a third more memory in place of wider entries.

## When to use it

Use an integral image when you need many rectangle sums or means of varying sizes on the same image: Haar features at many scales, a box filter whose radius depends on the pixel, local statistics for adaptive thresholding, or the windows of the guided filter. For one box blur of a fixed radius, two passes of running sums cost the same and need narrower words. For an image that changes between queries, use a Fenwick tree in 2D.

## Pitfalls

- **Off by one in the corners.** Reading $S[y_1 - 1][x_1 - 1]$ at line L8, as if the table were indexed by pixels, drops the last row and column of the rectangle. With the extra zero row and column, the corners of the half-open rectangle $[x_0, x_1) \times [y_0, y_1)$ are the indices $x_0, x_1, y_0, y_1$ themselves.
- **The wrong count at the border.** Dividing by $(2r+1)^2$ at line L10 for a window cut at the border darkens the border pixels. Divide by $(x_1 - x_0)(y_1 - y_0)$.
- **Entries that are too narrow.** 16-bit entries overflow once more than 257 pixels of value 255 are summed. Use words of $b + \lceil \log_2(WH) \rceil$ bits, or unsigned wrapping words and rectangles whose sums fit.
- **Variance from floating point tables.** In floating point, $\mathrm{mean}(f^2) - \mathrm{mean}(f)^2$ loses most of its digits when the variance is small compared with the squared mean, and can come out negative. Use integer tables, or subtract the image mean before building the tables, and clip negative results to zero.

## Implementations

## History

Crow (1984) introduced the summed-area table at SIGGRAPH to filter textures over rectangles of any size in constant time. McDonnell (1981) had already described box filtering at a cost that does not depend on the box size. Viola and Jones (2001, 2004) renamed the table the integral image, built it in one pass with a cumulative row sum, and used it to evaluate their rectangle features in constant time, which made real-time face detection possible.

## References
