---
tag: 5A5FQN
kind: problem
slug: convex-layers
name: Convex layers
aliases:
- onion peeling
- convex onion
- convex hull peeling
- onion layers
area: geometry/convex-hulls
level: core
summary: Repeatedly peel off the convex hull of the remaining points to get nested layers.
prereqs: [convex-hull-problem, andrew-monotone-chain]
see_also: [dynamic-convex-hull, jarvis-march, halfspace-range-searching, convex-hull-lower-bound, convex-hull, extreme-point, chan-algorithm, convex-hull-3d]
sources:
  - paper: doi:10.1109/TIT.1985.1057060
    title: Bernard Chazelle, On the convex layers of a planar set, IEEE Transactions on Information Theory 31(4), 1985
    locator: the O(n log n) time, O(n) space algorithm for all convex layers and its optimality
  - paper: doi:10.1016/0022-0000(81)90012-X
    title: Mark H. Overmars and Jan van Leeuwen, Maintenance of configurations in the plane, Journal of Computer and System Sciences 23(2), 1981
    locator: the dynamic convex hull with O(log^2 n) time per update and its use for convex layers in O(n log^2 n) time
  - paper: "Bernard Chazelle, Leonidas J. Guibas and D. T. Lee, The power of geometric duality, BIT 25(1), 1985"
    locator: half-plane range reporting in O(log n + k) query time and O(n) space with convex layers
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 4, the section on convex layers (peeling) and its statistical motivation
---

The convex layers of a finite point set are found by peeling it like an onion: the first layer is the set of points on the boundary of the [convex hull](/convex-hull/), the second layer is the set of points on the boundary of the hull of what remains, and so on until no points are left. Each point gets a depth, the number of its layer, which measures how far inside the set it lies. Peeling with a hull algorithm once per layer costs up to $\Theta(n^2)$ time, but Chazelle (1985) computes all layers in $O(n \log n)$ time and $O(n)$ space, which is optimal. Convex layers are used for half-plane range reporting and for robust statistics.

## In plain words

Take the rubber band around a set of nails, as for the convex hull, and pull out all the nails that touch it. Put a new rubber band around the nails that are left and pull out those it touches. Keep going until no nails are left. Each round gives one layer, and the layers sit inside each other like the skins of an onion.

The outer nails are the extreme ones and the inner nails are the central ones. So the round in which a nail comes out says how deep it is in the set. The simple way to do this is to find the band again from the start in each round. That is slow when there are many rounds. A cleverer method keeps the work of one round for the next, and finds all layers in about the time of one sort.

## Definition

**Input.** A finite set $S$ of $n$ points in the plane (repeated points are merged).

**Output.** The layers $L_1, L_2, \ldots, L_k$, defined by $S_1 = S$ and, while $S_j \ne \emptyset$,

$$L_j = S_j \cap \partial\, \mathrm{conv}(S_j), \qquad S_{j+1} = S_j \setminus L_j,$$

where $\partial$ is the boundary. Each layer is given as a counterclockwise cycle of its points. The *depth* of a point $p \in L_j$ is $j$, and $k$ is the number of layers.

**Convention on boundary points.** The definition above puts every point on the boundary of the current hull, including points in the middle of an edge, into the layer. This is the convention of Chazelle's paper. Another convention puts only the [extreme points](/extreme-point/) into the layer; it can give a different answer, because a point in the middle of an edge then stays for the next round. A page or a library must say which one it uses. If $S_j$ lies on one line, its hull is a segment and all of $S_j$ is on its boundary, so it forms the last layer.

**Number of layers.** Every layer except the last has at least three points (otherwise the remaining points would be on a line and form the last layer), so $k \le \lceil n/3 \rceil$. Nested triangles reach this bound. Points in convex position give $k = 1$.

**Model.** The [real RAM](/real-ram/), with the [orientation test](/orientation-test/) as the only geometric predicate; with integer coordinates every step is exact. Lower bounds are in the algebraic decision tree model.

## Variants

- **Extreme points only.** As described in the convention above.
- **Depth of one point.** Find the layer of a given query point without computing all layers. The same peeling, stopped early, does this.
- **Higher dimensions.** Peel the 3D hull repeatedly. Each round is a [3D convex hull](/convex-hull-3d/) computation, and the plane-specific methods below do not carry over directly.
- **Other depth notions.** Tukey (half-space) depth, the smallest number of points in a closed half-plane that contains $p$, is a different measure. A point of hull depth $j$ has Tukey depth at least $j$, since a half-plane through it must cut every enclosing layer, but the two can differ a lot.

## Examples

**Fifteen points.** Let

$$S = \{(0,0), (8,0), (8,8), (0,8), (4,0), (2,2), (6,2), (6,6), (2,6), (4,4), (3,4), (5,5), (4,7), (1,4), (7,4)\}.$$

A script that recomputes the hull with [Andrew's monotone chain](/andrew-monotone-chain/) in each round and collects the boundary points gives three layers:

| layer | hull corners (counterclockwise) | boundary points | size |
| --- | --- | --- | --- |
| $L_1$ | $(0,0), (8,0), (8,8), (0,8)$ | the corners and $(4,0)$ | 5 |
| $L_2$ | $(1,4), (2,2), (6,2), (7,4), (6,6), (4,7), (2,6)$ | the corners | 7 |
| $L_3$ | $(3,4), (4,4), (5,5)$ | the corners | 3 |

The point $(4, 0)$ is in the middle of the edge from $(0,0)$ to $(8,0)$. Under the extreme-points convention it would stay for round 2, and the second layer would change.

**A grid.** For the 25 points $\{0, 1, 2, 3, 4\}^2$, the layers are the 16 points of the outer square ring, the 8 points of the inner ring and the center point. Most of these are mid-edge points, so the extreme-points convention gives quite different layers here.

**Worst case for naive peeling.** For nested triangles, $n/3$ layers of 3 points each, recomputing the hull from scratch in each round costs $\Theta(n)$ per round after one initial sort, and $\Theta(n^2)$ in total.

## Known algorithms

All times are worst case on the real RAM.

| algorithm | time | space | idea |
| --- | --- | --- | --- |
| repeated hull from scratch | $O(n^2 \log n)$ | $O(n)$ | run an $O(n \log n)$ hull algorithm once per layer |
| sort once, then a monotone chain per layer | $O(n \log n + nk)$, at most $O(n^2)$ | $O(n)$ | the remaining points stay sorted, so each round of [Andrew's scan](/andrew-monotone-chain/) costs $O(\lvert S_j \rvert)$ |
| repeated [Jarvis march](/jarvis-march/) | $O(n^2)$ | $O(n)$ | each wrap step costs $O(\lvert S_j \rvert)$, and there are $n$ steps in total, one per point removed |
| dynamic hull with deletions (Overmars and van Leeuwen, 1981) | $O(n \log^2 n)$ | $O(n)$ | build the [dynamic hull](/dynamic-convex-hull/) once, then delete the points of each layer as it is reported |
| Chazelle (1985) | $O(n \log n)$ | $O(n)$ | a tree of hull bridges built once, with a deletion procedure whose total cost over the whole peeling is $O(n \log n)$ |

The Jarvis bound counts one wrap step per reported boundary point, plus one closing step per layer, and each step is a scan of the remaining points, so the total is at most $\sum_j (\lvert L_j \rvert + 1) \cdot n = O(n^2)$.

## Bounds

- **Lower bound.** $\Omega(n \log n)$ in the algebraic decision tree model. The first layer is the convex hull with all boundary points, and for points on a parabola it lists $n$ points in sorted order, so the [convex hull lower bound](/convex-hull-lower-bound/) applies.
- **Upper bound.** $O(n \log n)$ time and $O(n)$ space (Chazelle), so the problem is settled in the plane.
- **Random points.** For $n$ points drawn uniformly from a disk, the expected number of layers is $\Theta(n^{2/3})$ (Dalal, 2004). This is an expected-case statement about the input distribution.

## Reductions

- **Hull reduces to layers.** The first layer is the hull (with mid-edge points), so the layers are at least as hard as the [convex hull problem](/convex-hull-problem/).
- **Layers reduce to a dynamic hull.** Any structure that supports deletions and reports the current hull gives the layers: report, delete the reported points, repeat. The cost is $n$ deletions plus the output.
- **Duality.** Under the point-line duality, layers of points become nested envelopes of lines, the form used for half-plane range reporting.

## Applications

- **Half-plane range reporting.** Chazelle, Guibas and Lee (1985) use convex layers to report the $k$ points of a set inside a query half-plane in $O(\log n + k)$ time with $O(n)$ space: walk the layers from the outside, and stop at the first layer that the half-plane misses, since then it misses all inner layers. See [half-space range searching](/halfspace-range-searching/).
- **Robust statistics.** Peeling removes the most extreme points first, so trimming the outer layers removes outliers, and the innermost layer gives a multivariate analogue of the median. The depth of a point is a rank from the outside in.
- **Pattern recognition and data summaries.** The layer structure describes the shape of a point cloud at several levels.
- **Testing hull code.** Peeling exercises deletions and many hull computations with nested, degenerate inputs, which makes it a good stress test for an exact hull implementation.

## References
