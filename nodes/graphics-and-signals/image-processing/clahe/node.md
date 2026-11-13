---
tag: KNVCNG
kind: algorithm
slug: clahe
name: Contrast-limited adaptive histogram equalization
aliases:
- CLAHE
- adaptive histogram equalization
area: graphics-and-signals/image-processing
level: advanced
summary: Equalize each tile of the image with a clip limit on its histogram, then blend the tile tables bilinearly at each pixel.
solves: [contrast-enhancement]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, L: the number of gray levels, t: the number of tiles}
  time: {worst: Θ(W H + t L), average: Θ(W H + t L), best: Θ(W H + t L)}
  space: {extra: Θ(t L)}
properties: {deterministic: true, exact: true, point_operation: false, monotone: true, local: true}
history:
  year: 1987
  people: [Stephen M. Pizer, E. Philip Amburn, John D. Austin, Robert Cromartie, Ari Geselowitz, Trey Greer, Bart ter Haar Romeny, John B. Zimmerman, Karel Zuiderveld]
  note: Pizer and coauthors described interpolated and clipped adaptive equalization in 1987; Zuiderveld published the widely used C code in Graphics Gems IV in 1994.
prereqs: [histogram-equalization, bilinear-interpolation]
see_also: [contrast-enhancement, contrast-stretching, image-histogram, sliding-window-median, unsharp-masking, color-spaces, image-noise]
sources:
  - paper: doi:10.1016/S0734-189X(87)80186-X
    title: Stephen M. Pizer, E. Philip Amburn, John D. Austin, Robert Cromartie, Ari Geselowitz, Trey Greer, Bart ter Haar Romeny, John B. Zimmerman and Karel Zuiderveld, Adaptive histogram equalization and its variations, Computer Vision, Graphics, and Image Processing 39(3), 1987
    locator: pages 355 to 368 (adaptive equalization, interpolation between contextual regions, and the clipped, contrast-limited form)
  - book: isbn:9780123361554
    title: Karel Zuiderveld, Contrast Limited Adaptive Histogram Equalization, in Paul S. Heckbert (editor), Graphics Gems IV, Academic Press, 1994
    locator: pages 474 to 485 (the method, the clip limit and the C code)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.3, Local Histogram Processing, page 173
  - url: https://github.com/opencv/opencv/blob/4.x/modules/imgproc/src/clahe.cpp
    title: OpenCV, the CLAHE implementation in modules/imgproc/src/clahe.cpp
    locator: the clip limit scaled by tile size over histogram size, the one-pass redistribution, and the interpolation at tile centers
---

Contrast-limited adaptive histogram equalization (CLAHE) cuts an image into tiles, computes a [histogram equalization](/histogram-equalization/) table for each tile from a histogram whose bins are clipped at a limit, and maps each pixel by a [bilinear](/bilinear-interpolation/) blend of the tables of the four nearest tile centers. The tiles adapt the map to the local gray levels, the clip limit bounds the slope of each table and so the gain on noise, and the blend removes the seams between tiles. It costs $\Theta(WH + tL)$ time for a $W \times H$ image with $L$ levels and $t$ tiles. Global [histogram equalization](/histogram-equalization/) is the case of one tile with no clip.

## In plain words

Global equalization uses one table for the whole picture. If one half of a photo is dark and the other half is bright, one table cannot help both. CLAHE cuts the picture into a grid of tiles and makes a separate table for each tile, so each region gets its own contrast. A tile of almost one gray would get a very steep table, and the faint noise in it would become strong grain. So before making the table, CLAHE cuts the tall bars of the tile's histogram down to a limit and spreads the removed counts over all the bars. That keeps every table from being too steep. Last, a pixel near the border of two tiles should not jump from one table to another, so each pixel mixes the tables of the four nearest tile centers, with more weight for closer centers.

## The problem

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels with integer values in $\{0, \ldots, L-1\}$, one channel, usually gamma encoded as stored. A pixel $(x, y)$ has integer indices and its center at $(x + 1/2, y + 1/2)$. The image is cut into $n_x \times n_y$ tiles of $t_w = W/n_x$ by $t_h = H/n_y$ pixels; $t = n_x n_y$. The parameter $\alpha \ge 1$ is the normalized clip limit: a bin may hold at most $\alpha$ times the mean bin count $t_w t_h / L$. The output is an image of the same size and range in which each pixel is mapped by a monotone function of its value that depends on its position. Near the image border, outside the outermost tile centers, the nearest table is held constant; no pixel outside the image is read. This is a local method for [contrast enhancement](/contrast-enhancement/).

## The algorithm

```pseudo id=main
CLAHE(I, W, H, L, nx, ny, α)                  ▷ tiles of tw = W/nx by th = H/ny pixels
L1  for each tile (a, b) with 0 ≤ a < nx and 0 ≤ b < ny do
L2      h ← the histogram of the pixels of tile (a, b)
L3      β ← max(1, ⌊α · tw · th / L⌋)          ▷ β ← tw · th when α = ∞
L4      E ← Σ_k max(h[k] − β, 0);  h[k] ← min(h[k], β) for each k
L5      q ← ⌊E / L⌋, r ← E mod L;  h[k] ← h[k] + q for each k
L6      for m ← 0 to r − 1 do h[⌊mL / r⌋] ← h[⌊mL / r⌋] + 1
L7      T_ab ← the equalization table of h     ▷ lines L4 to L7 of histogram equalization
L8  for each pixel (x, y) do
L9      v ← (y + 1/2)/th − 1/2;  b0 ← clamp(⌊v⌋), b1 ← clamp(⌊v⌋ + 1), t ← v − ⌊v⌋
L10     u ← (x + 1/2)/tw − 1/2;  a0 ← clamp(⌊u⌋), a1 ← clamp(⌊u⌋ + 1), s ← u − ⌊u⌋
L11     g ← I(x, y)
L12     O(x, y) ← round((1−s)(1−t) T_a0b0[g] + s(1−t) T_a1b0[g] + (1−s)t T_a0b1[g] + st T_a1b1[g])
L13 return O
```

Lines L4 to L6 clip the histogram and give the excess $E$ back: $q$ counts to every bin, and one more count to $r$ bins spread evenly over the range. Line L7 is the table of global equalization, $T[k] = \operatorname{round}((L-1)c(k)/(t_w t_h))$, for the clipped histogram. In lines L9 and L10, the tile $(a, b)$ has its center at tile coordinates $(a, b)$, and clamp maps an index into $0 \ldots n_x - 1$ (for $a$) or $0 \ldots n_y - 1$ (for $b$). Line L12 rounds halves up. All quantities are rational with denominators $2t_w$ and $2t_h$, so the implementation does lines L9 to L12 in exact integers.

## Example

Take $L = 8$, an $8 \times 4$ image, $n_x = 2$ and $n_y = 1$, so each tile is $4 \times 4$ with 16 pixels, and $\alpha = 2$, so $\beta = \lfloor 2 \cdot 16/8 \rfloor = 4$:

$$I = \begin{pmatrix} 1 & 1 & 1 & 2 & 4 & 5 & 5 & 6 \\ 1 & 1 & 2 & 2 & 5 & 5 & 6 & 6 \\ 1 & 1 & 1 & 3 & 4 & 5 & 6 & 7 \\ 1 & 1 & 2 & 1 & 5 & 5 & 6 & 6 \end{pmatrix}.$$

| | tile 0 (left) | tile 1 (right) |
|---|---|---|
| histogram $h$ | 0 11 4 1 0 0 0 0 | 0 0 0 0 2 7 6 1 |
| excess $E$ over $\beta = 4$ | 7, so $q = 0$, $r = 7$ | 5, so $q = 0$, $r = 5$ |
| clipped and refilled | 1 5 5 2 1 1 1 0 | 1 1 0 1 3 4 5 1 |
| table with no clip | 0 5 7 7 7 7 7 7 | 0 0 0 0 1 4 7 7 |
| table $T$ with clip | 0 3 5 6 6 7 7 7 | 0 1 1 1 3 4 7 7 |

In tile 0, level 1 holds 11 of the 16 pixels. With no clip its table jumps from 0 to 5 at level 1. The clip lowers that bin to 4, spreads 7 counts over the bins 0 to 6, and the jump becomes 3. In tile 1, level 4 goes to 1 with no clip and to 3 with the clip.

For row 0, $v < 0$, so only the tile row 0 is used. The column coordinate is $u = (x + 1/2)/4 - 1/2$:

| $x$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 |
|---|---|---|---|---|---|---|---|---|
| $u$ | −0.375 | −0.125 | 0.125 | 0.375 | 0.625 | 0.875 | 1.125 | 1.375 |
| $(a_0, a_1, s)$ | (0, 0, ·) | (0, 0, ·) | (0, 1, 1/8) | (0, 1, 3/8) | (0, 1, 5/8) | (0, 1, 7/8) | (1, 1, ·) | (1, 1, ·) |
| $g$ | 1 | 1 | 1 | 2 | 4 | 5 | 5 | 6 |
| blend | 3 | 3 | 2.75 | 3.5 | 4.125 | 4.375 | 4 | 7 |
| $O$ | 3 | 3 | 3 | 4 | 4 | 4 | 4 | 7 |

At $x = 3$ the value is $(5/8) \cdot T_0[2] + (3/8) \cdot T_1[2] = (5/8) \cdot 5 + (3/8) \cdot 1 = 3.5$, which rounds to 4. The full output is

$$O = \begin{pmatrix} 3 & 3 & 3 & 4 & 4 & 4 & 4 & 7 \\ 3 & 3 & 5 & 4 & 5 & 4 & 7 & 7 \\ 3 & 3 & 3 & 4 & 4 & 4 & 7 & 7 \\ 3 & 3 & 5 & 2 & 5 & 4 & 7 & 7 \end{pmatrix}.$$

With no clip ($\alpha = \infty$), the dark background of the left tile goes to 5 instead of 3, which is the noise gain that the clip limit prevents. Global equalization of the same image sends level 1 to 2 and level 5 to 5 everywhere.

## Correctness

The proof is below. The clip of lines L4 to L6 keeps the total count of the tile, because the $r$ indices $\lfloor mL/r \rfloor$ are distinct when $r < L$, and it leaves each bin at most $\beta + q + 1$. So each table is a valid equalization table: nondecreasing, in range, with $T[L-1] = L-1$, and with each step less than $(L-1)(\beta + q + 1)/(t_w t_h) + 1$. Lines L9 and L10 give the clamped tent weights of [bilinear interpolation](/bilinear-interpolation/) between tile centers, the four weights of line L12 are nonnegative with sum 1, and so each output is a rounded convex combination of four table values. With one tile and $\beta \ge t_w t_h$, CLAHE is exactly global equalization.

## Complexity

In the [word RAM](/word-ram/):

- Line L2 reads each pixel once over all tiles, and clears $t$ histograms: $\Theta(WH + tL)$ time.
- Lines L3 to L7 take $\Theta(L)$ time per tile, so $\Theta(tL)$ in total.
- Lines L9 and L10 depend only on $y$ and on $x$, so they can be computed once per row and once per column. Line L12 does four table reads and a constant number of arithmetic steps per pixel: $\Theta(WH)$ time.

The total is $\Theta(WH + tL)$ time and $\Theta(tL)$ extra space for the $t$ tables. For an 8-bit image with an $8 \times 8$ grid, the tables hold $64 \cdot 256$ entries, so the cost is close to two passes over the pixels.

Adaptive equalization with a separate window per pixel costs much more. With a $k \times k$ window it needs a histogram per pixel: $O(WHk^2)$ time to build each one directly, or $O(WH(k + L))$ with a running histogram that moves by one column per step (add $k$ pixels, remove $k$ pixels) and then sums the clipped bins up to $g$. The tile grid with interpolation replaces this by $t$ histograms, at the cost of an approximation between the tile centers.

## Properties

- **Monotone at each position.** For a fixed pixel position, the output is a nondecreasing function of the input value, because each table is and the weights do not depend on it. Across positions the map changes, so two pixels with the same value can get different outputs, and the global gray order is not kept.
- **Bounded slope.** Each table rises by less than $(L-1)(\beta + q + 1)/(t_w t_h) + 1$ per level, about $\alpha$ when the excess is small. This is the contrast limit. Global equalization can rise by $L - 1$ in one level.
- **The two ends of the parameter.** With $\alpha = \infty$ there is no clip and the method is adaptive histogram equalization with interpolation. With $\alpha = 1$, $\beta \le t_w t_h / L$, so after the clip and the refill every bin is between $q$ and $\beta + q + 1$ with $q \le t_w t_h / L$. The clipped histogram is then close to flat, each table is close to a straight ramp, and the method changes little.
- **Continuous in position.** Inside the rectangle of tile centers, the value before rounding is a bilinear function of $(u, v)$ in each cell, so it has no jumps at tile borders. Outside the outer centers it uses one or two tables.
- **Count preserving clip.** The clipped histogram still has $t_w t_h$ counts, so the top level of each tile maps to $L - 1$.

## Variants and improvements

- **Plain adaptive histogram equalization (AHE).** No clip. Each pixel uses the table of a window centered on it, or the interpolated tile tables as here. Its main defect is the strong noise gain in flat regions.
- **Redistribution until no bin is above the limit.** The refill of lines L5 and L6 can push a bin up to $\beta + q + 1$. Some implementations cap those bins at $\beta$ and spread the rest again, in several passes, so that every bin ends at or below the limit. OpenCV uses one pass as here, with the remainder at bins spaced $\lfloor L/r \rfloor$ apart.
- **Window per pixel.** Compute the clipped table of a $k \times k$ window around each pixel, with a running histogram. It has no interpolation error and costs much more.
- **Output range and shape.** Zuiderveld's code maps each tile to a given range $[\min, \max]$ instead of $[0, L-1]$. Other versions equalize toward an exponential or a Rayleigh target, as in histogram matching.
- **Color and volume data.** For color, apply CLAHE to a lightness or luma channel, such as $L^*$ of CIELAB or $Y$ of YCbCr (see [color spaces](/color-spaces/)). For 3D medical volumes, use 3D tiles and trilinear interpolation of the tables.

## When to use it

Use CLAHE when the contrast that matters is local: X-ray, CT and MRI slices, microscopy, low-light and hazy photos, and as a step before feature detection on images with uneven light. Choose the tile grid by the size of the structures you want to see, and the clip limit by the noise level: the noisier the data, the smaller $\alpha$. Do not use it when the gray values carry a measurement or when the brightness relation between distant regions matters, because CLAHE changes both. For a global change with no parameters, use [histogram equalization](/histogram-equalization/), and for a linear change, use [contrast stretching](/contrast-stretching/).

## Pitfalls

- **Tile corners instead of tile centers.** Writing line L10 as $u \leftarrow x/t_w$ blends the tables as if each table belonged to the corner of its tile, so the result is shifted by half a tile and seams appear. Line L10 subtracts $1/2$ so that tile $a$ has its center at $u = a$. OpenCV writes $u = x/t_w - 1/2$, which uses the pixel index instead of the pixel center and shifts the blend by half a pixel; results from the two conventions differ slightly.
- **Losing the remainder of the excess.** Adding only $q$ to each bin at line L5 and skipping line L6 drops $r$ counts. The table then ends below $L - 1$ and the tile cannot reach white. Line L6 gives back the last $r$ counts at distinct bins.
- **A clip limit in raw counts.** Using $\alpha$ itself as $\beta$ at line L3 makes the effect depend on the tile size: the same number clips hard on large tiles and not at all on small ones. Line L3 scales $\alpha$ by the mean bin count $t_w t_h / L$.
- **Equalizing each color channel.** Running CLAHE on R, G and B separately gives each channel a different table, so gray pixels become colored. Apply it to one lightness channel.
- **An image size that is not a multiple of the grid.** The tiles at the right and bottom then have fewer pixels, and line L3 must use the size of each tile. The implementation here refuses such an image; others pad it by mirroring first.

## Implementations

## History

Adaptive histogram equalization came from medical imaging. Pizer, Amburn, Austin, Cromartie, Geselowitz, Greer, ter Haar Romeny, Zimmerman and Zuiderveld described it in 1987 with the two ideas of this page: bilinear interpolation of the tables of a grid of contextual regions, and a clip of each regional histogram that limits the contrast gain. So the clip and the interpolation are both in the 1987 paper. Karel Zuiderveld published a compact C implementation in Graphics Gems IV in 1994, with tiles, a normalized clip limit and interpolation at the tile centers. Most later implementations, such as the one in OpenCV, follow that structure.

## References
