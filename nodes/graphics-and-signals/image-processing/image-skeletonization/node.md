---
tag: DD2KYN
kind: problem
slug: image-skeletonization
name: Image skeletonization
area: graphics-and-signals/image-processing
level: advanced
summary: Reduce a binary shape to a thin set of pixels along its middle, ideally one pixel wide and with the same connectivity as the shape.
prereqs: [digital-image, connected-component-labeling, morphological-erosion]
see_also: [zhang-suen-thinning, medial-axis, distance-transform, hit-or-miss-transform, morphological-opening, felzenszwalb-distance-transform, chamfer-distance, mathematical-morphology]
sources:
  - paper: doi:10.1145/357994.358023
    title: T. Y. Zhang and C. Y. Suen, A fast parallel algorithm for thinning digital patterns, Communications of the ACM 27(3), 236 to 239, 1984
    locator: the two subiteration parallel thinning algorithm
  - paper: doi:10.1109/34.161346
    title: Louisa Lam, Seong-Whan Lee and Ching Y. Suen, Thinning methodologies, a comprehensive survey, IEEE Transactions on Pattern Analysis and Machine Intelligence 14(9), 869 to 885, 1992
    locator: the whole survey, on the goals of thinning and the sequential and parallel algorithms (general locator)
  - book: isbn:9783540429883
    title: Pierre Soille, Morphological Image Analysis, Principles and Applications, second edition, Springer, 2003
    locator: Chapter 5, Hit-or-miss and Skeletons (the morphological skeleton, thinning and thickening, and skeletons by distance functions)
  - paper: doi:10.1145/5666.5670
    title: H. E. Lü and P. S. P. Wang, A comment on a fast parallel algorithm for thinning digital patterns, Communications of the ACM 29(3), 239 to 242, 1986
    locator: the change of the neighbor count test that keeps diagonal lines two pixels thick
---

Image skeletonization turns a binary shape into a thin set of pixels that runs along its middle: its skeleton. The skeleton should be one pixel wide, keep the shape's connectivity and holes, lie near the center of the shape, and keep a branch for each limb. On a square grid these goals conflict, and each method gives up some of them. Thinning methods peel boundary pixels in rounds and keep connectivity, as in [Zhang-Suen thinning](/zhang-suen-thinning/). Morphological methods take a union of differences of erosions and openings; they are centered and let the shape be rebuilt, but are not always thin or connected. Distance based methods keep the ridges of the [distance transform](/distance-transform/). The continuous version of the problem is the [medial axis](/medial-axis/) of a shape in the plane.

## In plain words

Think of a shape drawn with a thick marker, such as a letter on a scanned page. We want the thin line that a pen would draw down the middle of the stroke. That line is shorter to store, easier to follow and easier to compare, but it should still show how the parts connect: a ring should stay a ring, and a letter T should keep three arms.

One way is to peel the shape like an onion. In each round, remove the outer pixels whose removal does not cut the shape apart and that are not the end of an arm. Stop when nothing more can go. Another way is to find, for each pixel, how far it is from the edge, and keep the pixels that are farther than their neighbors on both sides.

## Definition

**Input.** A binary image, with a finite set $X$ of foreground pixels on the grid $\mathbb{Z}^2$ and a choice of connectivity: 8-connectivity for the foreground with 4-connectivity for the background, or the reverse.

**Output.** A set $K \subseteq X$, the skeleton, that meets some of these goals:

1. **Topology.** $K$ has the same number of connected components as $X$, and the complement of $K$ has the same number of components as the complement of $X$: no part is cut, no hole is filled, and no hole is made.
2. **Thin.** $K$ is one pixel wide: no pixel of $K$ is a simple pixel other than an end point, where a pixel is simple if removing it does not change the topology in the sense of goal 1.
3. **Centered.** Each pixel of $K$ is near the middle of the shape, close to the [medial axis](/medial-axis/) of the continuous shape that $X$ samples.
4. **Limbs.** Each significant limb of $X$ gives one branch of $K$, and small bumps of the boundary do not give branches.
5. **Rebuilt.** With a radius stored at each pixel of $K$, $X$ is the union of the disks centered at $K$.

Goals 1, 2 and 4 are local tests on 3 by 3 neighborhoods for thinning. Goal 3 and goal 5 refer to distances, and goal 4 needs a scale below which a bump is noise. No method on the square grid meets all five for every shape: a 2 by 2 square has no centered pixel, and any choice of one of its four pixels breaks the symmetry.

## Variants

- **Thinning by peeling.** Remove simple pixels that are not end points, layer by layer, until none is left. Parallel algorithms decide a whole layer at once from the previous image and split each round into subiterations so that two sides of a two pixel thick line do not both vanish; sequential algorithms remove pixels one at a time in a fixed order and depend on that order.
- **The morphological skeleton.** For a structuring element $B$ that contains the origin and the shrunken images $X \ominus nB$, with $nB$ the dilation of $B$ by itself $n - 1$ times,

  $$S_n = (X \ominus nB) \setminus \bigl((X \ominus nB) \circ B\bigr), \qquad K = \bigcup_{n \ge 0} S_n,$$

  and $X = \bigcup_n S_n \oplus nB$. This uses only [erosion](/morphological-erosion/) and [opening](/morphological-opening/), and it rebuilds $X$ exactly, but $K$ can be two pixels thick and is often not connected. With $B$ the 3 by 3 square, $S_n$ is the set of centers of the maximal chessboard disks of radius $n$.
- **Ridges of the distance transform.** Keep the pixels whose distance to the background is a local maximum in some direction, or the centers of maximal disks for a chosen metric. These are centered and rebuild the shape, and connecting them into one piece needs an extra step.
- **Pruning.** Remove short branches, the spurs that come from noise on the boundary, by deleting end points for a fixed number of rounds or by a measure of how much of the shape a branch explains.
- **Three dimensions.** On voxel grids, a skeleton can be a set of surfaces or a set of curves, and the tests for simple voxels use 26 neighbors.
- **Gray images.** Thin the ridges of a gray image directly, or threshold first; see [image thresholding](/image-thresholding/).

## Examples

A 7 by 5 rectangle, a 6 by 4 rectangle and an L shape, each with its morphological skeleton for the 3 by 3 square, where a digit $n$ marks a pixel of $S_n$, and its Zhang-Suen skeleton:

```text
shape         morphological   Zhang-Suen
.#######.     .........       .........
.#######.     .........       .........
.#######.     ...222...       ...##....
.#######.     .........       .........
.#######.     .........       .........

.######.      ........        ........
.######.      ..1111..        ...##...
.######.      ..1111..        ........
.######.      ........        ........

.########.    ..........      ..........
.########.    ..111111..      ..#####...
.########.    ..1.......      ..#.......
.###......    ..1.......      ..#.......
.###......    ..1.......      ..........
.###......    ..........      ..........
```

The grids omit the background border rows above and below. On the 7 by 5 rectangle, the morphological skeleton is the 3 pixel middle row, the centers of the three chessboard disks of radius 2 that fill the rectangle. On the 6 by 4 rectangle it is a 4 by 2 block: the rectangle has no middle row, so the skeleton is two pixels thick. Thinning instead gives a short line in both cases, at the cost of the exact rebuild. On the L shape, both give a connected skeleton with two arms, and the thinned arms are shorter than the morphological ones. In each case, dilating each $S_n$ by $nB$ and taking the union gives back the shape.

The 2 by 2 square shows the limit of symmetric peeling: each of its pixels has the same neighborhood up to a rotation, so a rule that does not depend on the orientation must keep all four or delete all four. [Zhang-Suen thinning](/zhang-suen-thinning/) deletes all four in its first subiteration and so breaks goal 1.

## Known algorithms

| method | goals met | time | notes |
|---|---|---|---|
| [Zhang-Suen thinning](/zhang-suen-thinning/) (1984) | thin in most places; connectivity except for small shapes | $O(WH)$ per iteration, about half the thickness iterations | two parallel subiterations; a 2 by 2 square vanishes |
| Lü and Wang (1986) | as Zhang-Suen, and keeps 2 pixel diagonals | the same | changes the neighbor count test of Zhang-Suen |
| Guo and Hall (1989) and other parallel thinning | topology, thin | $O(WH)$ per iteration | other subiteration or subfield schemes; see the survey of Lam, Lee and Suen |
| sequential thinning by simple pixels | topology, thin | $O(WH)$ with a queue of border pixels | depends on the scan order |
| morphological skeleton (Lantuéjoul) | rebuilds exactly, centered | $O(WH \cdot t \cdot \lvert B\rvert)$ for thickness $t$ | not thin, not connected in general; Soille, Chapter 5 |
| ridges of the Euclidean [distance transform](/distance-transform/) | centered, rebuilds | $\Theta(WH)$ for the transform, by [Felzenszwalb-Huttenlocher](/felzenszwalb-distance-transform/) | needs a step to restore connectivity |
| ridges of the [chamfer transform](/chamfer-distance/) | centered for the chamfer metric | $\Theta(WH)$ | integer and fast; less isotropic |
| the [medial axis](/medial-axis/) of the boundary polygon | continuous, exact for the polygon | $O(n \log n)$ for $n$ boundary vertices | then sample it back on the grid |

## Bounds

- **Reading the image.** Every pixel can matter, so $\Omega(WH)$ time is needed.
- **Iterations of peeling.** A parallel thinning algorithm removes at most one layer of boundary per iteration, so a shape of thickness $t$ needs about $t/2$ iterations, and a naive implementation costs $O(WH \cdot t)$. Implementations that keep a list of the current border pixels look only at pixels next to the pixels just removed.
- **No method has all the goals.** The 2 by 2 square above shows that symmetry, connectivity and a centered one pixel result cannot all hold for every shape on the square grid. The 6 by 4 rectangle shows that an exact rebuild by disks centered on the grid and one pixel width can conflict.

## Reductions

- **To the distance transform.** The centers of the maximal disks of $X$ for a metric are the local maxima of the transform of the complement in a suitable sense, so a [distance transform](/distance-transform/) turns the centered part of the problem into a local test.
- **To the medial axis.** Trace the boundary of $X$ to a polygon and compute its [medial axis](/medial-axis/), then draw it back on the grid. This gives a centered and connected result for each simply connected component, at the cost of the tracing step.
- **To the hit-or-miss transform.** One thinning step with a structuring element pair $(B_1, B_2)$ is $X \setminus \mathrm{HMT}(X; B_1, B_2)$; cycling through the rotations of a few pairs until nothing changes gives a thinning built from the [hit-or-miss transform](/hit-or-miss-transform/).

## Applications

- **Character recognition.** Thinned strokes give a writer independent shape for letters and digits, the use that Zhang and Suen had in mind.
- **Fingerprints.** The ridge skeleton gives the minutiae, the ends and the forks of the ridges, used to match prints.
- **Networks in images.** Blood vessels, roads, rivers, neurons and cracks reduce to graphs of branches and junctions, for length and branching measures.
- **Shape description.** The skeleton graph is a compact description of a shape for matching and retrieval, and the radii along it give its thickness.
- **Robot planning.** The skeleton of the free space is a road map of paths that keep away from obstacles.

## References
