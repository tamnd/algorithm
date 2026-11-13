---
tag: QDCGWA
kind: algorithm
slug: contrast-stretching
name: Contrast stretching
aliases:
- min-max normalization
- linear contrast stretch
- percentile contrast stretch
area: graphics-and-signals/image-processing
level: intro
summary: Map the gray levels between two percentiles of the histogram linearly onto the full output range, and clip the rest.
solves: [contrast-enhancement]
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, L: the number of gray levels}
  time: {worst: Θ(W H + L), average: Θ(W H + L), best: Θ(W H + L)}
  space: {extra: Θ(L)}
properties: {deterministic: true, exact: true, point_operation: true, monotone: true, linear_between_ends: true}
prereqs: [image-histogram, contrast-enhancement, quantile]
see_also: [histogram-equalization, clahe, gamma-correction, order-statistic, quickselect, prefix-sums]
sources:
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Section 3.2, Some Basic Intensity Transformation Functions, Piecewise Linear Transformation Functions, Contrast Stretching, pages 142 to 144
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Section 3.1, Point operators (pixel transforms, gain and bias)
---

Contrast stretching is the point operation that maps the gray levels between a low end $lo$ and a high end $hi$ linearly onto the full range $0 \ldots L-1$, and clips the levels outside them to 0 or $L - 1$. With $lo$ and $hi$ equal to the darkest and the brightest pixel it is min-max scaling; with $lo$ and $hi$ at two [quantiles](/quantile/) of the [image histogram](/image-histogram/), a small fraction of extreme pixels is clipped so that one outlier cannot cancel the stretch. It costs $\Theta(WH + L)$ time with a histogram. It differs from [histogram equalization](/histogram-equalization/), which maps through the whole cumulative histogram: a stretch uses the histogram only to find the two ends, and it keeps the shape of the histogram between them.

## In plain words

A dim photo may use only the middle grays, from a dull dark gray to a light gray, and never reach black or white. Contrast stretching finds the darkest and the brightest gray in use and pulls them apart: the darkest becomes black, the brightest becomes white, and every gray in between moves to the same relative place on the new, wider scale. Nothing changes order and the spacing stays even. One very bright speck can spoil this, because it is the brightest gray even though it is only one pixel. So the usual version ignores a small share of the darkest and the brightest pixels, for example one percent at each end. Those pixels become pure black or pure white, and the rest of the image gets a stronger stretch.

## The problem

The input is a gray [digital image](/digital-image/) $I$ of $W \times H$ pixels with integer values in $\{0, \ldots, L-1\}$, one channel, and two fractions $p_{lo}, p_{hi} \ge 0$ with $p_{lo} + p_{hi} < 1$. The values are used as stored, usually gamma encoded. No neighbor is read, so no border rule is needed. The output is the image $O = T(I)$ with

$$T(k) = \operatorname{round}\Big(\operatorname{clamp}\Big(\frac{(L-1)(k - lo)}{hi - lo}, 0, L-1\Big)\Big),$$

where $lo$ is the smallest level with more than $p_{lo}N$ pixels at or below it and $hi$ is the smallest level with at least $(1 - p_{hi})N$ pixels at or below it. In sorted order $s_0 \le \cdots \le s_{N-1}$ of the pixel values, these are the [order statistics](/order-statistic/) $lo = s_{\lfloor p_{lo}N \rfloor}$ and $hi = s_{\lceil (1-p_{hi})N \rceil - 1}$. Rounding takes halves up. This is a method for [contrast enhancement](/contrast-enhancement/).

## The algorithm

```pseudo id=main
CONTRAST-STRETCH(I, W, H, L, p_lo, p_hi)       ▷ p_lo ≥ 0, p_hi ≥ 0, p_lo + p_hi < 1
L1  h ← the histogram of I;  N ← W · H
L2  c ← 0, lo ← −1, hi ← −1
L3  for k ← 0 to L − 1 do
L4      c ← c + h[k]                            ▷ c = c(k), the pixels with value ≤ k
L5      if lo < 0 and c > p_lo · N then lo ← k
L6      if hi < 0 and c ≥ (1 − p_hi) · N then hi ← k
L7  if lo = hi then return a copy of I          ▷ nothing to stretch
L8  for k ← 0 to L − 1 do
L9      if k ≤ lo then T[k] ← 0
L10     else if k ≥ hi then T[k] ← L − 1
L11     else T[k] ← ⌊(2(L − 1)(k − lo) + (hi − lo)) / (2(hi − lo))⌋
L12 for each pixel (x, y) do O(x, y) ← T[I(x, y)]
L13 return O
```

Lines L2 to L6 find both ends in one pass over the running sum of the histogram. Line L11 is the stretch rounded halves up in integers, as in [histogram equalization](/histogram-equalization/). With $p_{lo}$ and $p_{hi}$ as exact fractions, the tests of lines L5 and L6 are exact too. With $p_{lo} = p_{hi} = 0$, line L5 finds the smallest used level and line L6 the largest.

## Example

Take $L = 256$ and the $3 \times 3$ image with the values $60, 70, \ldots, 140$, one pixel each:

$$I = \begin{pmatrix} 60 & 70 & 80 \\ 90 & 100 & 110 \\ 120 & 130 & 140 \end{pmatrix}.$$

With $p_{lo} = p_{hi} = 0$, the ends are $lo = 60$ and $hi = 140$, and $T(k) = \operatorname{round}(255(k - 60)/80)$:

$$O = \begin{pmatrix} 0 & 32 & 64 \\ 96 & 128 & 159 \\ 191 & 223 & 255 \end{pmatrix}.$$

For instance $255 \cdot 20/80 = 63.75$ rounds to 64, and $255 \cdot 50/80 = 159.375$ rounds to 159. The 9 values that spanned 80 levels now span 255, with even steps of about 32.

With $p_{lo} = p_{hi} = 1/9$, one pixel may be clipped at each end. $N = 9$, so line L5 needs $c > 1$ and line L6 needs $c \ge 8$:

| $k$ | 60 | 70 | 80 | 90 | 100 | 110 | 120 | 130 | 140 |
|---|---|---|---|---|---|---|---|---|---|
| $c(k)$ | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 |
| $lo$ after the step | −1 | 70 | 70 | 70 | 70 | 70 | 70 | 70 | 70 |
| $hi$ after the step | −1 | −1 | −1 | −1 | −1 | −1 | −1 | 130 | 130 |

So $lo = 70$ and $hi = 130$, the gain is $255/60 = 4.25$, and

$$O = \begin{pmatrix} 0 & 0 & 43 \\ 85 & 128 & 170 \\ 213 & 255 & 255 \end{pmatrix}.$$

The value $255 \cdot 10/60 = 42.5$ rounds up to 43. The pixels 60 and 140 are clipped, together with the ends 70 and 130 that map exactly to 0 and 255.

## Correctness

The proof is below. Line L5 stops at the first level whose cumulative count passes $p_{lo}N$, which is the order statistic $s_{\lfloor p_{lo}N \rfloor}$; line L6 likewise gives $s_{\lceil (1-p_{hi})N \rceil - 1}$, and $lo \le hi$ because $p_{lo} + p_{hi} < 1$. At most $p_{lo}N$ pixels lie below $lo$ and at most $p_{hi}N$ above $hi$, so the clipped share is as requested. Line L11 computes the rounded line exactly. Because $hi - lo \le L - 1$, the slope $(L-1)/(hi - lo)$ is at least 1, so two different levels in $[lo, hi]$ never merge.

## Complexity

In the [word RAM](/word-ram/):

- Line L1 takes $\Theta(WH + L)$ time.
- Lines L2 to L6 and lines L8 to L11 take $\Theta(L)$ time.
- Line L12 takes $\Theta(WH)$ time.

The total is $\Theta(WH + L)$ time in each case and $\Theta(L)$ extra space. For real-valued pixels, where a histogram is not available, the two ends are order statistics and [quickselect](/quickselect/) finds each in $O(WH)$ expected time, or a sort finds both in $O(WH \log(WH))$ time.

## Properties

- **Linear between the ends.** Between $lo$ and $hi$ the map is a straight line of gain $(L-1)/(hi - lo)$ and offset $-lo$ before the gain, up to rounding. The shape of the histogram between the ends is kept, only spread out.
- **Monotone and injective in the middle.** $T$ is nondecreasing on all levels and injective on $[lo, hi]$. Only the clipped levels below $lo$ and above $hi$ merge.
- **Robust ends.** The ends are order statistics. A pixel below $lo$ can change to any darker value, and a pixel above $hi$ to any brighter value, without moving the ends, and one changed pixel moves each end by at most one rank in the sorted order.
- **Idempotent with no clip.** With $p_{lo} = p_{hi} = 0$, the output has $lo = 0$ and $hi = L - 1$ (when $lo < hi$), and a second run is the identity. With positive fractions a second run clips again.
- **A gain of at least 1.** The map never reduces the contrast between two levels inside $[lo, hi]$.

## Variants and improvements

- **Fixed ends.** Use a given $lo$ and $hi$, for example the known range of a sensor, instead of the histogram. Then the map is the same for every image, which matters for video and for comparison between images.
- **Piecewise linear maps.** Gonzalez and Woods describe the stretch through two control points $(r_1, s_1)$ and $(r_2, s_2)$ with three line pieces. The clipped stretch is the case $s_1 = 0$, $s_2 = L - 1$; thresholding is the limit $r_1 = r_2$.
- **Per channel or shared ends.** For color, stretching R, G and B with their own ends also changes the color balance, which is sometimes used as a crude automatic white balance. With one pair of ends for all three channels, the hues stay.
- **Gain and bias on real values.** For floating point images, $O = a I + b$ with clipping, where $a$ and $b$ come from the ends or from a target mean and standard deviation.
- **Nonlinear maps.** A [gamma](/gamma-correction/) or log curve changes the contrast unevenly over the range. [Histogram equalization](/histogram-equalization/) and [CLAHE](/clahe/) adapt the curve to the histogram.

## When to use it

Use it when the image uses only part of the range and its histogram shape is fine: underexposed scans, raw sensor data with an offset, and the display of 12-bit or 16-bit data on an 8-bit screen with one or two percent clipped at the ends. It is the safe default because it keeps the gray order and the relative spacing, so measurements in the middle remain proportional. When the histogram has a large peak, or when the detail is local, use [histogram equalization](/histogram-equalization/) or [CLAHE](/clahe/).

## Pitfalls

- **Dividing by zero on a flat image.** If all counted pixels share one level, $hi = lo$ and line L11 divides by zero. Line L7 returns the image unchanged before the table is built.
- **Truncating instead of rounding.** Writing line L11 as $\lfloor (L-1)(k - lo)/(hi - lo) \rfloor$ shifts every middle level down by up to one level. Line L11 adds $hi - lo$ to the numerator of the doubled fraction, which rounds halves up.
- **Min and max on noisy data.** With $p_{lo} = p_{hi} = 0$, one hot pixel at 255 and one dead pixel at 0 make line L5 return 0 and line L6 return 255, and the stretch does nothing. Use small positive fractions at lines L5 and L6.
- **The wrong comparison at an end.** Writing line L5 as $c \ge p_{lo}N$ makes $lo = 0$ whenever $p_{lo} = 0$, even when level 0 is empty. Line L5 needs the strict test $c > p_{lo}N$ and line L6 the test $c \ge (1 - p_{hi})N$.
- **Percentiles in floating point.** With $p_{lo} = 0.29$ as a double and $N = 100$, the product is 28.999999999999996, so a level with $c = 29$ passes the test of line L5, while the exact test $29 > 29$ fails, and $lo$ moves by one level. Use exact fractions, or integers $\lfloor p_{lo}N \rfloor$ and $\lceil (1 - p_{hi})N \rceil$ computed once.
- **Stretching encoded values as if they were light.** A linear stretch of gamma encoded codes is not a linear change of light. For photometric work, decode to linear values first (see [gamma correction](/gamma-correction/)).

## Implementations

## History

The linear stretch is among the simplest point operations of digital image display, and it has no single inventor. Gonzalez and Woods present it as a piecewise linear transform with two control points, with the min-max stretch as the case where the points are the darkest and the brightest level of the image. The version with percentile ends is the usual default of display software for remote sensing and scientific images, where a few sensor values are extreme.

## References
