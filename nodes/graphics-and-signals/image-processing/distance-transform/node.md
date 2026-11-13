---
tag: FA4GFT
kind: problem
slug: distance-transform
name: Distance transform
aliases:
- distance map
area: graphics-and-signals/image-processing
level: advanced
summary: For each pixel of a binary image, compute the distance to the nearest feature pixel, for a chosen metric such as city block, chessboard, chamfer or Euclidean.
prereqs: [digital-image, metric-space]
see_also: [felzenszwalb-distance-transform, chamfer-distance, fast-marching-method, voronoi-diagram, medial-axis, image-skeletonization, signed-distance-function, watershed-segmentation]
sources:
  - paper: doi:10.1145/321356.321357
    title: Azriel Rosenfeld and John L. Pfaltz, Sequential operations in digital picture processing, Journal of the ACM 13(4), 471 to 494, 1966
    locator: the distance to a set and its computation by two sequential raster passes (general locator)
  - paper: doi:10.1016/s0734-189x(86)80047-0
    title: Gunilla Borgefors, Distance transformations in digital images, Computer Vision, Graphics, and Image Processing 34(3), 344 to 371, 1986
    locator: the chamfer distances and their errors against the Euclidean distance (general locator)
  - paper: doi:10.4086/toc.2012.v008a019
    title: Pedro F. Felzenszwalb and Daniel P. Huttenlocher, Distance transforms of sampled functions, Theory of Computing 8(19), 415 to 428, 2012
    locator: Section 1 (the distance transform of a sampled function), Section 2 (the linear time squared Euclidean transform)
  - paper: doi:10.1145/1322432.1322434
    title: Ricardo Fabbri, Luciano da F. Costa, Julio C. Torelli and Odemir M. Bruno, 2D Euclidean distance transform algorithms, a comparative survey, ACM Computing Surveys 40(1), 1 to 44, 2008
    locator: the whole survey, which compares the exact and approximate EDT algorithms (general locator)
  - paper: doi:10.1109/tpami.2003.1177156
    title: Calvin R. Maurer, Rensheng Qi and Vijay Raghavan, A linear time algorithm for computing exact Euclidean distance transforms of binary images in arbitrary dimensions, IEEE Transactions on Pattern Analysis and Machine Intelligence 25(2), 265 to 270, 2003
    locator: the whole paper (general locator)
  - paper: doi:10.1016/0146-664x(80)90054-4
    title: Per-Erik Danielsson, Euclidean distance mapping, Computer Graphics and Image Processing 14(3), 227 to 248, 1980
    locator: the vector propagation method (general locator)
  - paper: doi:10.1016/0031-3203(94)90133-3
    title: Toyofumi Saito and Jun-Ichiro Toriwaki, New algorithms for Euclidean distance transformation of an n-dimensional digitized picture with applications, Pattern Recognition 27(11), 1551 to 1565, 1994
    locator: the separable exact squared EDT, one axis at a time (general locator)
  - paper: doi:10.1007/0-306-47025-x_36
    title: Arnold Meijster, Jos B. T. M. Roerdink and Wim H. Hesselink, A general algorithm for computing distance transforms in linear time, in Mathematical Morphology and its Applications to Image and Signal Processing, Kluwer, 331 to 340
    locator: the two phase linear time algorithm for the Euclidean, city block and chessboard distances (general locator)
---

The distance transform of a binary image gives every pixel its distance to the nearest feature pixel. The features are a chosen set of pixels: often the background, so that each foreground pixel learns how deep it lies inside its shape, or the edge pixels of an edge map. The answer depends on the metric. The city block and chessboard distances count grid steps, the chamfer distances add small integer weights for edge and diagonal steps, and the Euclidean distance is the straight line distance between pixel centers. All of them can be computed in time linear in the number of pixels, which is optimal, and the exact Euclidean one by a separable method such as the [Felzenszwalb-Huttenlocher transform](/felzenszwalb-distance-transform/).

## In plain words

Color some pixels of a picture black. For every other pixel, we want to know how far away the nearest black pixel is. The result is a new picture in which each pixel holds a number: zero on the black pixels, and larger values the farther you go from them.

How far depends on how you measure. You can count the steps a rook would need, or the steps a king would need, or the straight line distance. Each choice gives a slightly different picture, and each has a fast method. The result is useful for growing and shrinking shapes by a round amount, for finding the middle line of a shape, for telling a robot how much room it has, and for matching outlines.

## Definition

**Input.** A rectangle of pixels $R = \{0, \dots, W-1\} \times \{0, \dots, H-1\}$ with the pixel centers at the integer points, a set $S \subseteq R$ of feature pixels, and a metric $\rho$ on $\mathbb{Z}^2$.

**Output.** For every $p \in R$,

$$\mathrm{DT}_S(p) = \min_{q \in S} \rho(p, q),$$

and $\mathrm{DT}_S(p) = \infty$ when $S$ is empty. With $S$ the background of a binary image $X$, $\mathrm{DT}$ is the distance of each pixel of $X$ to the complement, which is 0 on the background; this is the usual distance transform of a shape.

**Metrics.** With $(\Delta x, \Delta y) = p - q$, $M = \max(|\Delta x|, |\Delta y|)$ and $m = \min(|\Delta x|, |\Delta y|)$:

| metric | $\rho(p, q)$ | ball | exact computation |
|---|---|---|---|
| city block, $d_4$ | $\lvert\Delta x\rvert + \lvert\Delta y\rvert$ | diamond | integer |
| chessboard, $d_8$ | $M$ | square | integer |
| chamfer $(a, b)$ | $a(M - m) + bm$ | octagon | integer, an approximation of $a$ times the Euclidean distance |
| Euclidean | $\sqrt{\Delta x^2 + \Delta y^2}$ | digital disk | the squared value is an integer |

The Euclidean transform is usually computed and stored squared, so that it stays exact in integers.

**Pixels outside the image.** The definition takes the minimum over $S \subseteq R$ only. If the shape continues past the border, the result near the border depends on that choice, and an application must decide whether the outside is feature, not feature, or padded.

## Variants

- **The feature transform.** Return, for each pixel, a nearest feature pixel $\arg\min_q \rho(p, q)$ as well as the distance. This is the discrete [Voronoi diagram](/voronoi-diagram/) of $S$ on the grid. Ties need a rule.
- **The signed distance transform.** Positive outside a shape and negative inside, or the reverse, from one transform of the shape and one of its complement. This is the discrete [signed distance function](/signed-distance-function/), used in [level set methods](/level-set-method/) and in font and shape rendering.
- **The distance transform of a sampled function.** Replace the 0 on the features by any cost: $D_f(p) = \min_q (\rho(p, q) + f(q))$. For $\rho$ the squared Euclidean distance this is the min-convolution with a paraboloid, used in part based object detection; Felzenszwalb and Huttenlocher solve it in linear time.
- **Geodesic or constrained distance.** Paths must stay inside a mask, as around obstacles. This is a shortest path problem on the grid graph, solved by [breadth-first search](/breadth-first-search/) for unit steps or [Dijkstra](/dijkstra/) for weights.
- **Continuous distance with a speed.** The distance as the solution of the [eikonal equation](/eikonal-equation/) $|\nabla u| = 1/F$, solved on the grid by the [fast marching method](/fast-marching-method/). With $F = 1$ it approximates the Euclidean distance, with small errors from the grid.
- **More dimensions and other grids.** Voxel grids in 3D for medical images, and pixels with different width and height. The separable exact methods extend directly, one axis at a time.

## Examples

A 7 by 5 image with one feature pixel at $(3, 2)$, under four metrics. The values show the shape of each ball.

```text
city block             chessboard             chamfer 3-4            squared Euclidean
5 4 3 2 3 4 5          3 2 2 2 2 2 3          11  8  7  6  7  8 11   13  8  5  4  5  8 13
4 3 2 1 2 3 4          3 2 1 1 1 2 3          10  7  4  3  4  7 10   10  5  2  1  2  5 10
3 2 1 0 1 2 3          3 2 1 0 1 2 3           9  6  3  0  3  6  9    9  4  1  0  1  4  9
4 3 2 1 2 3 4          3 2 1 1 1 2 3          10  7  4  3  4  7 10   10  5  2  1  2  5 10
5 4 3 2 3 4 5          3 2 2 2 2 2 3          11  8  7  6  7  8 11   13  8  5  4  5  8 13
```

At the corner $(0, 0)$, with $(\Delta x, \Delta y) = (3, 2)$, the distances are 5, 3, $11/3 \approx 3.67$ and $\sqrt{13} \approx 3.61$. The pixels within distance 2 of the feature form a diamond of 13 pixels for the city block distance, a 5 by 5 square of 25 pixels for the chessboard distance, and 13 pixels for the Euclidean distance, a digital disk whose squared distances are at most 4.

With many features the transform is the minimum of such cones, one per feature. The [Felzenszwalb-Huttenlocher page](/felzenszwalb-distance-transform/) and the [chamfer page](/chamfer-distance/) each work an example with two features.

## Known algorithms

| algorithm | metric | time | exact | notes |
|---|---|---|---|---|
| brute force | any | $O(WH \cdot \lvert S\rvert)$ | yes | the reference for tests |
| multi-source [breadth-first search](/breadth-first-search/) | $d_4$, $d_8$ | $\Theta(WH)$ | yes | a queue seeded with all features |
| two raster passes, Rosenfeld and Pfaltz (1966) | $d_4$, $d_8$ | $\Theta(WH)$ | yes | the first sequential method |
| [chamfer transform](/chamfer-distance/), Borgefors (1986) | chamfer $(a, b)$ | $\Theta(WH)$ | for its own metric | with 3 and 4, within about 6% of Euclidean |
| vector propagation, Danielsson (1980) | Euclidean | $\Theta(WH)$ | not for every configuration | passes that carry the offset to the nearest feature |
| separable squared EDT, Saito and Toriwaki (1994) | Euclidean | more than linear in the worst case | yes | one axis at a time |
| Meijster, Roerdink and Hesselink (2000) | Euclidean, $d_4$, $d_8$ | $\Theta(WH)$ | yes | two phases, columns then rows |
| Maurer, Qi and Raghavan (2003) | Euclidean | $\Theta(WH)$ | yes | partial Voronoi diagrams per line, any dimension |
| [Felzenszwalb and Huttenlocher](/felzenszwalb-distance-transform/) (2004, 2012) | squared Euclidean, also of sampled functions | $\Theta(WH)$ | yes | lower envelope of parabolas per line |
| [fast marching method](/fast-marching-method/) | eikonal, with a speed | $O(WH \log(WH))$ | no, a grid approximation | a priority queue, like Dijkstra |
| [Dijkstra](/dijkstra/) on the grid graph | path metrics, with obstacles | $O(WH \log(WH))$ | yes, for the graph metric | the general fallback |

Fabbri, Costa, Torelli and Bruno (2008) compare the Euclidean algorithms in a survey with tests on many images.

## Bounds

- **Lower bound.** Every pixel of the output must be written, and every pixel of the input can change the answer, so $\Omega(WH)$ time is needed. The linear time exact algorithms are optimal up to the constant, for every metric in the table above.
- **Exact Euclidean needs more than local propagation.** The nearest feature of a pixel is not always the nearest feature of one of its neighbors in a fixed small mask, so any method that copies offsets only from a few neighbors can be wrong for some images. The exact linear methods avoid this by solving each line with a lower envelope or a Voronoi construction.
- **The error of the chamfer metrics.** For $(3, 4)$ the scaled result $c/3$ lies between $\tfrac{2\sqrt{2}}{3}$ and $\tfrac{\sqrt{10}}{3}$ times the Euclidean distance, and both bounds are reached; the [chamfer page](/chamfer-distance/) proves it. No integer 3 by 3 mask is exact, since the Euclidean ball is not a polygon.

## Reductions

- **Morphology with disks.** The [dilation](/morphological-dilation/) of $S$ by the digital disk of radius $r$ is $\{p : \mathrm{DT}_S(p)^2 \le r^2\}$, and the [erosion](/morphological-erosion/) of a shape $X$ by the same disk is the set where the transform of the complement exceeds $r$. One transform answers the question for every radius at once, in $\Theta(WH)$, while a direct dilation costs $\Theta(r^2)$ per pixel.
- **The discrete Voronoi diagram.** The feature transform labels each pixel with its nearest feature, which is the [Voronoi diagram](/voronoi-diagram/) of $S$ sampled on the grid.
- **Skeletons.** The ridges of the transform of a shape, the pixels where the distance is a local maximum across the shape, approximate the [medial axis](/medial-axis/); see [image skeletonization](/image-skeletonization/) for the discrete methods.
- **The Hausdorff distance and edge matching.** For two edge sets $A$ and $B$, $\max_{a \in A} \mathrm{DT}_B(a)$ is the directed [Hausdorff distance](/hausdorff-distance/), so one transform of $B$ answers every placement of $A$ by lookups.
- **One dimension.** The 1D squared Euclidean transform of a sampled function is a lower envelope of parabolas, a case of the [lower envelope of segments](/lower-envelope-of-segments/) with one crossing per pair, and also a monotone [convex hull trick](/convex-hull-trick/).

## Applications

- **Mathematical morphology.** Fast erosion, dilation, opening and closing by disks of any radius; see [mathematical morphology](/mathematical-morphology/).
- **Separating touching objects.** The transform of a binary mask has one peak per round object; [watershed segmentation](/watershed-segmentation/) on its negative splits touching cells or grains.
- **Robotics and path planning.** The distance to the nearest obstacle gives the clearance of each cell, used to keep paths away from walls and to inflate obstacles by the robot radius.
- **Graphics.** Signed distance fields render fonts and shapes sharply at any scale, and drive outlines, glows and collision tests.
- **Shape analysis.** Skeletons, thickness measures and shape descriptors in medical and industrial imaging.
- **Matching.** A transform of an edge map turns the cost of placing a model edge set into a sum of lookups, as in [template matching](/template-matching/) with edges.

## References
