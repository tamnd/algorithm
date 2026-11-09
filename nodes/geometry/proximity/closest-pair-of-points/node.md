---
tag: C3REVA
kind: problem
slug: closest-pair-of-points
name: Closest pair of points
aliases:
- closest pair problem
- minimum-distance pair
- closest pair
area: geometry/proximity
level: core
summary: Find the pair of the n input points in the plane with the smallest Euclidean distance.
prereqs: [euclidean-distance, point-and-vector, real-ram]
see_also: [closest-pair-divide-and-conquer, closest-pair-sweep-line, randomized-closest-pair, closest-pair-lower-bound, all-nearest-neighbors, bichromatic-closest-pair, farthest-pair, proximity-problems]
sources:
  - paper: doi:10.1109/SFCS.1975.8
    title: Michael Ian Shamos and Dan Hoey, Closest-point problems, 16th Annual Symposium on Foundations of Computer Science, 1975, 151-162
    locator: the closest pair problem in the plane, the O(n log n) divide and conquer algorithm, and its relation to the Voronoi diagram
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 5, Proximity, fundamental algorithms (problem statements, the lower bound by element uniqueness, and the closest pair algorithms)
  - paper: "Michael O. Rabin, Probabilistic algorithms, in J. F. Traub (ed.), Algorithms and Complexity, New Directions and Recent Results, Academic Press, 1976, 21-39"
    locator: the randomized closest pair algorithm with expected linear time using a grid and the floor function
  - paper: doi:10.1145/800061.808735
    title: "Michael Ben-Or, Lower bounds for algebraic computation trees, Proceedings of the 15th Annual ACM Symposium on Theory of Computing (STOC 1983), 80-86"
    locator: the lower bound by the number of connected components, applied to element distinctness
  - paper: "Michiel Smid, Closest-point problems in computational geometry, in J.-R. Sack and J. Urrutia (eds.), Handbook of Computational Geometry, Elsevier, 2000, 877-935"
    locator: the survey sections on the static closest pair problem, its lower bounds and models, and the dynamic version
  - book: isbn:9780262046305
    title: Cormen, Leiserson, Rivest and Stein, Introduction to Algorithms, fourth edition
    locator: Chapter 33, Section 33.4, Finding the closest pair of points
---

The closest pair problem asks, for $n$ points in the plane, for two of them at the smallest [Euclidean distance](/euclidean-distance/). Checking all $\binom{n}{2}$ pairs takes $\Theta(n^2)$ time; Shamos and Hoey showed in 1975 that $O(n \log n)$ is enough, and an $\Omega(n \log n)$ lower bound in the [algebraic decision tree](/algebraic-decision-tree/) model shows that this is optimal there. With the floor function and randomization, Rabin's grid method solves it in $O(n)$ expected time, which shows how much the answer depends on the model. It is the simplest of the [proximity problems](/proximity-problems/) and the usual first example of [divide and conquer](/divide-and-conquer-paradigm/) in geometry.

## In plain words

You have a map with many dots, such as planes on a radar screen, and you want the two that are nearest to each other, for example to warn of a possible collision.

The obvious method measures the gap between every two dots and keeps the smallest. That is fine for a few hundred dots and hopeless for a million, because the number of pairs grows with the square of the number of dots.

The better methods use the fact that a close pair is local. If you already know a small gap, any better pair must sit in a small region, and only a few dots fit in a small region without being closer than the gap you know. Sorting the dots, sweeping across them, or dropping them into a grid of boxes all exploit this.

## Definition

**Input.** A list $P = (p_1, \ldots, p_n)$ of $n \ge 2$ points $p = (x, y)$ in $\mathbb{R}^2$. Points may repeat and may be collinear. For exact algorithms the coordinates are integers or rationals.

**Output.** Two indices $i \ne j$ such that

$$\|p_i - p_j\| = \delta(P) = \min_{a \ne b} \|p_a - p_b\|,$$

and usually the value $\delta(P)$ or its square $\delta^2(P)$. If two input points are equal, $\delta(P) = 0$. When several pairs reach the minimum, any one of them is a correct answer. For $n < 2$ there is no pair, and implementations return an empty answer.

**Exactness.** Because $t \mapsto t^2$ is increasing on $t \ge 0$, comparing $\|p - q\|$ with $\|r - s\|$ is the same as comparing the squared distances $(p_x - q_x)^2 + (p_y - q_y)^2$ and $(r_x - s_x)^2 + (r_y - s_y)^2$, which are exact integers for integer input. Taking square roots in floating point can merge different distances: for $a = (0, 0)$, $b = (10^8, 1)$, $c = (-10^8, 0)$, $\|a - b\|^2 = 10^{16} + 1$ and $\|a - c\|^2 = 10^{16}$, but both square roots round to the same double $10^8$. All algorithms on the linked pages compare squared distances.

**Model.** Deterministic algorithms are analyzed on the [real RAM](/real-ram/) with the four arithmetic operations and comparisons. The lower bound uses [algebraic decision trees](/algebraic-decision-tree/) (and [algebraic computation trees](/algebraic-computation-tree/)), in which the floor function is not allowed. The randomized linear-time algorithm needs floor and constant-time hashing, which is outside that model.

## Variants

- **One dimension.** For numbers on a line, sort them; the closest pair is two neighbours in sorted order. This takes $O(n \log n)$ time and is optimal in the algebraic decision tree model by the same lower bound.
- **Higher dimensions.** For points in $\mathbb{R}^d$ with $d$ fixed, divide and conquer (Bentley and Shamos, 1976) and the randomized grid both extend, with $O(n \log n)$ and $O(n)$ expected time respectively; the constants grow exponentially with $d$.
- **Other metrics.** The same algorithms work for the $L_1$ and $L_\infty$ distances, with the packing constant changed.
- **Decision version.** Given $\varepsilon$, is there a pair at distance less than $\varepsilon$? With floor this is easy in $O(n)$ expected time by hashing grid cells of side $\varepsilon$, and the randomized algorithms build on it.
- **All nearest neighbors.** Find, for every point, its nearest other point: [all nearest neighbors](/all-nearest-neighbors/). The closest pair is the smallest of these $n$ distances.
- **Two colours.** Find the closest red-blue pair: [bichromatic closest pair](/bichromatic-closest-pair/). This is harder; the packing argument fails because two red points may be arbitrarily close.
- **k closest pairs.** Report the $k$ smallest distances; possible in $O(n \log n + k)$ time.
- **Dynamic.** Keep the closest pair while points are inserted and deleted. In fixed dimension this is possible in $O(\log n)$ worst-case time per update (Bespamyatnikh, 1998), as surveyed by Smid.
- **Farthest pair.** The opposite question, the two points at the largest distance, is the [farthest pair](/farthest-pair/) problem, solved by the convex hull and rotating calipers.

## Examples

**Eight points.** For

$$P = \{(0,0), (1,9), (3,6), (4,2), (5,3), (7,0), (8,8), (9,5)\}$$

the closest pair is $(4,2), (5,3)$ with $\delta^2 = 2$, so $\delta = \sqrt{2}$. The next smallest squared distances are $10$, for $(8,8), (9,5)$, and $13$, reached by three pairs. The [divide and conquer page](/closest-pair-divide-and-conquer/) traces its algorithm on this set: the best pair inside the left half has $\delta^2 = 13$, inside the right half $10$, and the winning pair crosses the dividing line.

**One dimension.** For the numbers $7, 2, 19, 11, 4, 15$, sorting gives $2, 4, 7, 11, 15, 19$ with gaps $2, 3, 4, 4, 4$, so the closest pair is $2, 4$.

**Duplicates.** For $P = \{(1,1), (7,3), (2,9), (7,3), (0,5)\}$ the answer is the two copies of $(7,3)$ with distance $0$. An algorithm that stores the points in a set loses this pair.

**Floating point.** For $a = (0, 0)$, $b = (10^8, 1)$, $c = (-10^8, 0)$ the closest pair is $a, c$ with $\delta^2 = 10^{16}$, not $a, b$ with $10^{16} + 1$. A program that compares `math.hypot` values sees a tie and may return either.

## Known algorithms

| algorithm | time | model | idea |
| --- | --- | --- | --- |
| brute force | $\Theta(n^2)$ | real RAM | check every pair |
| [divide and conquer](/closest-pair-divide-and-conquer/) (Shamos and Hoey, 1975) | $\Theta(n \log n)$ | real RAM | split at the median $x$, recurse, scan a strip with at most 7 checks per point |
| [plane sweep](/closest-pair-sweep-line/) (Hinrichs, Nievergelt and Schorn, 1988) | $O(n \log n)$ | real RAM | sweep left to right, keep points within $\delta$ of the sweep line in a balanced tree by $y$ |
| [Delaunay triangulation](/delaunay-triangulation/) | $O(n \log n)$ | real RAM | the closest pair is a Delaunay edge; scan the $O(n)$ edges |
| [randomized grid](/randomized-closest-pair/) (Rabin, 1976; Khuller and Matias, 1995) | $O(n)$ expected | real RAM with floor and hashing | random order or random sampling, grid of side $\delta$, compare with neighbouring cells |
| deterministic grid (Fortune and Hopcroft, 1979) | $O(n \log \log n)$ | real RAM with floor | grids without randomization |

The Delaunay route works because if $p, q$ is a closest pair, the disk with diameter $pq$ contains no other point (such a point would be closer to $p$ or $q$), so $pq$ is an edge of the [Gabriel graph](/gabriel-graph/) and hence of the Delaunay triangulation.

## Bounds

- **Lower bound.** In the algebraic decision tree model, any algorithm that decides whether $\delta(P) = 0$, and so any closest pair algorithm, needs $\Omega(n \log n)$ operations. The proof maps numbers $x_1, \ldots, x_n$ to points $(x_i, 0)$ and uses [Ben-Or's theorem](/ben-or-theorem/) for [element distinctness](/element-distinctness/), whose "yes" set has $n!$ connected components. The bound also holds for inputs promised to be distinct, by asking whether $\delta(P) \ge 1$. See [closest pair lower bound](/closest-pair-lower-bound/).
- **Upper bounds.** $O(n \log n)$ deterministic on the real RAM, which matches the lower bound; $O(n)$ expected with floor and randomization; $O(n \log \log n)$ deterministic with floor.
- **Why the models differ.** The floor function lets an algorithm put each point into a grid cell in constant time and compare only points in the same or neighbouring cells. An algebraic decision tree has no such operation; each test is the sign of a polynomial in the coordinates. The $\Omega(n \log n)$ bound says nothing about algorithms that use floor.
- **Sorted input.** Presorting by $x$ does not help in the plane: map $x_i \mapsto (0, x_i)$; all points have the same $x$, so any order is sorted by $x$, and the question is still element distinctness. In one dimension, sorted input gives $O(n)$ time by scanning neighbours.

## Reductions

- **Element distinctness reduces to closest pair.** Map $x_i \mapsto (x_i, 0)$ in $O(n)$ time; the numbers are distinct exactly when $\delta(P) > 0$. This gives the lower bound.
- **Closest pair reduces to all nearest neighbors.** The closest pair is the smallest distance among the nearest-neighbor distances, found in $O(n)$ extra time.
- **Closest pair reduces to the Euclidean MST.** The shortest edge of any [Euclidean minimum spanning tree](/euclidean-minimum-spanning-tree/) is a closest pair, by the [cut property](/cut-property/).
- **Closest pair reduces to the Delaunay triangulation and the Voronoi diagram.** A closest pair is a Delaunay edge, so it follows in $O(n)$ time from the [Voronoi diagram](/voronoi-diagram/).

## Applications

- **Collision warning.** Air and sea traffic control check which two moving objects are nearest; the closest pair of the current positions is the first alarm candidate. See [collision detection](/collision-detection/).
- **Duplicate and near-duplicate detection.** A closest pair at distance $0$ or below a threshold reveals repeated or almost repeated records, for example in point clouds or mesh vertices before welding.
- **Clustering.** The first merge of [single linkage clustering](/single-linkage-clustering/) joins a closest pair.
- **Robustness checks.** The closest pair distance bounds how much a point set can be perturbed before two points can swap places, which matters for snapping coordinates to a grid.
- **Subroutine.** Grid-based algorithms for other geometric problems first compute $\delta(P)$ to choose the cell size, as in the [uniform grid](/uniform-grid/).

## References
