---
tag: CZBFE7
kind: algorithm
slug: felzenszwalb-distance-transform
name: Felzenszwalb-Huttenlocher distance transform
aliases:
- exact Euclidean distance transform
area: graphics-and-signals/image-processing
level: advanced
summary: The exact squared Euclidean distance transform in O(WH) time, by a lower envelope of parabolas along each column and then each row.
solves: [distance-transform]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels, n: the length of one row or column}
  time: {worst: Θ(W H)}
  space: {extra: Θ(W H)}
properties: {deterministic: true, recursive: false, in_place: false, exact: true, linear: false, separable: true}
prereqs: [distance-transform, lower-envelope-of-segments, convex-hull-trick]
see_also: [chamfer-distance, voronoi-diagram, medial-axis, signed-distance-function, morphological-dilation, morphological-erosion, euclidean-distance, image-skeletonization]
sources:
  - paper: doi:10.4086/toc.2012.v008a019
    title: Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Distance transforms of sampled functions, Theory of Computing 8(19), 415 to 428, 2012
    locator: Section 2.1 (Algorithm 1 and Theorem 2.1, the one-dimensional transform), Section 2.2 (Theorem 2.2, arbitrary dimensions), Section 3 (the L1 transform)
  - paper: doi:10.1109/tpami.2003.1177156
    title: Calvin R. Maurer, Rensheng Qi and Vijay Raghavan, A linear time algorithm for computing exact Euclidean distance transforms of binary images in arbitrary dimensions, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(2), 265 to 270, 2003
    locator: the whole paper (an earlier exact linear time method by partial Voronoi diagrams, general locator)
---

The Felzenszwalb-Huttenlocher algorithm computes the exact squared Euclidean [distance transform](/distance-transform/) of an image in $\Theta(WH)$ time. In one dimension, the transform $D(p) = \min_q \bigl((p - q)^2 + f(q)\bigr)$ is the lower envelope of one parabola per sample, and a single left to right pass with a stack builds that envelope in $O(n)$ time. In two dimensions the squared distance splits into a column term and a row term, so the 1D transform down every column and then along every row gives the 2D result. The input can be any sampled function, not only a binary image, which makes the same code a fast min-convolution for flat or quadratic costs. Felzenszwalb and Huttenlocher wrote it up in a 2004 technical report and published it in Theory of Computing in 2012.

## In plain words

For every pixel of a picture, we want the distance to the nearest marked pixel. Checking every marked pixel for every pixel is slow. The trick is to do one line at a time.

On a single row, each marked pixel spreads a bowl shaped cost around itself: zero at the mark and growing with the square of the distance. The answer at each pixel is the lowest bowl there. Seen from below, only a few bowls show, and they meet at crossing points. A program can walk once along the row, keep the bowls that still show, drop the ones that a new bowl hides, and then read off the lowest bowl at each pixel.

Do this down every column, then do it again along every row with the column results as the bowl heights. The result is the exact squared straight-line distance.

## The problem

The input is a sampled function $F$ on the pixel grid $\{0, \dots, W-1\} \times \{0, \dots, H-1\}$, with values in $\mathbb{Z} \cup \{\infty\}$ and the pixel centers at the integer points. The output is

$$D_F(x, y) = \min_{(x', y')} \bigl((x - x')^2 + (y - y')^2 + F(x', y')\bigr).$$

For a binary image with a set $S$ of feature pixels, set $F = 0$ on $S$ and $F = \infty$ elsewhere; then $D_F(p)$ is the squared Euclidean distance from $p$ to the nearest pixel of $S$, and its square root is the Euclidean distance transform. If $S$ is empty, $D_F = \infty$. The squared values are integers, so the output is exact; the square root is the only step with rounding. Pixels outside the image do not take part: the nearest feature is the nearest inside the image.

## The algorithm

```pseudo id=main
DT1(f, n)                          ▷ D(p) = min over q of (p − q)² + f(q); f(q) = ∞ is allowed
                                   ▷ S(q, r) = ((f(q) + q²) − (f(r) + r²)) / (2q − 2r)
L1   k ← −1                        ▷ v[0..k]: the parabolas of the envelope; z: the breakpoints
L2   for q ← 0 to n − 1 do
L3       if f(q) = ∞ then skip to the next q
L4       while k ≥ 0 and S(q, v[k]) ≤ z[k] do k ← k − 1
L5       k ← k + 1; v[k] ← q; z[k] ← (−∞ if k = 0 else S(q, v[k − 1])); z[k + 1] ← +∞
L6   if k < 0 then return ∞ for every p
L7   k ← 0
L8   for p ← 0 to n − 1 do
L9       while z[k + 1] < p do k ← k + 1
L10      D(p) ← (p − v[k])² + f(v[k])
L11  return D

EDT(F, W, H)
L12  for each column x: G[·][x] ← DT1(F[·][x], H)
L13  for each row y: D[y][·] ← DT1(G[y][·], W)
L14  return D                      ▷ with F = 0 on the features and ∞ elsewhere
```

$S(q, r)$ is the abscissa where the parabolas of $q$ and $r$ cross; right of it, the parabola of the larger index is lower. Line L4 removes parabolas from the top of the stack while the new one crosses the top one at or before the point where the top one starts to rule: such a parabola never shows again. Line L5 pushes the new parabola, which rules from its crossing with the new top to $+\infty$. Lines L7 to L10 walk along the row and the breakpoints together and read the ruling parabola at each $p$. Line L3 skips the samples with $f = \infty$, which have no parabola. This follows Algorithm 1 of the paper, written with a stack index that starts at $-1$ so that a row may begin with infinite samples.

## Example

The 1D transform of the row $f = (9, 9, 2, 9, 9, 9, 0, 9, 9)$:

| $q$ | removed from the stack | stack $v$ after line L5 | breakpoints $z[1..k]$ |
|---|---|---|---|
| 0 | | 0 | |
| 1 | | 0, 1 | $1/2$ |
| 2 | 1, since $S(2, 1) = -2 \le 1/2$ | 0, 2 | $-3/4$ |
| 3 | | 0, 2, 3 | $-3/4$, 6 |
| 4 | 3, since $S(4, 3) = 7/2 \le 6$ | 0, 2, 4 | $-3/4$, $19/4$ |
| 5 | 4, since $S(5, 4) = 9/2 \le 19/4$ | 0, 2, 5 | $-3/4$, $14/3$ |
| 6 | 5, since $S(6, 5) = 1 \le 14/3$ | 0, 2, 6 | $-3/4$, $15/4$ |
| 7 | | 0, 2, 6, 7 | $-3/4$, $15/4$, 11 |
| 8 | 7, since $S(8, 7) = 15/2 \le 11$ | 0, 2, 6, 8 | $-3/4$, $15/4$, $37/4$ |

The final envelope is the parabola of 0 on $(-\infty, -3/4]$, of 2 on $[-3/4, 15/4]$, of 6 on $[15/4, 37/4]$ and of 8 on $[37/4, \infty)$. The parabolas of 0 and 8 rule only outside the row. Reading the envelope gives

| $p$ | 0 | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 |
|---|---|---|---|---|---|---|---|---|---|
| $D(p)$ | 6 | 3 | 2 | 3 | 4 | 1 | 0 | 1 | 4 |

The pixel $p = 4$ is nearer to the sample 2, but the sample 6 is lower: $(4 - 6)^2 + 0 = 4 < (4 - 2)^2 + 2 = 6$.

A 6 by 4 binary image with the features $(1, 1)$ and $(5, 3)$, `#` in the first grid, has this squared EDT:

```text
features          squared distance
. . . . . .        2  1  2  5 10  9
. # . . . .        1  0  1  4  5  4
. . . . . .        2  1  2  5  2  1
. . . . . #        5  4  5  4  1  0
```

At $(4, 0)$ both features are at squared distance 10: $3^2 + 1^2$ and $1^2 + 3^2$.

## Correctness

Two parabolas $P_q$ and $P_r$ with $r < q$ differ by a linear function of $p$, so they cross once, at $S(q, r)$, and $P_q$ is the lower one to the right. The proof below keeps the invariant that the stack holds the parabolas of the envelope of the samples seen so far, left to right, with strictly increasing breakpoints, each ruling on its interval. A new parabola, which has the largest index so far, rules on a final interval $[\tau, \infty)$, and the proof shows that the loop of line L4 stops exactly at the parabola that it crosses at $\tau$; every parabola removed rules nowhere any more. The 2D result follows because $(x - x')^2 + (y - y')^2$ is a sum of a term in $x'$ and a term in $y'$, so the minimum over the pixels is a minimum over rows of a minimum over columns.

## Complexity

- **Time.** In one dimension, each sample enters the stack once and leaves at most once, and the reading pass moves $k$ only forward: $O(n)$. In two dimensions, $W$ columns of length $H$ and $H$ rows of length $W$: $\Theta(WH)$ in the word-RAM model, in every case and independent of the number of features. In $d$ dimensions, $d$ passes give $O(dN)$ for $N$ pixels (Theorem 2.2 of the paper).
- **Space.** The stack and the breakpoints take $O(n)$ for one line, and the intermediate image $\Theta(WH)$.
- **Arithmetic.** With integer $f$, $S$ is a fraction with a denominator of at most $2n$. A program can compare $S(q, v[k]) \le z[k]$ by cross multiplication in integers, or use floating point; floating point can change which of two equal parabolas wins, but not the value of $D$, if the values are small enough to be exact.
- **Lower bound.** Every output pixel must be written, so $\Omega(WH)$ is needed. The algorithm is optimal up to the constant.

## Properties

- **Exact.** The squared result is an integer and equals the brute force minimum at every pixel. No approximation of the metric is made, unlike the [chamfer transform](/chamfer-distance/).
- **Separable.** The 2D transform is the composition of 1D transforms along each axis, in either order.
- **Works on any sampled function.** $F$ may take any finite values, not only 0 and $\infty$. The result is the min-convolution of $F$ with the paraboloid $|p|^2$, also called the generalized distance transform, which is the step used in pictorial structure models for object detection.
- **Feature transform with no extra cost.** Store $v[k]$ at line L10 to get, for each pixel, the coordinate of its nearest feature along the line; two passes give the nearest feature pixel, a discrete [Voronoi diagram](/voronoi-diagram/) of the features.
- **Parallel.** The columns are independent, and so are the rows, so each pass parallelizes over lines.
- **The convex hull trick in disguise.** $P_q(p) - p^2 = -2qp + (q^2 + f(q))$ is a line with slope $-2q$, and the slopes come sorted. The pass of lines L2 to L5 is the monotone [convex hull trick](/convex-hull-trick/), and the envelope is a special case of the [lower envelope of segments](/lower-envelope-of-segments/), where each pair crosses once.

## Variants and improvements

- **Other exact linear time methods.** Maurer, Qi and Raghavan (2003) build partial Voronoi diagrams along each line, and Meijster, Roerdink and Hesselink (2000) use a similar two phase scheme. All three give the exact EDT in linear time; they differ in the details of the 1D step.
- **L1 and other metrics.** For the city block distance, the 1D transform is two passes of a minimum with a slope of 1, also linear (Section 3 of the paper). Any convex function of the distance whose pairwise crossings are unique works with the same stack.
- **Signed distance.** Run the transform on the foreground and on the background and take the difference of the square roots to get a [signed distance function](/signed-distance-function/), used for level sets and for rendering fonts.
- **Disk morphology.** Thresholding the squared EDT at $r^2$ gives the [erosion](/morphological-erosion/) or [dilation](/morphological-dilation/) by a digital disk of radius $r$ in $\Theta(WH)$ for any $r$.
- **Skeletons.** The ridges of the EDT, the pixels where the distance is locally largest across the shape, approximate the [medial axis](/medial-axis/); see [image skeletonization](/image-skeletonization/).
- **Anisotropic pixels.** For pixels of width $a$ and height $b$, use $a^2(p - q)^2$ in the row pass and $b^2(p - q)^2$ in the column pass.

## When to use it

Use this algorithm when you need the exact Euclidean distance from every pixel to a set, for any number of features and any image size: for disk shaped morphology, for skeletons, for signed distance fields, for nearest feature maps, or for robot path clearance. Use it also as a fast min-convolution with a quadratic cost, as in the distance transforms of part based object models. If an approximation is enough and the code must be tiny, a two pass [chamfer transform](/chamfer-distance/) is shorter. For a few queries at chosen points, a [nearest neighbor search](/nearest-neighbor-search/) in a [k-d tree](/kd-tree-nearest-neighbor-search/) of the features is cheaper than the full transform.

## Pitfalls

- **Infinite samples.** The formula for $S$ subtracts $f$ values, and $\infty - \infty$ is undefined. Skip infinite samples at line L3, or use a large finite value with care: too large a value overflows in $f + q^2$, too small a value makes a far pixel look like a feature.
- **A row with no features.** If every sample is infinite, the stack stays empty; return $\infty$ at line L6, not the value of a parabola from the previous row.
- **Using $<$ instead of $\le$ at line L4.** A parabola that only touches the envelope at one point can stay on the stack. The values stay right, but the stack can grow, and the invariant of strictly increasing breakpoints breaks; with floating point it can then read the wrong parabola.
- **Taking the square root too early.** The second pass needs the squared distances of the first pass as the heights of the parabolas. Take the square root only at the end.
- **Integer overflow.** $f(q) + q^2$ in the second pass can reach about $W^2 + H^2$, which fits easily in 64 bits but not always in 16.
- **The border.** Pixels outside the image are never features. If the shape continues outside the image, pad the image first.

## Implementations

## History

Felzenszwalb and Huttenlocher described the lower envelope method in a Cornell technical report in 2004, as a tool for their work on pictorial structures and on belief propagation for early vision, where distance transforms of sampled functions speed up the message updates. The journal version appeared in Theory of Computing in 2012. Exact linear time EDT algorithms by other means were known before: Meijster, Roerdink and Hesselink (2000) and Maurer, Qi and Raghavan (2003). The appeal of this one is its short code and its use for any sampled function.

## References
