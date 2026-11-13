---
tag: FCH3KR
kind: algorithm
slug: median-cut
name: Median cut
aliases:
- Heckbert median cut
area: graphics-and-signals/image-processing
level: advanced
summary: Make a palette of k colors by splitting the box of image colors with the largest side at the median along that side, until there are k boxes, then use the mean of each box.
solves: [color-quantization]
model: real-ram
complexity:
  vars: {n: the number of pixels, k: the palette size}
  time: {worst: O(n k), average: O(n k), best: Θ(n)}
  space: {extra: Θ(n)}
properties: {deterministic: true, exact: false, heuristic: true, greedy: true, divisive: true}
history:
  year: 1979
  people: [Paul S. Heckbert]
  note: Heckbert devised median cut in December 1979 as an alternative to the popularity algorithm, described it in his MIT bachelor's thesis of 1980, and published it at SIGGRAPH 1982.
prereqs: [color-quantization, selection-problem]
see_also: [octree-color-quantization, k-means, kd-tree, vector-quantization, floyd-steinberg-dithering, ordered-dithering, k-means-problem, nearest-neighbor-search]
sources:
  - paper: doi:10.1145/965145.801294
    title: Paul Heckbert, Color image quantization for frame buffer display, ACM SIGGRAPH Computer Graphics 16(3), 1982, 297 to 307
    locator: the section on the median cut algorithm, and the comparison with the popularity algorithm
  - url: https://www.cs.cmu.edu/~ph/ciq_thesis
    title: Paul S. Heckbert, Color image quantization for frame buffer display, bachelor's thesis, Department of Mathematics, Massachusetts Institute of Technology, May 1980
    locator: the sections The Median Cut Algorithm (the split rule and the box means), The Variance Bisection Algorithm, and Phase 3 (the mapping of each color to the nearest palette color)
  - paper: doi:10.1145/146443.146475
    title: Xiaolin Wu, Color quantization by dynamic programming and principal analysis, ACM Transactions on Graphics 11(4), 1992, 348 to 372
    locator: the comparison of median cut with splits that reduce the variance, and the splits along the principal axis
---

Median cut makes a palette of $k$ colors for an image. It puts all pixel colors in one box of the RGB cube and then, $k - 1$ times, splits the box with the longest side across that side, at the median color along it, so that each half holds about the same number of pixels. The palette is the mean color of each box, and each pixel takes the nearest palette color. Paul Heckbert devised the method in 1979 as an alternative to taking the $k$ most frequent colors. It is a fast heuristic for the [color quantization](/color-quantization/) problem: it gives each palette color a similar number of pixels, but it has no bound on its error relative to the best palette.

## In plain words

Think of each pixel as a dot in a cube, where the three directions are red, green and blue. Put a box around all the dots. Find the box that is longest in some direction, and cut it into two boxes across that direction, at the place where half of its dots are on each side. Do this again and again until you have as many boxes as palette colors. The average color of the dots in each box becomes one palette color. Then paint each pixel with the palette color that is nearest to it. Because each cut halves the dots, busy color regions get many palette colors and empty regions get few. A small group of very different pixels can share a box with many others and lose its color.

## The problem

The input is a list of $n$ colors $c_1, \ldots, c_n$, one per pixel, each a vector of $d$ numbers (for RGB, $d = 3$ and the values are integers from 0 to 255), and a palette size $k \ge 1$. The output is a palette $p_1, \ldots, p_{k'}$ with $k' \le k$ and an index $j(i)$ for each pixel. The error is

$$
\mathrm{SSE} = \sum_{i=1}^{n} |c_i - p_{j(i)}|^2 ,
$$

the total squared distance in the color space. Minimizing it is the weighted [k-means problem](/k-means-problem/) on the colors; median cut does not minimize it, it only aims to make it small.

## The algorithm

```pseudo id=main
MEDIAN-CUT(c₁ … cₙ, k)
L1  B ← one box that holds all n colors
L2  while |B| < k do
L3      pick the box b ∈ B and axis a with the largest extent max_{c∈b} c_a − min_{c∈b} c_a
L4      if that extent is 0 then break                  ▷ each box holds one distinct color
L5      order the colors of b by coordinate a
L6      m ← coordinate a of the color at position ⌊|b|/2⌋   ▷ the median
L7      L ← {c ∈ b : c_a < m};  R ← {c ∈ b : c_a ≥ m}   ▷ if L = ∅, use ≤ m and > m
L8      replace b in B by L and R
L9  p ← the mean of each box of B
L10 for i ← 1 to n do j(i) ← the index of the palette color nearest to cᵢ
L11 return p, j
```

The split in line L7 uses a plane $c_a = m$, so equal colors always go to the same side and the boxes never share a color. A tie in line L3 goes to the first box in the list and then to the red, green, blue order. Line L5 needs only the median, so a [selection](/selection-problem/) algorithm such as [quickselect](/quickselect/) or the linear worst case [median of medians](/median-of-medians/) can replace the sort.

## Example

Five pixels have the colors $(0, 0, 0)$, $(1, 0, 0)$, $(2, 0, 0)$, $(3, 0, 0)$ and $(100, 0, 0)$, and $k = 2$.

- **Line L3.** The red extent is 100 and the other extents are 0, so the split is on red.
- **Lines L5 to L7.** The median is the color at position $\lfloor 5/2 \rfloor = 2$, so $m = 2$. Then $L = \{0, 1\}$ and $R = \{2, 3, 100\}$ in red.
- **Line L9.** The means are $p_1 = (1/2, 0, 0)$ and $p_2 = (35, 0, 0)$.
- **Line L10.** The pixels 0, 1, 2 and 3 are nearer to $1/2$ than to 35, and 100 is nearer to 35. The error is $\frac{1}{4} + \frac{1}{4} + \frac{9}{4} + \frac{25}{4} + 65^2 = 4234$.

The best palette of two colors is $(3/2, 0, 0)$ and $(100, 0, 0)$, with the groups $\{0, 1, 2, 3\}$ and $\{100\}$ and an error of $\frac{9}{4} + \frac{1}{4} + \frac{1}{4} + \frac{9}{4} = 5$. Median cut is worse by a factor of more than 800, because the median split balances the pixel counts and puts the outlier with two of the dark pixels. On 200 random images of 3 to 8 pixels with values in $[0, 16)$ and $k \in \{2, 3\}$, chosen with seed 8, median cut was strictly worse than the best palette on 130 and never better.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows three facts. First, the loop stops with exactly $\min(k, D)$ boxes, where $D$ is the number of distinct colors, and the box means are distinct, so the palette has $\min(k, D)$ colors. Second, when the values on the split axis are distinct, line L7 puts exactly $\lfloor |b|/2 \rfloor$ colors in $L$. Third, the error is at least the error of the best palette, and the ratio between them is not bounded: for the colors $0, 1, 2, 3, M$ in red and $k = 2$, median cut has error $9 + ((2M - 5)/3)^2$ for $M \ge 12$ while the best error is 5.

## Complexity

- **One split.** Lines L5 to L8 cost $\Theta(|b|)$ with a linear-time selection, or $\Theta(|b| \log |b|)$ with a sort, as in the implementation. Line L3 costs $O(|B|)$ if the extents of each box are kept with the box.
- **All splits.** When the splits are even, each level of the tree of boxes holds all $n$ colors, there are about $\log_2 k$ levels, and the splits cost $\Theta(n \log k)$ in total. Many equal colors can make the splits uneven; in the worst case each split removes few colors from a large box, and $k - 1$ splits cost $O(n k)$.
- **Mapping.** Line L10 with a search over the whole palette costs $\Theta(n k)$; it runs once per distinct color if the colors are first collected in a histogram. A [k-d tree](/kd-tree/) or a grid of buckets over the palette makes each [nearest-neighbor search](/nearest-neighbor-search/) faster in practice.
- **Total.** $O(n k)$ time in the [real RAM](/real-ram/), and $\Theta(n)$ when all pixels have one color and the loop stops at once. The boxes are a partition of the colors, so the extra space is $\Theta(n)$.

Heckbert first reduced each primary to 5 bits, so the boxes hold at most $2^{15} = 32768$ distinct colors with their counts, and the cost depends on that number instead of $n$.

## Properties

- **Equal counts.** Each split halves the pixels of a box, so every palette color stands for a similar share of the image.
- **Boxes are disjoint.** Each split is a plane, so the boxes are axis-aligned and form a partition of the occupied part of the cube, like the cells of a [k-d tree](/kd-tree/) built by median splits.
- **Exact palette size.** The palette has $k$ colors when the image has at least $k$ distinct colors.
- **Deterministic.** The result depends only on the colors and the tie rules.
- **No error bound.** A small group of very different pixels can be merged into a large box, as in the example.

## Variants and improvements

- **Variance split.** Choose the split plane on the dominant axis that minimizes the sum of the variances of the two halves, which Heckbert proposed in the thesis as variance bisection. Wu splits along the principal axis of each box and picks the box whose split reduces the error most.
- **Split the box with the most error.** Pick the box with the largest total squared error, or the largest count times extent, instead of the longest side.
- **Refinement by k-means.** Use the median cut palette as the start of [k-means](/k-means/) iterations, which can only reduce the error.
- **Histogram first.** Reduce each channel to 5 or 6 bits and count colors, so the algorithm works on distinct colors with weights.
- **Perceptual spaces.** Run the splits in a space such as CIELAB, where the distance is closer to the perceived difference.
- **Dithering.** Map pixels through [Floyd-Steinberg dithering](/floyd-steinberg-dithering/) or [ordered dithering](/ordered-dithering/) instead of the nearest color, to hide the bands between palette colors.

## When to use it

Use median cut to make a palette of 16 to 256 colors fast and with no tuning, for GIF images, indexed displays and previews. It gives each palette color a fair share of the pixels, which suits photographs with large smooth areas. For a lower error, refine it with a few rounds of k-means or use a variance split. Use [octree quantization](/octree-color-quantization/) when the image is too large to keep all its colors in memory, because the octree has a bounded size.

## Pitfalls

- **Outliers lose their color.** Small, saturated details such as a red light can disappear into a large box. Weight the split choice by error instead of by size if they matter.
- **Ties on the median.** If many pixels share the median value, a split at a sorted position puts the same color in both boxes. Split by a plane and handle the case where the lower side is empty, as line L7 does.
- **Fewer distinct colors than k.** The loop must stop when no box can be split, or it splits a box of one color into an empty box.
- **Rounding the palette.** The box means are fractions. Rounding them to integers can make two palette colors equal on tiny boxes.
- **Nearest color versus box.** A pixel can be nearer to the mean of another box than to the mean of its own. Mapping by nearest color never increases the error, but it costs a search.

## Implementations

## History

Heckbert, then a student in the Architecture Machine Group at MIT, devised median cut in December 1979, as an alternative to the popularity algorithm of Tom Boyle and Andy Lippman, which took the $k$ most frequent colors after a reduction to 5 bits per primary. His bachelor's thesis of May 1980 describes the median cut and proposes the variance bisection variant, and it notes that an efficient algorithm for the optimal multidimensional problem seemed unlikely. He published the method at SIGGRAPH 1982. Wu in 1992 replaced the median by splits that reduce the variance, along principal axes.

## References
