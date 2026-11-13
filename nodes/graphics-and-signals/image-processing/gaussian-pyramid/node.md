---
tag: 5RH4SA
kind: data-structure
slug: gaussian-pyramid
name: Gaussian pyramid
area: graphics-and-signals/image-processing
level: advanced
summary: The levels G_0 to G_N of an image, each one the one before blurred with a 5-tap separable kernel and cut to its even rows and columns. It takes about 4/3 of the image size.
model: real-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels}
  time: {build: Θ(W H), level: O(1), sample: O(1)}
  space: {total: Θ(W H)}
properties: {persistent: false, concurrent: false, external: false}
history:
  year: 1983
  people: [Peter J. Burt, Edward H. Adelson]
  note: Burt and Adelson defined the sequence of reduced images with the REDUCE step and a 5-by-5 generating kernel, and named it the Gaussian pyramid after the shape of its main kernel.
prereqs: [image-pyramid, gaussian-filter, separable-filter]
see_also: [laplacian-pyramid, mipmap, image-resampling, aliasing, discrete-wavelet-transform, lucas-kanade-method, sift, bilinear-interpolation]
sources:
  - paper: doi:10.1109/TCOM.1983.1095851
    title: Peter J. Burt and Edward H. Adelson, The Laplacian pyramid as a compact image code, IEEE Transactions on Communications 31(4), 1983, 532 to 540
    locator: page 533 (REDUCE, the separable generating kernel, equal contribution and the sizes M 2^N + 1) and page 534 (the kernel family for a = 0.3 to 0.6)
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 3, Section 3.5, Pyramids and wavelets (decimation, the binomial kernel and the Gaussian pyramid)
  - paper: "Edward H. Adelson, Charles H. Anderson, James R. Bergen, Peter J. Burt and Joan M. Ogden, Pyramid methods in image processing, RCA Engineer 29(6), 1984, 33 to 41"
    locator: the construction of the Gaussian pyramid and its cost compared with direct filtering at each scale
---

A Gaussian pyramid stores an image $G_0$ together with the reduced images $G_1, G_2, \ldots, G_N$, where each $G_{l+1}$ is $G_l$ blurred with a small separable kernel and then cut to its even rows and columns. It is the low-pass kind of [image pyramid](/image-pyramid/). Each level has about a quarter of the samples of the level below, so the whole structure takes about $4/3$ of the space of the image, and it is built in $\Theta(WH)$ time for a $W \times H$ image. Burt and Adelson's kernel has 5 taps and resembles a [Gaussian](/gaussian-filter/), which gives the name.

## In plain words

You want copies of a picture at half size, quarter size and so on, and you want each copy to look like a smooth, smaller version of the picture, not a noisy one. To make the next copy, replace each pixel by a weighted average of the 5 by 5 pixels around it, with the most weight in the middle, and then keep only every second pixel in each row and every second row. Repeat this on the result until only one pixel is left. The same small table of weights is used at every step. Because each copy is a quarter of the one before, all the copies together are only about one third larger than the picture. A program can then look at the picture at any of these sizes without blurring again.

## The abstract type

The structure holds a sequence of 2D arrays $G_0, \ldots, G_N$ of real values, with these operations.

- **Build** $(I, \hat w)$: make the levels from an image $I$ of $W \times H$ samples and a 1D kernel $\hat w(-2), \ldots, \hat w(2)$.
- **Level** $(l)$: return $G_l$, an array of $W_l \times H_l$ samples.
- **Sample** $(l, x, y)$: return $G_l(x, y)$ for $0 \le x < W_l$ and $0 \le y < H_l$.
- **Map** $(l, x, y)$: return the position $(2^l x, 2^l y)$ of level 0 on which sample $(x, y)$ of level $l$ sits.

The invariant is $G_{l+1} = \mathrm{REDUCE}(G_l)$, with

$$
G_{l+1}(i, j) = \sum_{m=-2}^{2} \sum_{n=-2}^{2} \hat w(m)\, \hat w(n)\, G_l\big(\rho_{W_l}(2i + m), \rho_{H_l}(2j + n)\big),
$$

where $\rho_n$ is the border rule. The pyramid is static: it is rebuilt from the image when the image changes.

**Model.** The image has one channel (a color image gets one pyramid per channel, or one with vector samples). Pixel $(x, y)$ has integer indices, with its center at $(x + 1/2, y + 1/2)$ in level 0 units. Sample $(i, j)$ of level $l$ sits on pixel $(2^l i, 2^l j)$ of level 0, not at the center of a $2^l \times 2^l$ block; this is the grid of Burt and Adelson, and it differs from the block-centered grid of the [mipmap](/mipmap/). The values are real numbers, best in a linear encoding when the average must be physical; an sRGB image averaged as stored gives darker results at sharp contrasts (see [gamma correction](/gamma-correction/)). The border rule on this page is reflect-101: $\rho_n(-1) = 1$, $\rho_n(n) = n - 2$, and in general $\rho_n$ reflects the index with period $2n - 2$ (with $\rho_1 \equiv 0$). Sizes round up: $W_{l+1} = \lceil W_l / 2 \rceil$, $H_{l+1} = \lceil H_l / 2 \rceil$, and the last level is $1 \times 1$.

**The kernel.** Burt and Adelson ask that $\hat w$ is normalized ($\sum_m \hat w(m) = 1$), symmetric, and of *equal contribution*: each sample of level $l$ gives the same total weight $1/4$ to level $l + 1$. With $\hat w(0) = a$, these three rules force $\hat w(\pm 1) = 1/4$ and $\hat w(\pm 2) = 1/4 - a/2$. The choice $a = 0.4$ gives a shape close to a Gaussian; $a = 3/8$ is the binomial kernel $\frac{1}{16}(1, 4, 6, 4, 1)$; $a = 1/2$ is a triangle; $a = 0.6$ has negative side taps.

## Representation

The levels are stored as separate arrays, or packed one after another in one buffer with a table of offsets, $\mathrm{off}_0 = 0$ and $\mathrm{off}_{l+1} = \mathrm{off}_l + W_l H_l$. Sample $(x, y)$ of level $l$ is then at index $\mathrm{off}_l + y W_l + x$. The sizes $W_l$ and $H_l$ come from the base size alone, so the table costs $O(\log \max(W, H))$ words. The kernel is the same for all levels and is stored once.

## Operations

```pseudo id=main
REDUCE(g, ŵ)                                ▷ g has W × H samples
L1  W′ ← ⌈W / 2⌉;  H′ ← ⌈H / 2⌉
L2  for each row y in 0 .. H − 1 and each i in 0 .. W′ − 1 do
L3      r[y][i] ← Σ_{m = −2..2} ŵ(m) · g[y][ρ_W(2i + m)]      ▷ the rows, at even columns only
L4  for each j in 0 .. H′ − 1 and each i in 0 .. W′ − 1 do
L5      g′[j][i] ← Σ_{n = −2..2} ŵ(n) · r[ρ_H(2j + n)][i]     ▷ the columns, at even rows only
L6  return g′

BUILD(I, ŵ)
L7  G_0 ← I
L8  while G_l has more than one sample do               ▷ l is the index of the last level
L9      G_{l+1} ← REDUCE(G_l, ŵ)
L10 return G_0, …, G_N
```

Lines L2 and L3 filter each row but compute only the outputs at even columns, since the others are dropped. Lines L4 and L5 do the same down the columns, and only at even rows. This order gives the 2D sum of the invariant (see the proof) with $5 W' H + 5 W' H'$ multiply-adds, about $3.75\,WH$, where a direct $5 \times 5$ sum at every pixel followed by the cut costs $25\,WH$.

**Level, sample and map** are array lookups through the offset table, in $O(1)$ time. **Map** returns $(2^l x, 2^l y)$; the reverse direction, from a level 0 position $(X, Y)$ to level $l$, gives the real position $(X / 2^l, Y / 2^l)$, and a sample there is read with [bilinear interpolation](/bilinear-interpolation/).

## Example

Take the $5 \times 5$ image in which every row is $0, 0, 16, 16, 16$, a vertical step edge, and the binomial kernel $\frac{1}{16}(1, 4, 6, 4, 1)$. All rows are equal and the kernel sums to 1, so the column pass of REDUCE changes nothing, and it is enough to follow one row.

| level | size | each row |
|---|---|---|
| $G_0$ | $5 \times 5$ | $0, 0, 16, 16, 16$ |
| $G_1$ | $3 \times 3$ | $2, 11, 16$ |
| $G_2$ | $2 \times 2$ | $33/4, 47/4$ |
| $G_3$ | $1 \times 1$ | $10$ |

For $G_1(0)$, the taps $2i + m$ for $m = -2, \ldots, 2$ are $-2, -1, 0, 1, 2$, which the border maps to $2, 1, 0, 1, 2$, with values $16, 0, 0, 0, 16$. So $G_1(0) = (1 \cdot 16 + 4 \cdot 0 + 6 \cdot 0 + 4 \cdot 0 + 1 \cdot 16)/16 = 2$. For $G_1(1)$, the taps are $0$ to $4$, and $(0 + 0 + 6 \cdot 16 + 4 \cdot 16 + 16)/16 = 176/16 = 11$. For $G_1(2)$, the taps $2, 3, 4, 5, 6$ map to $2, 3, 4, 3, 2$, all 16, so the value is 16. The edge is now a ramp over the three samples. The next step gives $(16 + 4 \cdot 11 + 6 \cdot 2 + 4 \cdot 11 + 16)/16 = 132/16 = 33/4$ and $(2 + 4 \cdot 11 + 6 \cdot 16 + 4 \cdot 11 + 2)/16 = 188/16 = 47/4$, and the last step gives $10$.

The top value 10 is not the mean $48/5 = 9.6$ of the image. The mirror border counts the edge samples with other weights than the inner ones, so the pyramid top is a weighted mean.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows four facts. First, the two 1D passes of lines L2 to L5 compute exactly the 2D sum of the invariant, by [separability](/separable-filter/) and an exchange of the finite sums. Second, a kernel with sum 1 maps a constant image to the same constant at every level, and a kernel with no negative taps ($0 \le a \le 1/2$) keeps every level within the minimum and maximum of the image. For $a = 3/5$ the row $16, 0, 0, 0, 16$ gives $-8/5$ at its middle, so the range rule fails when a tap is negative. Third, the loop stops after exactly $\lceil \log_2 \max(W, H) \rceil$ calls of REDUCE. Fourth, the size counts of the next section hold.

## Complexity

Let $S = \sum_{l=0}^{N} W_l H_l$ be the number of samples in all levels.

- **Size, powers of two.** For $W = H = 2^N$, the levels are $2^{N-l} \times 2^{N-l}$ and $S = \sum_{l=0}^{N} 4^{l} = (4^{N+1} - 1)/3 = (4WH - 1)/3$. A $256 \times 256$ image gives $S = 87381$.
- **Size, rounding down.** If each halving rounds down, $W_l \le W / 2^l$ and $H_l \le H / 2^l$, so $S \le WH \sum_{l \ge 0} 4^{-l}$ and $S < \frac{4}{3} WH$.
- **Size, rounding up.** With $\lceil \cdot / 2 \rceil$, as on this page and in the $2^N + 1$ sizes of Burt and Adelson, $S$ can exceed $\frac{4}{3} WH$. A $3 \times 3$ image has levels of 9, 4 and 1 samples, so $S = 14 > 12$. A $257 \times 257$ image has $S = 88413$, which is $1043/3$ more than $\frac{4}{3} \cdot 66049$. A $640 \times 480$ image has $S = 409609$, 9 more than $\frac{4}{3} WH = 409600$. The bound that holds for all sizes is $S \le \frac{4}{3}(W-1)(H-1) + 2(W + H - 2) + (N + 1)$, and for $W = H = 2^k + 1$ every level but the $1 \times 1$ one meets its term of this bound with equality. So $S = \frac{4}{3} WH + O(W + H + \log \max(W, H))$.
- **Time to build.** REDUCE on a $W_l \times H_l$ level does $5 W_{l+1} H_l$ multiply-adds in lines L2 and L3 and $5 W_{l+1} H_{l+1}$ in lines L4 and L5. Both are at most $5 W_l H_l$, because $\lceil n/2 \rceil \le n$ for $n \ge 1$, so the total is $O(S) = \Theta(WH)$ in the [real RAM](/real-ram/), and it is $\Omega(WH)$ because every pixel is read.
- **Queries.** Level, sample and map take $O(1)$.

A blur as wide as $2^l$ pixels, computed directly on the full image with a 2D kernel of that width, costs $\Theta(WH \cdot 4^l)$. The pyramid gives a blur of that width at level $l$, on a grid with about $4^l$ times fewer samples, for $\Theta(WH / 4^l)$ more work.

## Variants

- **The kernel parameter.** Burt and Adelson study $a$ from 0.3 to 0.6. The binomial $a = 3/8$ is common because its taps are small integers over 16.
- **Odd sizes.** Burt and Adelson take $C = M_C 2^N + 1$ columns and $R = M_R 2^N + 1$ rows, so that every level has the form $M 2^{N-l} + 1$ and the samples at even indices include both ends. With other sizes, the last sample of a level sits at or before the last pixel of level 0: $2^l (W_l - 1) \le W - 1$.
- **Box kernel.** A $2 \times 2$ box average with block-centered samples gives the [mipmap](/mipmap/). It is cheaper and blurs less, so the levels alias more.
- **Finer scale steps.** [SIFT](/sift/) and other scale-space detectors put several blurs between two halvings, so that the scale grows by a factor smaller than 2 from one image to the next.
- **No subsampling.** A Gaussian stack keeps all images at full size. It costs $\Theta(WH)$ per level instead of a geometric sum.
- **Band-pass levels.** The [Laplacian pyramid](/laplacian-pyramid/) stores the differences between a level and the expanded next level, built on top of this structure.

## When to use it

Use a Gaussian pyramid when a method must look at an image at several scales: coarse-to-fine motion estimation such as the iterative [Lucas-Kanade method](/lucas-kanade-method/), coarse-to-fine [template matching](/template-matching/), multiscale feature detection, and the low-pass half of the Laplacian pyramid. Use a [mipmap](/mipmap/) instead for texture lookup in a renderer, where the box filter and the fixed layout are what the hardware expects. Use a [discrete wavelet transform](/discrete-wavelet-transform/) when the samples must not exceed the image size.

## Pitfalls

- **Subsampling with no blur.** Dropping every second sample of an unfiltered level aliases fine patterns into false coarse ones (see [aliasing](/aliasing/)).
- **The grid offset.** Sample $(i, j)$ of level $l$ sits on pixel $(2^l i, 2^l j)$, not on the center of a $2^l \times 2^l$ block. Code that mixes this grid with the block-centered grid of a mipmap or a resize function is off by $(2^l - 1)/2$ pixels at level $l$.
- **The 4/3 bound.** It is an upper bound when sizes round down, and for $W = H = 2^N$, where $S = (4WH - 1)/3$ is just under it. With rounding up it can be exceeded by a term of order $W + H$, even for powers of two that are not square: a $4 \times 1$ image has $S = 7$, and a $1024 \times 512$ image has $S = 699051$ against $699050\tfrac{2}{3}$; allocate from the exact sum of $W_l H_l$.
- **The border.** Zero padding darkens the edges of every level, and the effect grows with the level. Mirror or clamp the border.
- **Gamma.** Averaging sRGB values as stored shifts the gray level of fine patterns. Convert to linear values first when the levels must keep the mean light.
- **Integer levels.** Rounding each level to integers adds a rounding error at each step. Keep extra fraction digits, or use a wider type, when later steps subtract levels.

## Implementations

## History

Burt and Adelson described the Gaussian pyramid in 1983, as the first step of their Laplacian pyramid code. They defined the REDUCE step, the 5-by-5 separable generating kernel with the equal contribution rule, and the family of kernels for $a$ from 0.3 to 0.6, and they named the sequence after the Gaussian-like member of that family. For the conditions on the kernel they refer to Burt's 1981 paper on fast filter transforms for image processing. The 1984 survey by Adelson, Anderson, Bergen, Burt and Ogden in RCA Engineer collected the uses of these pyramids.

## References
