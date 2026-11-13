---
tag: M54ARC
kind: algorithm
slug: region-growing
name: Region growing
aliases:
- seeded region growing
- SRG
- Adams-Bischof region growing
area: graphics-and-signals/image-processing
level: advanced
summary: Grow one region from each set of seed pixels, one pixel per step, always adding the unallocated border pixel whose value is closest to the current mean of a region it touches.
solves: [image-segmentation]
model: word-ram
complexity:
  vars: {N: the number of pixels, R: the number of seed regions}
  time: {worst: O(N R log N), average: O(N R log N), best: O(N R log N)}
  space: {extra: Θ(N)}
properties: {deterministic: true, greedy: true, needs_seeds: true, parameter_free: true, regions_meet_their_seeds: true}
history:
  year: 1994
  people: [Rolf Adams, Leanne Bischof]
  note: Adams and Bischof described seeded region growing, controlled by seeds instead of homogeneity thresholds, in IEEE Transactions on Pattern Analysis and Machine Intelligence in 1994.
prereqs: [image-segmentation, priority-queue]
see_also: [watershed-segmentation, flood-fill, connected-component-labeling, felzenszwalb-segmentation, image-thresholding, hysteresis-thresholding, active-contours, grabcut]
sources:
  - paper: doi:10.1109/34.295913
    title: Rolf Adams and Leanne Bischof, Seeded region growing, IEEE Transactions on Pattern Analysis and Machine Intelligence 16(6), 641 to 647, 1994
    locator: Section II (the set T, the measure δ, the step rule, the sequentially sorted list and its frozen δ values) and Section III (properties and the comparison with the watershed)
  - paper: doi:10.1016/S0167-8655(97)00131-1
    title: Andrew Mehnert and Paul Jackway, An improved seeded region growing algorithm, Pattern Recognition Letters 18(10), 1065 to 1071, 1997
    locator: the two order dependencies of seeded region growing and the order-independent version that processes all pixels of equal priority together
  - book: isbn:9780133356724
    title: Rafael C. Gonzalez and Richard E. Woods, Digital Image Processing, fourth edition, Pearson, 2018
    locator: Chapter 10, Image segmentation, the section on region growing and region splitting and merging
---

Region growing segments an image by starting from seed pixels and adding neighboring pixels to the regions one at a time. The best-known form is seeded region growing, from Adams and Bischof in 1994. The user gives one or more sets of seed pixels, one set for each region wanted. At every step the algorithm looks at all unallocated pixels on the border of some region, measures how far each one's gray value is from the current mean of that region, and adds the closest one. It stops when every pixel is allocated. There is no threshold to tune: the seeds decide which features matter, and the rule makes each region as uniform as the connectivity allows. Each piece of a region is connected to a seed of that region. With a [priority queue](/priority-queue/) of border pixels the method is fast, and its flooding order is close to that of the [watershed](/watershed-segmentation/), but it compares pixel values with region means instead of reading a gradient.

## In plain words

Put a few pins in the picture, one pin or a small group for each thing you want to cut out. Each pin starts a region. Now look at all the pixels that touch a region but do not belong to any region yet. For each one, ask how different it is from the average color of the region it touches. Take the one that fits best, add it to that region, and update the average. Repeat until there is nothing left. Noise and small spots get swallowed by the region around them, because they are added last, when nothing better is left.

## The problem

The input is a gray [digital image](/digital-image/) $g$ with $N$ pixels, a neighborhood (4 or 8 neighbors; the paper uses 8), and $R \ge 1$ disjoint nonempty seed sets $A_1, \ldots, A_R$. The output assigns every pixel that is connected to some seed to one of the regions $1, \ldots, R$. It is one form of the [image segmentation](/image-segmentation/) problem, where the seeds fix the number of regions and say which one is which.

The paper defines the growth step by step. After some steps, let $T$ be the set of unallocated pixels with at least one neighbor in some region. For $x \in T$ and a region $A_i$ that $x$ touches, let

$$\delta(x, i) = \Bigl|\, g(x) - \operatorname{mean}_{y \in A_i} g(y) \,\Bigr|.$$

A step takes the pair $(x, i)$ with $x \in T$, $A_i$ touching $x$, and the least $\delta(x, i)$, and adds $x$ to $A_i$. If $x$ touches several regions, it goes to the one with the least $\delta$; the paper also allows flagging such a pixel as a boundary pixel. The rule leaves ties open. The implementation here breaks them by the row, then the column of the pixel, then the region number, which makes the result unique. For color images, $|\cdot|$ becomes a color distance.

## The algorithm

```pseudo id=main
SRG(g, A_1, ..., A_R)
L1  for i ← 1 to R do label A_i with i;  s_i ← Σ_{y ∈ A_i} g(y);  c_i ← |A_i|;  F_i ← ∅
L2      add every unlabeled neighbor of A_i to F_i     ▷ F_i is ordered by gray value
L3  while some F_i is not empty do
L4      for each i with F_i ≠ ∅ do x_i ← the pixel of F_i with g(x_i) closest to s_i / c_i
L5      (x, i) ← the pair (x_i, i) with the least |g(x_i) − s_i / c_i|
L6      label x with i;  s_i ← s_i + g(x);  c_i ← c_i + 1
L7      remove x from every F_j
L8      add every unlabeled neighbor of x to F_i
L9  return the labels
```

$F_i$ is the part of $T$ that touches region $i$, so a pixel that touches two regions is in two lists. Keeping each $F_i$ sorted by gray value is what makes line L4 cheap: the pixel closest to the mean is found by binary search, next to the position where the mean would go. Line L6 updates the sum and the count, so the mean is always current. The implementation keeps the means as exact fractions and applies the tie rule at lines L4 and L5.

**The paper's faster version.** Adams and Bischof implement the method with one sorted list of pixels, the sequentially sorted list. When a pixel enters the list, its $\delta$ is computed against the mean of the region that put it there, and that value is not updated later when the means change. The first pixel of the list is removed; if all its labeled neighbors are in one region, it joins that region and its unlabeled neighbors enter the list; otherwise it is flagged as a boundary pixel. The authors note that the frozen values make a negligible difference in their results and a large difference in speed. The implementation includes this version as well, and the example below shows a case where the frozen values change the result.

## Example

Take the $6 \times 4$ image with rows $(10, 12, 11, 40, 42, 41)$, $(11, 30, 13, 39, 20, 40)$, $(12, 11, 14, 38, 41, 43)$ and $(13, 12, 25, 37, 40, 42)$, 4-connectivity, and two seeds: the top left pixel (value 10) for region 1 and the top right pixel (value 41) for region 2. Write pixels as (column, row). The first steps are:

| step | pixel | value | region | δ | new mean |
|---|---|---|---|---|---|
| 1 | (4, 0) | 42 | 2 | 1 | 83/2 |
| 2 | (0, 1) | 11 | 1 | 1 | 21/2 |
| 3 | (1, 0) | 12 | 1 | 3/2 | 11 |
| 4 | (2, 0) | 11 | 1 | 0 | 11 |
| 5 | (0, 2) | 12 | 1 | 1 | 56/5 |

Step 1 wins a tie of $\delta = 1$ against step 2 because the pixel (4, 0) comes first in the row. At step 3 the pixel 12 at (1, 0) has $\delta = |12 - 21/2| = 3/2$, which beats the bright pixel 40 at (3, 0) with $\delta = 3/2$ only by the tie rule, and both are added soon. The three outliers are the last pixels allocated, at steps 20 to 22: the 25 at (2, 3) joins region 1 with $\delta = 131/10$, the 30 at (1, 1) joins region 1 with $\delta = 186/11$, and the 20 at (4, 1) joins region 2 with $\delta = 223/11$. The 30 is surrounded by region 1, so it can only join region 1. The result is the left three columns for region 1, with mean $174/12 = 14.5$, and the right three for region 2, with mean $463/12 \approx 38.6$. No single gray threshold gives this result: the 20 belongs with the bright region and the 25 and 30 with the dark one, so every threshold puts at least one of them in the wrong class.

**Where the frozen values matter.** Take the $4 \times 2$ image with rows $(15, 4, 10, 13)$ and $(28, 26, 29, 28)$, a seed at the top left (15) and a seed at the bottom right (28). The exact rule gives the top row to region 1 and the bottom row to region 2. In the sorted-list version, the pixel 10 at (2, 0) enters the list when region 2 reaches the 29 below it, with $\delta = |10 - 57/2| = 37/2$. Region 1 then grows to the pixel 4 and has mean $19/2$, so the true $\delta$ of the pixel 10 is $1/2$, but the list still holds $37/2$. The pixel 13 at (3, 0), with its stored $\delta = 15$ from the start, is removed first, and it joins region 2, its only labeled neighbor.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). It shows that the lists $F_i$ hold exactly the pixels of $T$ that touch region $i$ at the start of each pass of the loop, so lines L4 and L5 take the pair with the least $\delta$ over all of $T$, which is the step of the definition. The binary search at line L4 is correct because the value closest to a number in a sorted list sits next to the place where that number would be inserted. Each added pixel has a neighbor in its region, so every connected piece of a region contains a seed pixel of that region. The loop stops when $T$ is empty, which on a connected grid means every pixel is allocated, after exactly $N - \sum_i |A_i|$ steps. The tests compare the implementation with a step-by-step simulation that recomputes $T$, all means and all values of $\delta$ from scratch.

## Complexity

- Each pass of the loop allocates one pixel, so there are at most $N$ passes.
- Line L4 does one search per region: $O(R \log N)$ with balanced search trees for the $F_i$.
- Lines L7 and L8 remove one pixel from at most $R$ lists and insert at most 8 pixels: $O(R \log N)$.

The total is $O(N R \log N)$ time. A pixel is in at most $\min(R, 8)$ lists, so the extra space is $\Theta(N)$. The implementation here uses Python lists with binary search, where an insertion moves the tail of the list, which adds a term proportional to the list length per insertion. The paper's sorted-list version removes each pixel once and inserts it once, so it costs $O(N \log N)$ with a heap, independent of $R$.

## Properties

- **No homogeneity threshold.** The seeds are the only input besides the image. This is the main difference from classical region growing, where a pixel joins when it differs from the region by less than a set amount.
- **Regions meet their seeds.** Every connected piece of region $i$ contains a pixel of $A_i$. With one connected seed set per region, every region is connected.
- **Outliers are absorbed.** A small spot that differs from everything around it is added last, to a region that surrounds it, so it does not form a region of its own unless it has a seed.
- **Order dependence.** The definition does not fix ties, and the sorted-list version also depends on the order in which pixels with equal values enter the list. Mehnert and Jackway named two such dependencies, on the order of pixels with equal $\delta$ and on the choice of region for a pixel with equal $\delta$ to two regions.
- **Assumes equal noise.** The measure $\delta$ compares with the mean only. The paper notes that for regions with very different noise, $\delta$ should be divided by the region's standard deviation, at a higher cost.

## Variants and improvements

- **Classical region growing.** Start from a seed and add 4- or 8-neighbors while $|g(x) - \text{mean}| \le \theta$ or $|g(x) - g(y)| \le \theta$ for a neighbor $y$. This is a [flood fill](/flood-fill/) with a test, and it needs a threshold. With the test $|g(x) - g(y)| \le \theta$, a slow ramp can carry the region anywhere.
- **Improved seeded region growing.** Mehnert and Jackway process all pixels of equal priority in parallel and give a fixed rule for pixels that tie between regions, which makes the result independent of the scan order.
- **Boundary flags.** Pixels that touch two regions are given a boundary label instead of a region, which draws a one-pixel boundary between regions, useful for display and for interactive correction.
- **Normalized δ.** Divide by the standard deviation of the region when regions have different noise levels.
- **Split and merge.** Split the image into blocks by a quadtree until each block is uniform, then merge adjacent uniform blocks. It needs no seeds but needs a uniformity test.
- **Seeds from elsewhere.** Seeds can come from [thresholding](/image-thresholding/) at strict levels, from local extrema, or from a user. The paper shows both manual and automatic seeds.

## When to use it

Use seeded region growing when a user or another step can point at each object, the objects have fairly uniform values, and the result must follow the actual pixel values instead of a gradient: organs in medical images, cells, regions in an interactive tool. It needs no threshold and is robust to isolated noise. Use small seed areas instead of single pixels in noisy images, so that the starting mean is not an outlier, as the paper advises. Do not use it on strongly textured regions, where the mean is not a good model; [Felzenszwalb segmentation](/felzenszwalb-segmentation/) or [mean shift](/mean-shift-segmentation/) adapt better. When the borders are clear in the gradient but the regions are not uniform, the [marker-based watershed](/watershed-segmentation/) is the closer tool. For foreground extraction with color models, see [GrabCut](/grabcut/).

## Pitfalls

- **Single seeds on outliers.** A seed on a noisy pixel gives a wrong starting mean, and the region grows into the wrong values. Use seed areas.
- **Frozen δ values.** The fast version keeps old values in the queue. The error is usually small, but near weak borders it can move pixels from one region to the other, as in the example.
- **Leaks.** One weak spot in a border lets a region flow into the next region if that region has no seed of its own. Every object that must be separate needs a seed.
- **Lighting gradients.** The rule compares with a single mean, so a region with a slow change in brightness is split badly. Correct the background first, as the paper says.
- **Unequal noise.** A noisy region has a mean that is far from many of its own pixels, and a quiet neighbor wins them. Use the normalized $\delta$.
- **Disconnected images.** Pixels in a connected part of the image with no seed are never in $T$ and stay unallocated. Check for them.

## Implementations

## History

Region growing is one of the oldest segmentation methods. The early forms merged a pixel with its neighbors when a homogeneity test passed, and their results depended strongly on the threshold of the test and on noise. Rolf Adams and Leanne Bischof of CSIRO published seeded region growing in 1994 as a correspondence in IEEE Transactions on Pattern Analysis and Machine Intelligence. They replaced the threshold with seeds, defined the step by the least difference from the current region mean, and gave a fast implementation with a sorted list, comparing the results with marker-based watershed segmentation. In 1997 Andrew Mehnert and Paul Jackway showed that the method depends on the order in which pixels are processed and gave an order-independent version.

## References
