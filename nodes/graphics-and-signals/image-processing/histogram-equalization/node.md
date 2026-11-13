---
tag: JQ35J4
kind: algorithm
slug: histogram-equalization
name: Histogram equalization
aliases:
- global histogram equalization
area: graphics-and-signals/image-processing
level: intro
summary: Map each gray level through the rounded cumulative histogram, so that the output histogram is close to flat.
solves: [contrast-enhancement]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, L: the number of gray levels}
  time: {worst: Θ(W H + L), average: Θ(W H + L), best: Θ(W H + L)}
  space: {extra: Θ(L)}
properties: {deterministic: true, exact: true, point_operation: true, monotone: true, idempotent: true}
history:
  year: 1977
  people: [Robert A. Hummel]
  note: Hummel described the cumulative histogram map as an automatic enhancement routine in Computer Graphics and Image Processing in 1977.
prereqs: [image-histogram, contrast-enhancement, prefix-sums]
see_also: [clahe, contrast-stretching, gamma-correction, inverse-transform-sampling, shannon-entropy, image-thresholding, counting-sort]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.3, Histogram Processing, pages 147 to 175 (histogram equalization from page 148, histogram matching from page 156, exact histogram matching from page 163)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.1.4, Histogram equalization
  - paper: "Robert A. Hummel, Image enhancement by histogram transformation, Computer Graphics and Image Processing 6(2), 1977"
    locator: pages 184 to 195
---

Histogram equalization is the point operation for [contrast enhancement](/contrast-enhancement/) that maps each gray level $k$ of an image to $\operatorname{round}((L-1)\,c(k)/N)$, where $c(k)$ is the number of pixels with a value of at most $k$, $N$ is the number of pixels and $L$ is the number of levels. It uses the [image histogram](/image-histogram/) and its [prefix sums](/prefix-sums/), so it costs $\Theta(WH + L)$ time for a $W \times H$ image, with no parameter to set. The output histogram is close to flat but in general not flat: the map can merge levels but cannot split one. [CLAHE](/clahe/) applies the same map per tile with a clip limit, and [contrast stretching](/contrast-stretching/) uses a straight line instead of the cumulative histogram.

## In plain words

Sort all the pixels of a gray image from dark to bright. A pixel that is darker than 30 percent of the image should get the gray that is 30 percent of the way from black to white. Histogram equalization gives each pixel exactly that gray. A gray that many pixels share takes up a wide part of the output range, and a gray that few pixels use takes up a narrow part. So the busy part of the range is spread out, and detail in it becomes easier to see. Pixels that had the same gray still have the same gray afterward, so a large patch of one gray cannot be split. That is why the result is only close to even, and why a large flat background can take over the whole output.

## The problem

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels with integer values in $\{0, \ldots, L-1\}$, for example $L = 256$ for 8 bits. One channel is used. The values are taken as they are stored, which for most files means gamma encoded (see [gamma correction](/gamma-correction/)); equalization does not need linear values, because it uses only the order of the levels. The method looks at no neighbors, so the pixel center convention and the border rule do not matter. The output is an image $O$ of the same size and range, with $O = T(I)$ for a nondecreasing table $T$ chosen so that the output levels are used about equally. This is one method for the [contrast enhancement](/contrast-enhancement/) problem.

## The algorithm

```pseudo id=main
HISTOGRAM-EQUALIZATION(I, W, H, L)             ▷ I has values in 0 .. L − 1
L1  N ← W · H
L2  h[0 .. L − 1] ← 0
L3  for each pixel (x, y) do h[I(x, y)] ← h[I(x, y)] + 1
L4  c ← 0
L5  for k ← 0 to L − 1 do
L6      c ← c + h[k]                            ▷ c = c(k), the pixels with value ≤ k
L7      T[k] ← ⌊(2(L − 1)c + N) / (2N)⌋         ▷ round((L − 1)c / N), halves up
L8  for each pixel (x, y) do O(x, y) ← T[I(x, y)]
L9  return O
```

Lines L2 and L3 build the histogram, lines L4 to L6 form its running sum, and line L7 scales it to $0 \ldots L-1$. Line L7 is in integers: $\lfloor (2a + N)/(2N) \rfloor = \lfloor a/N + 1/2 \rfloor$, so the table is exact and the rounding does not depend on floating point. Line L8 is one table lookup per pixel.

The idea comes from probability. If a gray value $X$ has a continuous distribution function $F$, then $F(X)$ is uniform on $[0, 1]$; this is the converse of [inverse transform sampling](/inverse-transform-sampling/). Line L7 is the discrete version, $c(k)/N$ being the empirical $F$. With integer levels the distribution has jumps, and the uniform result holds only up to the size of the largest jump.

## Example

Take $L = 8$ (3 bits) and the $4 \times 4$ image

$$I = \begin{pmatrix} 2 & 3 & 3 & 2 \\ 4 & 2 & 3 & 5 \\ 3 & 3 & 4 & 3 \\ 2 & 4 & 3 & 3 \end{pmatrix}, \qquad N = 16.$$

The image uses only the levels 2 to 5 of the range 0 to 7. The loop of line L5 gives:

| $k$ | $h[k]$ | $c(k)$ | $7c(k)/16$ | $T[k]$ |
|---|---|---|---|---|
| 0 | 0 | 0 | 0 | 0 |
| 1 | 0 | 0 | 0 | 0 |
| 2 | 4 | 4 | 1.75 | 2 |
| 3 | 8 | 12 | 5.25 | 5 |
| 4 | 3 | 15 | 6.5625 | 7 |
| 5 | 1 | 16 | 7 | 7 |
| 6 | 0 | 16 | 7 | 7 |
| 7 | 0 | 16 | 7 | 7 |

Line L8 gives

$$O = \begin{pmatrix} 2 & 5 & 5 & 2 \\ 7 & 2 & 5 & 7 \\ 5 & 5 & 7 & 5 \\ 2 & 7 & 5 & 5 \end{pmatrix}.$$

The output spans 2 to 7 and its histogram is 4 pixels at level 2, 8 at level 5 and 4 at level 7. It is not flat: level 3 has 8 of the 16 pixels, and no table can split them. The levels 4 and 5 merge into 7, so the image now has 3 levels instead of 4. Equalizing $O$ again gives $O$.

## Correctness

The proof is below. Line L7 stores $\operatorname{round}((L-1)c(k)/N)$ by the integer identity above, and line L8 applies it. The table is nondecreasing and $T[L-1] = L-1$, so the output is a valid image and the order of the levels is kept. For $s \le L - 2$, the fraction $G(s)$ of output pixels with value at most $s$ satisfies

$$\frac{s + 1/2}{L-1} - \frac{h_{\max}}{N} \le G(s) < \frac{s + 1/2}{L-1},$$

where $h_{\max}$ is the largest bin of the input histogram. So the output is as flat as a point operation allows, up to one input bin. A second run returns the same image.

## Complexity

In the [word RAM](/word-ram/) with words of at least $\log_2(2LN)$ bits:

- Lines L2 and L3 take $\Theta(L + WH)$ time, like the counting pass of [counting sort](/counting-sort/).
- Lines L4 to L7 take $\Theta(L)$ time. Each step does one addition, one multiplication and one division.
- Line L8 takes $\Theta(WH)$ time, one lookup per pixel.

The total is $\Theta(WH + L)$ time in each case, and $\Theta(L)$ extra space for $h$ and $T$ besides the output, which can overwrite the input. Each pixel must be read, so $\Omega(WH)$ time is necessary. For 16-bit data, $L = 65536$, and the table is still small next to a typical image.

## Properties

- **Point operation.** The output at a pixel depends only on the value there and on the global histogram. Two pixels with the same value get the same output.
- **Monotone.** $T$ is nondecreasing, so edges keep their direction and the gray order is kept. Levels can merge; they never swap.
- **Fewer or equal levels.** The number of distinct values cannot grow, and the [Shannon entropy](/shannon-entropy/) of the histogram cannot grow either, because merging bins never adds information. Equalization makes the histogram look wider, not richer.
- **Idempotent.** Equalizing twice gives the same result as equalizing once.
- **Invariant to monotone changes.** If $I' = f(I)$ for a strictly increasing $f$, then $I$ and $I'$ have the same cumulative counts at matching levels, so they equalize to the same image. This includes a [gamma](/gamma-correction/) curve or a [contrast stretch](/contrast-stretching/) on the stored levels, as long as it does not merge two used levels.
- **No parameter.** There is nothing to tune, which is good for automatic display and bad when the result is wrong.

## Variants and improvements

- **Start at the first used level.** A common form is $T(k) = \operatorname{round}((L-1)(c(k) - c_{\min})/(N - c_{\min}))$, where $c_{\min}$ is the smallest nonzero $c(k)$. It sends the darkest used level to 0, so the output uses the full range. It needs $N > c_{\min}$, that is, at least two levels in use.
- **Histogram matching (specification).** Map through $c$ and then through the inverse of the cumulative histogram of a target shape instead of the uniform one. Equalization is the case of a flat target.
- **Exact histogram specification.** Break the ties between pixels of the same level by a second key, such as a local mean, and then assign output levels by rank. This can split a level and reach the target histogram exactly, at the cost of a sort of $WH$ keys.
- **Adaptive and contrast-limited equalization.** Compute the table per region. [CLAHE](/clahe/) does this per tile with a clip limit on each histogram and interpolates between the tiles.
- **Color.** Equalize one luma or lightness channel and keep the chroma, for example $Y$ of YCbCr or $L^*$ of CIELAB (see [color spaces](/color-spaces/)). Equalizing R, G and B separately changes the hues.

## When to use it

Use it to make a dark, bright or washed-out image readable on screen with no parameter, for example a medical or a satellite image in a viewer, or as a step that removes global brightness and contrast changes before [thresholding](/image-thresholding/) or matching. Do not use it when the gray values carry a measurement, because it destroys the scale. Do not use it on an image with a large uniform background or on noisy flat regions: the large bin takes a big part of the output range and the noise in it is amplified. Use [CLAHE](/clahe/) there, or a [contrast stretch](/contrast-stretching/) when a linear change is enough.

## Pitfalls

- **Scaling by L instead of L − 1.** Writing line L7 as $T[k] \leftarrow \lfloor L\,c/N \rfloor$ gives $T[L-1] = L$, which is 256 for 8-bit data and overflows a byte. Line L7 scales by $L - 1$, so the top level maps to $L - 1$.
- **Rounding in floating point.** Computing $(L-1)c/N$ as a float and then rounding can send a value that should be exactly $k + 1/2$ to the wrong side, and it differs between languages that round halves to even. Line L7 rounds in integers, halves up, so two implementations agree on each pixel.
- **The cumulative count before the bin.** Using $c(k-1)$ instead of $c(k)$ at line L7 (the count strictly below $k$) maps the darkest used level to 0 always, and can map the brightest used level below $L-1$. Line L6 adds $h[k]$ before line L7 reads $c$.
- **Equalizing each color channel.** Running the algorithm on R, G and B separately gives three different tables, so a gray pixel can become colored. Equalize a luma or lightness channel and keep the chroma.
- **Expecting a flat histogram.** The output histogram is flat only when each input bin is small. A test that checks for a flat output fails on most images; the right check is the bound in the Correctness section.

## Implementations

## History

Robert Hummel described the cumulative histogram map, with other histogram transforms, as an automatic enhancement routine for display in 1977. Its adaptive form, with one table per region, was developed in the 1970s and 1980s and led to [CLAHE](/clahe/). The method is standard in image processing textbooks, often with the continuous derivation from the distribution function.

## References
