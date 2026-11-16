---
tag: YWMV35
kind: data-structure
slug: cost-volume
name: Cost volume
aliases:
- disparity space image
area: computer-vision/stereo-and-dense-reconstruction
level: core
summary: A 3D array of matching costs indexed by pixel column, row and disparity, on which aggregation and optimization run.
model: word-ram
complexity:
  vars: {W: the image width in pixels, H: the image height in pixels, D: the number of disparities}
  time: {build: Θ(W H D), query: Θ(1)}
  space: {extra: Θ(W H D)}
properties: {deterministic: true, static: false, exact: true}
history:
  year: 1994
  people: [Stephen S. Intille, Aaron F. Bobick]
  note: Intille and Bobick named the disparity space image, the costs of one scanline over all disparities, to reason about occlusions. Scharstein and Szeliski (2002) used the 3D disparity space image as the common data of all the methods in their taxonomy.
prereqs: [stereo-matching-cost, disparity]
see_also: [cost-aggregation, block-matching-stereo, semi-global-matching, left-right-consistency-check, subpixel-disparity-refinement, plane-sweep-stereo, census-transform, stereo-matching]
sources:
  - paper: doi:10.1023/A:1014573219977
    title: Daniel Scharstein and Richard Szeliski, A taxonomy and evaluation of dense two-frame stereo correspondence algorithms, International Journal of Computer Vision 47(1-3), 2002, 7-42
    locator: the parts on the disparity space image C(x, y, d), aggregation as filtering of this volume, and winner-takes-all
  - paper: "Stephen S. Intille and Aaron F. Bobick, Disparity-space images and large occlusion stereo, Computer Vision, ECCV '94, Lecture Notes in Computer Science 801, Springer, 1994"
    locator: the disparity space image of a scanline and its use for occlusions
  - paper: doi:10.1109/TPAMI.2012.156
    title: Asmaa Hosni, Christoph Rhemann, Michael Bleyer, Carsten Rother and Margrit Gelautz, Fast cost-volume filtering for visual correspondence and beyond, IEEE Transactions on Pattern Analysis and Machine Intelligence 35(2), 2013, 504-511
    locator: the cost volume, its filtering slice by slice, and winner-takes-all
  - paper: "Alex Kendall, Hayk Martirosyan, Saumitro Dasgupta, Peter Henry, Ryan Kennedy, Abraham Bachrach and Adam Bry, End-to-end learning of geometry and context for deep stereo regression, IEEE International Conference on Computer Vision, 2017"
    locator: the 4D feature cost volume, 3D convolutions on it, and the soft argmin
  - book: isbn:9783030343712
    title: Richard Szeliski, Computer Vision, Algorithms and Applications, second edition, Springer, 2022
    locator: Chapter 12, Depth estimation (the disparity space image and the cost volume)
---

A cost volume, also called a disparity space image, is the three dimensional array $C(u, v, d)$ that holds the [matching cost](/stereo-matching-cost/) of the left pixel $(u, v)$ at each disparity $d$ of a rectified stereo pair, for all $W H$ pixels and $D$ disparities. It is the common data of almost all dense [stereo matching](/stereo-matching/) methods: a matching cost fills it, [cost aggregation](/cost-aggregation/) filters it, an optimizer such as [semi-global matching](/semi-global-matching/) or winner-takes-all reads a disparity map out of it, and [subpixel refinement](/subpixel-disparity-refinement/) reads the costs next to the chosen disparity. Each entry is read or written in $O(1)$ time; the price is $W H D$ entries of memory. [Plane sweep stereo](/plane-sweep-stereo/) builds the same kind of volume with planes in place of disparities.

## In plain words

Stack $D$ images on top of each other. Image number $d$ of the stack says, for each pixel of the left image, how badly it matches the pixel $d$ columns to its left in the right image. A column through the stack, at one pixel, lists the costs of all candidate disparities of that pixel; its lowest entry is the best match of that pixel alone. A layer of the stack is an ordinary image, so image filters can smooth it. Every step of a stereo program works on this stack, which is why it gets its own name.

## The abstract type

The cost volume is an array over the index set $\{0, \ldots, W - 1\} \times \{0, \ldots, H - 1\} \times \{0, \ldots, D - 1\}$ with these operations:

- **BUILD$(I_L, I_R, D, c)$** sets $C(u, v, d) = c(u, v, d)$, the cost of the left pixel $(u, v)$ against the right pixel $(u - d, v)$, and $C(u, v, d) = \infty$ when $u - d < 0$.
- **GET$(u, v, d)$** and **SET$(u, v, d, x)$** read and write one entry.
- **SLICE$(d)$** and **SET-SLICE$(d, A)$** read and write the $H \times W$ image of one disparity, which is what aggregation filters.
- **WTA()** returns for each pixel the least $d$ with the least cost.
- **RIGHT-VIEW()** returns the volume with the right image as reference, $C_R(x, v, d) = C(x + d, v, d)$, which is $\infty$ when $x + d \ge W$.

## Representation

The code stores the volume in one flat array of $W H D$ numbers. Entry $(u, v, d)$ is at position $(v W + u) D + d$, so the disparity is the fastest index and the costs of one pixel are next to each other. This order suits winner-takes-all, subpixel refinement and the path updates of semi-global matching, which all read the whole column of a pixel. The other common order puts the disparity first, at $(d H + v) W + u$, so that each slice is a contiguous image; it suits filters that work on slices. The two orders hold the same numbers; changing between them is a transpose.

Invalid entries, those whose right pixel is outside the image, hold $\infty$ in the code. A program with integer costs uses the largest value of the type instead. The value must be larger than any valid cost, and larger than any sum of valid costs if aggregation sums over invalid entries.

Learned stereo methods keep a 4D volume: instead of one cost per pixel and disparity, a feature vector of length $F$, built by joining or correlating the features of the two images (Kendall et al. 2017). Networks then turn it into a 3D cost volume.

## Operations

```pseudo id=main
INDEX(u, v, d)
L1  return (v · W + u) · D + d

BUILD(I_L, I_R, D, c)
L2  for each pixel (u, v) in row-major order do
L3      for d ← 0 to D - 1 do
L4          C[INDEX(u, v, d)] ← c(u, v, d) if u - d ≥ 0, else ∞

WTA(C)
L5  for each pixel (u, v) do
L6      best ← C(u, v, 0);  disp(u, v) ← 0
L7      for d ← 1 to D - 1 do if C(u, v, d) < best then best ← C(u, v, d); disp(u, v) ← d
L8  return disp

RIGHT-VIEW(C)
L9  for each pixel (x, v) do
L10     for d ← 0 to D - 1 do
L11         C_R(x, v, d) ← C(x + d, v, d) if x + d < W, else ∞
```

BUILD visits each entry once in the order of the array and costs $W H D$ calls of the cost function. WTA reads each column once and keeps the first minimum, so ties go to the smallest disparity. RIGHT-VIEW uses that the right pixel $(x, v)$ at disparity $d$ is matched with the left pixel $(x + d, v)$, the same pair as the left entry $(x + d, v, d)$. So the volume of the right image costs no new cost evaluations, which is how semi-global matching and others get the second disparity map for a [left-right consistency check](/left-right-consistency-check/). It is a shear of the volume along $u$.

## Example

Take one row, the left row $(10, 10, 50, 90, 10, 10)$, the right row $(10, 50, 90, 10, 10, 10)$, $D = 3$ and the absolute difference cost. BUILD gives these columns, one per left pixel ($\infty$ marks invalid entries):

| $u$ | $d = 0$ | $d = 1$ | $d = 2$ | WTA |
|---|---|---|---|---|
| 0 | 0 | $\infty$ | $\infty$ | 0 |
| 1 | 40 | 0 | $\infty$ | 1 |
| 2 | 40 | 0 | 40 | 1 |
| 3 | 80 | 0 | 40 | 1 |
| 4 | 0 | 0 | 80 | 0 |
| 5 | 0 | 0 | 0 | 0 |

The true disparity is 1 everywhere. WTA is right where the column has one clear minimum and wrong at $u = 4$ and $u = 5$, where flat pixels tie and the tie goes to 0; at $u = 0$ the true match is outside the right image. Slice $d = 1$ is the row $(\infty, 0, 0, 0, 0, 0)$. RIGHT-VIEW gives the columns $(0, 0, 40)$, $(40, 0, 40)$, $(40, 0, 80)$, $(80, 0, 0)$, $(0, 0, \infty)$, $(0, \infty, \infty)$ for $x = 0, \ldots, 5$; for instance $C_R(3, 0, 2) = C(5, 0, 2) = 0$.

**Size.** A $640 \times 480$ pair with $D = 128$ has $39\,321\,600$ entries: 78.6 MB with 16-bit costs, 157.3 MB with 32-bit costs.

## Correctness

The full proof is in [proofs/correctness.md](proofs/correctness.md). INDEX is a bijection from the index set onto $\{0, \ldots, W H D - 1\}$, so every entry has its own cell. BUILD writes each cell exactly once with the value of the definition. WTA keeps, for each pixel, the invariant that after the disparities $0, \ldots, d$ it holds the least cost and the least disparity that reaches it. RIGHT-VIEW is correct because the pair (right $(x, v)$, left $(x + d, v)$) is the pair of the left entry $(x + d, v, d)$, and $x + d < W$ is exactly the condition that this left entry exists.

## Complexity

| operation | time | notes |
|---|---|---|
| INDEX, GET, SET | $\Theta(1)$ | |
| BUILD | $\Theta(W H D)$ cost evaluations | each $O(1)$ for AD or census, $O(r^2)$ for a window cost computed directly |
| SLICE, SET-SLICE | $\Theta(W H)$ | |
| WTA | $\Theta(W H D)$ | |
| RIGHT-VIEW | $\Theta(W H D)$ | no cost evaluations |
| space | $\Theta(W H D)$ | 4D learned volumes: $\Theta(W H D F)$ |

The model is the word RAM with costs that fit a word. [Block matching](/block-matching-stereo/) avoids the $\Theta(W H D)$ space by keeping one slice at a time and a running best per pixel, but then it cannot run an optimizer that needs all the costs of a pixel at once.

## Variants

- **Reduced volumes.** Keep only the $D' \ll D$ best candidates of each pixel, or a coarse volume at a lower resolution, to save memory. Hierarchical and learned methods refine from coarse to fine.
- **Plane sweep volumes.** For many views or unrectified images, index the volume by depth planes instead of disparities; see [plane sweep stereo](/plane-sweep-stereo/).
- **Feature volumes.** Learned methods join the feature vectors of the two images per disparity (a 4D volume) or store their dot product (a correlation volume), then process it with 3D convolutions.
- **Soft argmin.** Instead of WTA, take $\hat d = \sum_d d \, \sigma_d$ with $\sigma = \operatorname{softmax}(-C(u, v, \cdot))$. It is differentiable and gives a fractional disparity; Kendall et al. (2017) used it to train networks end to end. With a cost column that has two minima it returns a value between them.

## When to use it

Build the full volume when a later step needs the costs of all disparities of a pixel at once: edge-aware [aggregation](/cost-aggregation/) slice by slice, semi-global matching, a uniqueness test on the best and second best costs, subpixel refinement, or the right view for a consistency check. When memory is short, as on small processors or for large $D$, keep one slice at a time as block matching does, or use a reduced volume.

## Pitfalls

- **Memory.** $W H D$ grows fast. A 2-megapixel pair with $D = 256$ and 32-bit costs needs 2 GB. Choose the type of the costs and the disparity range with this in mind.
- **Invalid entries.** The first $d$ columns have no match at disparity $d$. If they hold 0 instead of a large value, WTA chooses them. If they hold the largest integer, a sum over a window overflows.
- **Layout and cache.** Filtering slices of a volume stored with the disparity as the fastest index jumps by $D$ entries per pixel. Choose the order for the step that dominates the time.
- **Sign of the right view.** The right pixel $(x, v)$ matches the left pixel $(x + d, v)$, not $(x - d, v)$. Getting this wrong makes every left-right check fail.

## Implementations

## History

Intille and Bobick (1994) introduced the disparity space image of a scanline, the costs of each column at each disparity, to find occlusions in stereo. Scharstein and Szeliski (2002) made the 3D disparity space image the common data of all methods in their taxonomy, with aggregation as a filter on it and optimization as a search in it. Hosni et al. (2013) framed local stereo as filtering of the cost volume with an edge-aware filter, and Kendall et al. (2017) brought the cost volume into deep networks as a 4D array of features.

## References
