---
tag: HJGGJE
kind: algorithm
slug: chamfer-distance
name: Chamfer distance transform
aliases:
- chamfer matching distance
area: graphics-and-signals/image-processing
level: advanced
summary: Approximate the Euclidean distance transform with two raster passes that add small integer weights, such as 3 for an edge step and 4 for a diagonal step.
solves: [distance-transform]
model: word-ram
complexity:
  vars: {W: image width in pixels, H: image height in pixels}
  time: {worst: Θ(W H)}
  space: {extra: O(1)}
properties: {deterministic: true, recursive: false, in_place: true, exact: false, linear: false}
prereqs: [distance-transform, digital-image]
see_also: [felzenszwalb-distance-transform, dijkstra, morphological-erosion, image-skeletonization, medial-axis, fast-marching-method, hausdorff-distance, template-matching]
sources:
  - paper: doi:10.1016/s0734-189x(86)80047-0
    title: Gunilla Borgefors, Distance transformations in digital images, Computer Vision, Graphics, and Image Processing 34(3), 344 to 371, 1986
    locator: the sections on the 3 by 3 and 5 by 5 chamfer masks, their weights and the two pass algorithm (general locator)
  - paper: doi:10.1145/321356.321357
    title: Azriel Rosenfeld and John L. Pfaltz, Sequential operations in digital picture processing, Journal of the ACM 13(4), 471 to 494, 1966
    locator: the two pass sequential computation of the distance to a set for the 4-neighbor and 8-neighbor distances (general locator)
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: the sections on discrete distances and distance functions (general locator)
---

The chamfer distance transform gives each pixel of a binary image an integer approximation of its distance to the nearest feature pixel, in two passes over the image. A step to an edge neighbor costs a small integer $a$ and a step to a corner neighbor costs $b$; with $(a, b) = (3, 4)$ the result divided by 3 is within about 6% of the Euclidean distance. The forward pass runs top to bottom and left to right and pulls values from the four neighbors already visited; the backward pass runs the other way. The algorithm is a [distance transform](/distance-transform/) in the sense of Rosenfeld and Pfaltz, and Borgefors (1986) studied the choice of weights. It is different from the point set chamfer distance used in shape matching, which sums the distances from the points of one set to the nearest points of another.

## In plain words

Mark some pixels of a grid. We want, for every other pixel, how far it is from the nearest marked pixel. Think of walking from a mark to the pixel through neighboring pixels: a step left, right, up or down costs 3, and a diagonal step costs 4, because a diagonal is longer but not twice as long.

The program sweeps the grid like reading a page, from the top left. At each pixel it asks the four neighbors it has already seen (left, and the three above) and keeps the cheapest of their costs plus one step. Then it sweeps back from the bottom right and asks the other four neighbors. After these two sweeps every pixel has the cost of its cheapest walk. Dividing by 3 gives a distance that is close to the straight line distance.

## The problem

The input is a binary image on the rectangle $R = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ with a set $S$ of feature pixels, and two integer weights with $0 < a \le b \le 2a$. The output at each pixel $p$ is the length of the shortest path from $S$ to $p$ in the grid graph where each pixel is joined to its 8 neighbors, an edge step costs $a$ and a diagonal step costs $b$. The proof shows that this equals

$$d(p) = \min_{q \in S} \bigl(a(M - m) + bm\bigr), \qquad M = \max(|\Delta x|, |\Delta y|), \quad m = \min(|\Delta x|, |\Delta y|),$$

with $(\Delta x, \Delta y) = p - q$. If $S$ is empty, $d = \infty$. The value $d/a$ approximates the Euclidean distance $\min_q |p - q|$.

## The algorithm

```pseudo id=main
CHAMFER(I, W, H, a, b)          ▷ I = 1 on the features; neighbors outside the image are skipped
L1   for each pixel p: d(p) ← 0 if I(p) = 1 else ∞
L2   for y ← 0 to H − 1 do                       ▷ forward pass, raster order
L3       for x ← 0 to W − 1 do
L4           d(x, y) ← min(d(x, y), d(x − 1, y) + a, d(x, y − 1) + a, d(x − 1, y − 1) + b, d(x + 1, y − 1) + b)
L5   for y ← H − 1 downto 0 do                   ▷ backward pass, reverse raster order
L6       for x ← W − 1 downto 0 do
L7           d(x, y) ← min(d(x, y), d(x + 1, y) + a, d(x, y + 1) + a, d(x + 1, y + 1) + b, d(x − 1, y + 1) + b)
L8   return d
```

Line L1 starts with 0 on the features and $\infty$ elsewhere. Line L4 uses the forward half of the 3 by 3 mask: the left neighbor and the three neighbors in the row above, all of them already final for this pass. Line L7 uses the mirror half: the right neighbor and the three neighbors in the row below. Each line takes the minimum of the current value and a neighbor plus the cost of the step from it. The result is written in place, so the two passes need no other array.

## Example

A 7 by 5 image with features at $(1, 1)$ and $(5, 3)$, weights 3 and 4. After the forward pass (a dot is still $\infty$) and after the backward pass:

```text
after the forward pass        after the backward pass      exact squared distance
 .  .  .  .  .  .  .          4  3  4  7 10  9 10          2  1  2  5 10  9 10
 .  0  3  6  9 12 15          3  0  3  6  7  6  7          1  0  1  4  5  4  5
 4  3  4  7 10 13 16          4  3  4  7  4  3  4          2  1  2  5  2  1  2
 7  6  7  8 11  0  3          7  6  7  6  3  0  3          5  4  5  4  1  0  1
10  9 10 11  4  3  4         10  9 10  7  4  3  4         10  9 10  5  2  1  2
```

The forward pass cannot reach the row above a feature, nor the pixels to its left in its own row; the backward pass fills them. At $(4, 0)$ the result is $10$, so the estimate is $10/3 \approx 3.33$ against the exact $\sqrt{10} \approx 3.16$. At $(1, 0)$ it is $3/3 = 1$, exact. At $(3, 4)$ it is $7/3 \approx 2.33$ against $\sqrt{5} \approx 2.24$.

## Correctness

Every value the algorithm writes is the cost of a real path of steps from a feature, so no result is below the graph distance. For the upper bound, the cheapest path from a feature $q$ to $p$ takes $m$ diagonal steps toward $p$ and $M - m$ steps along the longer axis, and each of these steps is either forward (it ends at a pixel later in raster order than where it starts) or backward. Doing the forward steps first, the forward pass carries the cost along the first part, and the backward pass carries it along the second part. The path stays in the bounding box of $q$ and $p$, so it never leaves the image. The lower bound $a\alpha + b\delta \ge a(M - m) + bm$ for any path with $\alpha$ edge and $\delta$ diagonal steps uses $a \le b \le 2a$; the [proof](proofs/correctness.md) gives the details.

## Complexity

- **Time.** Each pass visits every pixel once and reads at most four neighbors: $\Theta(WH)$ in every case, independent of the number of features and of the distances.
- **Space.** The passes work in place on the output array; no queue or stack is needed. Each value fits in a small integer: at most $b \cdot \max(W, H)$.
- **Memory access.** Both passes read the current row and one neighboring row, in order, so the transform streams well through caches and suits hardware with line buffers.

## Properties

- **The error of the 3-4 transform, proved.** With $c$ the result and $E$ the exact squared Euclidean distance at a pixel, $8E \le c^2 \le 10E$. So $c/3$ is at least $\tfrac{2\sqrt{2}}{3} \approx 0.943$ and at most $\tfrac{\sqrt{10}}{3} \approx 1.054$ times the Euclidean distance: up to about 5.7% too small, on the diagonals, and up to about 5.4% too large, in the direction $(3, 1)$. Both bounds are reached, for example at $(1, 1)$ with $c = 4$ and at $(3, 1)$ with $c = 10$. Along the axes the scaled result is exact.
- **City block and chessboard as special cases.** $(a, b) = (1, 2)$ gives the city block distance $|\Delta x| + |\Delta y|$, and $(a, b) = (1, 1)$ gives the chessboard distance $\max(|\Delta x|, |\Delta y|)$. Both are exact for their own metric.
- **A metric.** For $0 < a \le b \le 2a$, $g(\Delta) = a(M - m) + bm$ is a norm on $\mathbb{Z}^2$ (its unit ball is an octagon when $a < b < 2a$, a square when $a = b$ and a diamond when $b = 2a$), so the result is the distance to $S$ in a true metric, and its level sets are these polygons rather than circles.
- **Graph distance.** The result is the [Dijkstra](/dijkstra/) distance from all features in the weighted 8-neighbor grid graph, computed without a priority queue because the grid order is enough for these masks.
- **Integer arithmetic.** Only additions and comparisons of small integers, with no rounding.
- **The absolute error grows with the distance.** The relative error is bounded, so the absolute error of $c/3$ grows linearly with the distance: at distance 100 it can be more than 5 pixels.

## Variants and improvements

- **Other weights.** Any $0 < a \le b \le 2a$ works with the same code. The pair $(1, 1)$ and $(1, 2)$ give the chessboard and city block distances, and $(3, 4)$ is the common choice for a small integer approximation of the Euclidean distance. Borgefors also studied the real weights that minimize the largest error for the 3 by 3 mask; the integer pairs approximate them.
- **Larger masks.** A 5 by 5 mask adds the knight moves such as $(1, 2)$ with a third weight, for example $(5, 7, 11)$, and cuts the error further. The forward and backward halves each take the neighbors before and after the pixel in raster order.
- **Three dimensions.** The same scheme with $3 \times 3 \times 3$ masks and three weights for face, edge and corner neighbors works on voxel grids; Borgefors (1984) treated arbitrary dimensions.
- **Exact Euclidean.** When the error is too large, the [Felzenszwalb-Huttenlocher transform](/felzenszwalb-distance-transform/) gives the exact squared Euclidean distance with the same $\Theta(WH)$ time and about the same code length.
- **Constrained and geodesic distances.** Skipping the pixels of an obstacle mask in both passes does not give the geodesic distance in one go, because a shortest path around an obstacle may need many alternations of direction; repeat the two passes until nothing changes, or use [breadth-first search](/breadth-first-search/) or [Dijkstra](/dijkstra/) on the grid.
- **Uses.** Thresholding the result gives [erosion](/morphological-erosion/) by the unit ball, an octagon for $a < b < 2a$, the local maxima give a [skeleton](/image-skeletonization/) of the shape close to the [medial axis](/medial-axis/), and a distance image of edges is the input of the point set matching methods mentioned above.

## When to use it

Use the chamfer transform when an approximate distance is enough and the code must be small, integer only and fast: on embedded hardware, in hardware pipelines, as the input to edge based [template matching](/template-matching/) and to [Hausdorff distance](/hausdorff-distance/) estimates, or for rough clearance maps. Use it with $(1, 2)$ or $(1, 1)$ when the city block or chessboard metric is the one you want, since then it is exact. When the Euclidean distance must be exact, for disk shaped morphology or a precise skeleton, use the [Felzenszwalb-Huttenlocher transform](/felzenszwalb-distance-transform/). On a curved surface or with a speed function, use the [fast marching method](/fast-marching-method/).

## Pitfalls

- **Forgetting to divide by the axial weight.** With $(3, 4)$, the result is about 3 times the distance. Divide by 3, or compare against $3r$ when you threshold at radius $r$.
- **Treating the result as Euclidean.** The level sets are octagons. A threshold at $3r$ gives an octagon, not a disk, and the error grows with the radius.
- **Weights out of range.** If $b > 2a$, diagonal steps are never used and the result is the city block distance times $a$, not the closed form above. If $b < a$, a path can zig-zag through diagonals and leave the bounding box, and two passes may not find it near the image border.
- **One pass only.** The forward pass alone leaves the rows above each feature at $\infty$ and the pixels left of a feature too large. Both passes are needed.
- **Overflow with a sentinel.** If $\infty$ is coded as a large integer, adding $b$ to it can overflow. Use a value larger than any real distance but small enough that the sum fits.
## Implementations

## History

Rosenfeld and Pfaltz (1966) introduced sequential operations on digital pictures and computed the city block and chessboard distances to a set with one forward and one backward raster pass. Later work added weighted masks to get closer to the Euclidean distance. Borgefors (1984) treated distance transforms in arbitrary dimensions, and Borgefors (1986) studied the weights of 3 by 3 and 5 by 5 chamfer masks and their maximal errors, which made the 3-4 and 5-7-11 transforms standard tools.

## References
