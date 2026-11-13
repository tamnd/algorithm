---
tag: ES8PJ7
kind: algorithm
slug: box-blur
name: Box blur
aliases:
- box filter
- mean filter
area: graphics-and-signals/image-processing
level: intro
summary: Replace each pixel by the mean over a square window around it. Running sums along the rows and then the columns make the cost per pixel constant for any window size.
solves: [image-smoothing]
model: real-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, r: window radius}
  time: {worst: "Θ(W H + (W + H) r)"}
  space: {extra: Θ(W H)}
properties: {deterministic: true, linear: true, separable: true, exact: true, in_place: false}
history:
  year: 1981
  people: [Mark J. McDonnell]
  note: McDonnell described box filtering at a cost per pixel that does not depend on the size of the box, and its use as a general tool for image processing.
prereqs: [linear-filtering, sliding-window]
see_also: [separable-filter, integral-image, gaussian-filter, moving-average, two-dimensional-prefix-sums, guided-filter, median-filter, sliding-window-maximum]
sources:
  - paper: doi:10.1016/S0146-664X(81)80009-3
    title: Mark J. McDonnell, Box-filtering techniques, Computer Graphics and Image Processing 17(1), 65 to 70, 1981
    locator: the whole paper (box filtering by running sums at a cost that does not depend on the box size)
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.5, Smoothing (Lowpass) Spatial Filters, the subsection Box Filter Kernels
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.2, Linear filtering (the box filter, separable filtering and running sums)
  - paper: doi:10.1109/TPAMI.1986.4767776
    title: William M. Wells, Efficient synthesis of Gaussian filters by cascaded uniform filters, IEEE Transactions on Pattern Analysis and Machine Intelligence 8(2), 234 to 239, 1986
    locator: the whole paper (repeated box filters as an approximation of the Gaussian)
---

The box blur replaces each pixel of an image by the mean of the $(2r+1) \times (2r+1)$ pixels around it. It is the [linear filter](/linear-filtering/) whose kernel has the same weight $1/(2r+1)^2$ at every position. Done directly it costs $(2r+1)^2$ additions per pixel. The box kernel is [separable](/separable-filter/), and along one row the window sum changes by one pixel in and one pixel out when the window moves one step. So a horizontal pass and a vertical pass of running sums give every window sum with about four additions per pixel, whatever the radius, in $\Theta(WH + (W+H)r)$ time. It is the fastest way to [smooth an image](/image-smoothing/), and it is the building block of the [integral image](/integral-image/), the [guided filter](/guided-filter/) and the repeated-box approximation of the [Gaussian filter](/gaussian-filter/).

## In plain words

Put a small square window over the image, centered on one pixel. Add up the values of all the pixels under the window and divide by their number. That average is the new value of the center pixel. Do this for every pixel.

A slow program adds up the whole window again for each pixel. A fast program notices that when the window moves one pixel to the right, only one column leaves it and one column enters it. So it keeps a running total, adds the entering value, and takes away the leaving value. It first does this along each row, then along each column of the result. The work per pixel is then the same for a tiny window and for a huge one.

## The problem

The input is a gray image $f$ with $W$ columns and $H$ rows, $f[y][x]$ for $0 \le x < W$ and $0 \le y < H$, with the pixel centers at the integer points, a radius $r \ge 0$, and a border rule. A pixel is a point sample, not a little square. The border rule extends each axis beyond the image: for an index $i$ of an axis of length $n$, $\mathrm{ext}(i, n)$ is the nearest index inside (clamp), the reflected index with the edge pixel repeated, so that $-1 \mapsto 0$ (mirror), $i \bmod n$ (wrap), or no pixel at all, read as $0$ (zero). The extended image is $\tilde f(i, j) = f[\mathrm{ext}(j, H)][\mathrm{ext}(i, W)]$. The output is

$$h(x, y) = \frac{1}{(2r+1)^2} \sum_{v=-r}^{r} \sum_{u=-r}^{r} \tilde f(x+u, y+v).$$

The values are numbers in a linear scale. For an 8-bit image stored with the sRGB curve, decode to linear values first, or accept that the blur is done on the encoded values.

## The algorithm

```pseudo id=main
BOX-BLUR(f, W, H, r)                       ▷ ext is the border rule of each axis
L1  for y ← 0 to H − 1 do                  ▷ horizontal pass
L2      s ← Σ_{u = −r}^{r} f[y][ext(u, W)]
L3      g[y][0] ← s
L4      for x ← 1 to W − 1 do
L5          s ← s + f[y][ext(x + r, W)] − f[y][ext(x − r − 1, W)]
L6          g[y][x] ← s
L7  for x ← 0 to W − 1 do                  ▷ vertical pass on g
L8      s ← Σ_{v = −r}^{r} g[ext(v, H)][x]
L9      h[0][x] ← s
L10     for y ← 1 to H − 1 do
L11         s ← s + g[ext(y + r, H)][x] − g[ext(y − r − 1, H)][x]
L12         h[y][x] ← s
L13 return h / (2r + 1)²
```

A term with no pixel under the zero rule counts as $0$. Lines L1 to L6 make $g[y][x]$, the sum of the $2r+1$ extended pixels of row $y$ centered at $x$. Line L2 sums the first window directly. Line L5 moves the window one step: the window of $x$ is the window of $x - 1$ without the index $x - r - 1$ and with the index $x + r$. Lines L7 to L12 do the same along the columns of $g$, so $h[y][x]$ is a sum of $2r+1$ row sums, the sum over the whole square. Line L13 divides once, at the end. With integer pixels the sums at lines L5 and L11 are exact, and the only rounding is the final division.

## Example

Take $W = 5$, $H = 3$, $r = 1$ and the clamp rule, with the image

| | $x = 0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| $y = 0$ | 10 | 10 | 10 | 80 | 80 |
| $y = 1$ | 10 | 10 | 90 | 80 | 80 |
| $y = 2$ | 10 | 10 | 10 | 80 | 80 |

The horizontal pass on row 1, with $\mathrm{ext}(-1) = 0$ and $\mathrm{ext}(5) = 4$:

| step | line | enters | leaves | $s = g[1][x]$ |
|---|---|---|---|---|
| $x = 0$ | L2 | $10 + 10 + 10$ | | 30 |
| $x = 1$ | L5 | $f[2] = 90$ | $f[0] = 10$ | 110 |
| $x = 2$ | L5 | $f[3] = 80$ | $f[0] = 10$ | 180 |
| $x = 3$ | L5 | $f[4] = 80$ | $f[1] = 10$ | 250 |
| $x = 4$ | L5 | $f[4] = 80$ | $f[2] = 90$ | 240 |

Rows 0 and 2 give $g = 30, 30, 100, 170, 240$. The vertical pass adds three row sums at each column; for row 1 these are rows 0, 1 and 2, and for row 0 they are rows 0, 0 and 1 by the clamp. In this image every row of $h$ is the same:

| | $x = 0$ | 1 | 2 | 3 | 4 |
|---|---|---|---|---|---|
| window sum | 90 | 170 | 380 | 590 | 720 |
| mean $h$ | 10 | 18.9 | 42.2 | 65.6 | 80 |

The single bright pixel 90 is spread over its neighbors, and the step from 10 to 80 becomes a ramp three pixels wide. With the zero rule the sums of row 0 are $40, 140, 280, 420, 320$ instead: the missing pixels count as black, and the corners grow dark.

## Correctness

The horizontal pass keeps the invariant $s = \sum_{u=-r}^{r} f[y][\mathrm{ext}(x+u, W)]$ at line L6, by induction on $x$: line L2 sets it for $x = 0$, and line L5 removes the one index that leaves the window and adds the one that enters it. The vertical pass keeps the same invariant on the columns of $g$. Because the extension is applied to each axis on its own, the extended value of $g$ at a row outside the image is the row sum of the extended row, and the two sums together are the double sum of the problem. The full proof is below.

## Complexity

- **Time.** Line L2 costs $2r+1$ additions per row and line L8 costs $2r+1$ per column, $\Theta((W + H) r)$ in total. Lines L5 and L11 cost two additions per pixel and per pass, $\Theta(WH)$. The total is $\Theta(WH + (W+H)r)$ in the real-RAM model, which is $\Theta(WH)$ when $r \le \max(W, H)$. Direct filtering costs $\Theta(WH r^2)$, and separable filtering with general weights $\Theta(WH r)$.
- **Space.** The intermediate image $g$ takes $WH$ values, and the output another $WH$. One row or one column of extra storage suffices if the passes write in place with a small buffer.
- **Word size.** With pixels in $[0, 2^b)$ the sums are below $(2r+1)^2 2^b$, so an unsigned 32-bit integer holds them for 8-bit pixels and any radius up to 2000.

## Properties

- **Linear and shift invariant** under the wrap rule, and away from the border under every rule.
- **Exact.** Integer inputs give exact integer sums. The output equals direct 2D filtering with the same border rule.
- **Keeps the mean level.** A constant image stays constant under clamp, mirror and wrap, because the weights sum to 1. Under the zero rule the border pixels grow darker.
- **Poor low-pass response.** The frequency response of the 1D box is $\sin((2r+1)\pi\omega) / ((2r+1) \sin(\pi \omega))$ at the frequency $\omega$ in cycles per pixel. It has zeros and negative lobes, so some fine patterns are kept with their sign inverted. The square window is also not rotation invariant.

## Variants and improvements

- **Integral image.** An [integral image](/integral-image/) gives the sum over any rectangle in four lookups, so the radius can change from pixel to pixel, and the window can be cut at the border with the right pixel count.
- **Repeated boxes.** Two box passes give a triangle kernel, and $n$ passes give a kernel whose shape tends to the Gaussian by the [central limit theorem](/central-limit-theorem/). Three passes are a common fast [Gaussian filter](/gaussian-filter/) (Wells 1986).
- **Normalized box at the border.** Divide each sum by the number of pixels that lie inside the image in place of $(2r+1)^2$. This is the mean over the cut window, and it is the form used by the guided filter.
- **Rectangles and other shapes.** Different radii along $x$ and $y$ are free. Other shapes, such as diamonds and hexagons, are sums of a few running sums along other directions.
- **Order statistics.** The same running window gives the running minimum and maximum, by the [sliding window maximum](/sliding-window-maximum/) method, and the running median, a nonlinear [median filter](/median-filter/), with a histogram that is updated by one column at a time.

## When to use it

Use the box blur when speed matters more than the shape of the blur: for a quick preview, for local means in thresholding and in statistics such as the local variance, and as a step in the guided filter. Use the [Gaussian filter](/gaussian-filter/), or three repeated boxes, when the result is shown to people or fed to an edge or feature detector, because the box kernel makes square artifacts and passes some high frequencies with the wrong sign. Use an [edge preserving filter](/bilateral-filter/) when edges must stay sharp.

## Pitfalls

- **Rounding between the passes.** Storing $g$ at line L6 as 8-bit values rounded after a division loses precision twice. Keep $g$ as exact sums, and divide once at line L13.
- **Floating point drift.** In floating point, line L5 adds and subtracts the same value at different times, and the rounding errors add up along a long row. Use integer sums, or restart the sum from line L2 every few hundred pixels, or use [compensated summation](/kahan-summation/).
- **Off by one in the leaving index.** Subtracting $f[y][\mathrm{ext}(x - r)]$ at line L5 gives a window of $2r$ pixels that drifts to the right. The pixel that leaves is $x - r - 1$.
- **The wrong count at the border.** With the zero rule, dividing by $(2r+1)^2$ at line L13 darkens the border. Divide by the number of pixels inside the image, or use clamp or mirror.
- **Repeated boxes at the border.** Running the box blur $n$ times with the clamp rule is not one filter with the $n$-fold kernel and the clamp rule: each pass applies the rule again to an image that is already blurred. The two agree only at a distance of at least $nr$ from the border, and agree everywhere only under the wrap rule.

## Implementations

## History

Moving averages are much older than digital images. For images, McDonnell (1981) described box filtering at a cost per pixel independent of the box size, and its extensions as a general tool. Crow (1984) introduced the summed-area table for filtering textures with rectangles of any size, and Wells (1986) used cascades of box filters to approximate Gaussian filters.

## References
