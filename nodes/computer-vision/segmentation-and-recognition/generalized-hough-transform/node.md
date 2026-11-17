---
tag: GZ6ZY6
kind: algorithm
slug: generalized-hough-transform
name: Generalized Hough transform
aliases:
- Ballard generalized Hough transform
- R-table voting
area: computer-vision/segmentation-and-recognition
level: core
summary: "Detect an arbitrary shape by having each edge point vote, through a table indexed by gradient direction, for the positions of the shape reference point."
solves: [object-detection]
model: real-ram
complexity:
  vars: {m: the number of template edge points, e: the number of image edge points, W: the image width, H: the image height, k: the largest number of R-table entries in one direction bin}
  time: {worst: O(e m + W H), best: O(e k + W H)}
  space: {extra: O(W H + m)}
properties: {deterministic: true, exact: true, output: accumulator and peak}
history:
  year: 1981
  people: [Dana H. Ballard]
  note: "Ballard (Pattern Recognition, 1981) generalized the Hough transform from analytic curves to any shape given by examples, with a table from the gradient direction to the offsets of a reference point, and extended it to rotation, scale and composite shapes."
prereqs: [hough-transform, sobel-operator]
see_also: [implicit-shape-model, template-matching, chamfer-distance, geometric-hashing, alignment-recognition, edge-detection, non-maximum-suppression, object-recognition]
sources:
  - paper: doi:10.1016/0031-3203(81)90009-1
    title: "Dana H. Ballard, Generalizing the Hough transform to detect arbitrary shapes, Pattern Recognition 13(2), 1981, 111-122"
    locator: "The R-table indexed by the gradient direction, the voting for the reference point, and the extension of the parameter space to rotation and scale"
  - paper: doi:10.1145/361237.361242
    title: "Richard O. Duda and Peter E. Hart, Use of the Hough transformation to detect lines and curves in pictures, Communications of the ACM 15(1), 1972, 11-15"
    locator: "The voting scheme for lines in the normal parameterization and its extension to other analytic curves"
  - paper: doi:10.1016/S0734-189X(88)80033-1
    title: "John Illingworth and Josef Kittler, A survey of the Hough transform, Computer Vision, Graphics, and Image Processing 44(1), 1988, 87-116"
    locator: "The survey of the generalized Hough transform and its variants"
---

The generalized Hough transform finds a shape of any form in an image. It does not need a formula for the shape. It needs only one example, the template. Each edge point of the template has a gradient direction and an offset to a fixed reference point. The R-table stores these offsets, sorted by gradient direction. In a new image, each edge point looks up its gradient direction in the R-table and votes for all the reference positions that the table allows. A copy of the shape makes many votes agree on one cell, and that cell gives its position. This page builds on the [Hough transform](/hough-transform/) for lines and covers only what the generalization adds.

## In plain words

Draw the outline of a shape and mark one point inside it, the center. For each point of the outline, note in which direction the outline faces there and where the center is from that point. Keep these notes in a book, with one page for each direction.

To find the shape in a picture, take each outline point of the picture. Look at the page for its direction. For each note on that page, put a mark where the center would be. Where the shape really is, many marks fall on the same spot. Other outline points scatter their marks. The spot with the most marks is the answer.

## The problem

**Input.** A template image $T$ and a reference point $c$ in it, and an image $I$ of width $W$ and height $H$, both as arrays $\mathrm{img}[v][u]$ with $u$ the column and $v$ the row. A threshold $\tau > 0$ on the gradient magnitude and a number $B$ of direction bins (here $B = 8$).

**Edge points.** The gradient $(g_u, g_v)$ at a pixel comes from the [Sobel operator](/sobel-operator/), and it is 0 on the border of the image. A pixel $y$ is an edge point if $g_u^2 + g_v^2 \ge \tau^2$ and the gradient is not zero. Its bin is $b(y) = \lfloor \varphi / (2\pi / B) + 1/2 \rfloor \bmod B$ with $\varphi = \mathrm{atan2}(g_v, g_u)$, so the bins are centered at the multiples of $2\pi / B$. The template gives $m$ edge points $(x_i, b_i)$ and the image gives $e$ edge points $(y_j, b_j)$.

**Output.** The accumulator $A$ on the pixel grid,
$$A[p] = \#\{(i, j) : b_i = b_j \text{ and } y_j + (c - x_i) = p\},$$
the number of pairs of a template edge point and an image edge point with the same bin that put the reference point at $p$. Also the cell with the largest count, with ties to the smallest $v$, then the smallest $u$.

## The algorithm

```pseudo id=main
GHT(template edges, c, image edges)    ▷ R[0..B-1] are empty lists
L1  for each template edge point (x, b) do
L2      append the offset c - x to R[b]
L3  A ← 0 on the W by H grid
L4  for each image edge point (y, b) do
L5      for each offset r in R[b] do
L6          p ← y + r
L7          if p is inside the grid then A[p] ← A[p] + 1
L8  return the cell p with the largest A[p], and A
```

Lines L1 and L2 build the R-table once for each template. Lines L3 to L7 are the voting. Line L8 takes the peak. A real detector takes all the local maxima above a vote threshold, after [non-maximum suppression](/non-maximum-suppression/), to find several copies.

**Rotation and scale.** Ballard extends the accumulator to four parameters $(p, \theta, s)$. For a rotation $\theta$ and a scale $s$, the shape edge point that now has bin $b$ had bin $b - \theta$ in the template, so line L5 reads $R[(b - k) \bmod B]$ for a rotation of $k$ bins, and line L6 becomes $p \leftarrow y + s\, \mathrm{rot}_\theta(r)$. The code does this in `vote_rotations`, with one accumulator for each pair $(k, s)$. It is exact for rotations by multiples of 90 degrees. For other angles, the rounding of the offsets and the width of the bins spread the votes.

## Example

The template is a $7 \times 7$ image with a $3 \times 3$ square of value 1 at $u, v \in \{2, 3, 4\}$, and $c = (3, 3)$, the center of the square. With $\tau = 1$, every pixel of the $5 \times 5$ block around the square has a nonzero gradient, except the center, so $m = 24$. The gradient points to the square. The counts in the bins 0 to 7 are 4, 2, 4, 2, 4, 2, 4, 2: the sides give the bins of the axis directions, and the corners give the diagonal bins. Bin 2 (gradient down) holds the points $(2, 1)$, $(3, 1)$, $(4, 1)$ and $(3, 2)$ above the square, so

$$R[2] = \{(1, 2), (0, 2), (-1, 2), (0, 1)\}.$$

Paste the template into a blank image of $12 \times 10$ pixels with its top left pixel at $t = (4, 2)$. The point $(3, 2)$ of the template is now at $(7, 4)$, with bin 2. It votes at $(8, 6)$, $(7, 6)$, $(6, 6)$ and $(7, 5)$. Only the last one is the true center $c + t = (7, 5)$. The 24 edge points of the copy all vote at $(7, 5)$, so the peak is $A[(7, 5)] = 24 = m$. The second largest count in $A$ is 6, at cells next to the peak. The tests check these numbers.

## Correctness

The proof in the correctness file shows three facts.

**Theorem 1 (the votes count matching pairs).** Lines L1 to L7 compute exactly the $A$ of the problem statement: each pair of a template edge point and an image edge point with the same bin adds one vote, at $y + c - x$, if that cell is inside the grid.

**Theorem 2 (a translated copy gives a peak of at least $m$).** If the image edge points include $(x_i + t, b_i)$ for all $m$ template edge points and $c + t$ is inside the grid, then $A[c + t] \ge m$. If the image edge points are exactly these $m$ points, then $A[c + t] = m$. This holds when the image is the template moved by $t$ on a blank background and the template has a blank border of 2 pixels, since the Sobel gradient of a pixel depends only on its $3 \times 3$ neighborhood.

**Theorem 3 (rotation by 90 degrees).** Rotating the image by 90 degrees rotates the Sobel gradient by 90 degrees and moves each bin by $B/4$. So the rotated copy gives $A_{B/4}[c' ] \ge m$ in the accumulator for the rotation of $B/4$ bins, where $c'$ is the rotated reference point.

What is not claimed: the peak at $c + t$ is not always the largest cell. Clutter can put more votes on another cell, and the bins make some wrong pairs agree. That the peak wins in practice is a heuristic, supported by experiments.

## Complexity

In the [real RAM](/real-ram/), lines L1 and L2 cost $O(m)$, and the edge detection costs $O(W H)$ for each image. Line L3 costs $O(W H)$. An image edge point with bin $b$ makes $|R[b]|$ votes, so lines L4 to L7 cost $\sum_j |R[b_j]| \le e\, k \le e\, m$, where $k = \max_b |R[b]|$. The peak search in line L8 costs $O(W H)$. The space is $O(W H)$ for $A$ and $O(m)$ for the table.

With $n_\theta$ rotations and $n_s$ scales, time and accumulator space grow by the factor $n_\theta n_s$. This is the main cost of the method, and it is why most systems search position only, or a coarse grid of rotations and scales.

## Properties

- **Any shape.** The shape needs no formula. Holes and several separate parts are allowed, since the table lists all the edge points.
- **Robust to occlusion.** A copy with only a part of its outline visible still gets one vote from each visible edge point. The peak is lower but in the correct place.
- **Linear in the votes.** The accumulator of an image is the sum of the accumulators of its edge points. Two copies of the shape give two peaks.
- **Invariant to brightness change.** The Sobel gradient does not change when a constant is added to the image, and its direction does not change when the image is multiplied by a positive constant. So the bins are the same. The threshold $\tau$ must be scaled with the contrast.
- **Not invariant to rotation and scale.** The basic table is for one rotation and one scale. Each extra rotation or scale needs one more accumulator.

## Variants and improvements

- **Weighted votes.** Votes can be weighted by the gradient magnitude, or by how rare the direction is in the template, so that frequent directions count less.
- **Coarse to fine.** A coarse accumulator finds candidate cells, then a finer one refines them.
- **Rotation without a full 4D search.** Pairs of edge points give a rotation invariant (the difference of their gradient directions), at a higher voting cost. This is a heuristic with no exact guarantee.
- **Votes from learned parts.** The [implicit shape model](/implicit-shape-model/) replaces the edge points by local features matched to a codebook, and each codebook entry stores the center offsets seen in the training images. It uses the same voting step for categories of objects.
- **Votes from features.** With local features such as [SIFT](/sift/), one match gives position, rotation and scale, and a coarse Hough grid over these four parameters groups the matches before [alignment](/alignment-recognition/) checks them.

## When to use it

Use the generalized Hough transform to find a known rigid shape of fixed size and orientation in an image, for example a part in industrial inspection, a logo, or a mark on a document. It works well when the outline is clear and when parts of it can be hidden. For a shape with a formula (a line or a circle), the standard [Hough transform](/hough-transform/) has fewer parameters. For a gray-level pattern, [template matching](/template-matching/) uses all the pixels, not only the edges. For an edge template under small deformation, [chamfer matching](/chamfer-distance/) is smoother. For objects with textured surfaces, local features with [geometric hashing](/geometric-hashing/) or alignment handle rotation and scale at lower cost.

## Pitfalls

- **Bins too fine or too coarse.** Noise moves the gradient direction across the bin boundary, and the vote goes to the wrong table entry. Many bins make this happen often. Few bins make each entry list long and add wrong votes. Votes into the two nearest bins help.
- **Gradient sign.** A dark shape on a light background has the opposite gradient of a light shape on a dark background. The bins differ by $B/2$, and the template does not match. Use the direction modulo $\pi$ if both polarities can occur.
- **Cost of the extension.** Rotation and scale multiply the time and the memory. A full search over 36 angles and 10 scales costs 360 times more than position alone.
- **Peak spread.** Rounding, the bin width and small changes of the shape spread the votes over several cells. Smooth the accumulator, or sum it over a small window, before the peak search.
- **Clutter in textured areas.** Many edge points in a textured area give many random votes, and a false peak can win. Check each peak, for example by counting how many template edge points fall on image edge points at the found pose.

## Implementations

The Python code has the integer Sobel gradient, the direction bins, the R-table, the voting, the peak with the tie rule of this page, and the extension to rotation by bins and to scale. It also has helpers to rotate an image by 90 degrees and to paste a template into an image. The tests check the example of this page, a translated non-symmetric template with and without clutter far from it, the equality of the votes with a direct count over all pairs, the rotation by 90 degrees through the bin shift, the scaled offsets, and the invariance of the edge points to a brightness change.

## History

The Hough transform comes from a 1962 patent of Paul Hough for bubble chamber tracks. Duda and Hart (1972) gave the bounded parameterization for lines and extended the voting to other analytic curves. Ballard (1981) removed the need for a formula: the R-table from the gradient direction to the offsets of a reference point describes any shape, and the same table, rotated and scaled, gives the search over rotation and scale. Illingworth and Kittler (1988) surveyed the many variants. Later, Leibe, Leonardis and Schiele used the same voting for object categories in the implicit shape model.

## References
