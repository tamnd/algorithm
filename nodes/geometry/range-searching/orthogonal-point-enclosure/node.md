---
tag: 1MRQ1J
kind: problem
slug: orthogonal-point-enclosure
name: Orthogonal point enclosure
aliases:
- point enclosure query
- rectangle stabbing
- rectangle stabbing query
area: geometry/range-searching
level: advanced
summary: Report the rectangles that contain a query point; the dual of orthogonal range reporting.
prereqs: [orthogonal-range-reporting, interval-stabbing-query, segment-tree]
see_also: [interval-stabbing-query, interval-tree, segment-tree, two-dimensional-segment-tree, dominance-counting, orthogonal-range-reporting, rectangle-intersection-reporting, decomposable-searching-problem]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (orthogonal range searching; rectangle stabbing as the dual problem)
  - paper: doi:10.1137/0215051
    title: Bernard Chazelle, Filtering search, a new approach to query-answering, SIAM Journal on Computing 15(3), 1986, pages 703 to 724
    locator: point enclosure among rectangles in the plane with O(n) space and O(log n + k) query time (DOI to be checked)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 10, Section 10.1 (interval trees) and Section 10.3 (segment trees with associated structures); notes in Section 10.5
---

Orthogonal point enclosure stores a set $S$ of $n$ axis-parallel boxes so that, for a query point $q$, the boxes of $S$ that contain $q$ can be reported or counted. It is the dual of [orthogonal range reporting](/orthogonal-range-reporting/): there the ranges are queries and the points are stored, here the points are queries and the ranges are stored. In one dimension it is [interval stabbing](/interval-stabbing-query/), solved by an [interval tree](/interval-tree/) in $O(\log n + k)$ time and $O(n)$ space. In the plane a [segment tree](/segment-tree/) with interval trees at its nodes gives $O(\log^2 n + k)$ time with $O(n \log n)$ space, and Chazelle's filtering search reaches $O(\log n + k)$ with $O(n)$ space.

## In plain words

A set of rectangles is stored, for example the areas covered by several delivery zones on a map. A question gives a single point, and the answer is every rectangle that covers that point, or how many there are.

This turns the usual range question around. Usually points are stored and a rectangle is asked about; here rectangles are stored and a point is asked about. A rectangle covers the point when the point is between its left and right sides and between its bottom and top. Each of these four conditions is a simple comparison, so the question can also be seen as a range question about four numbers per rectangle.

## Definition

**Notation.** $S$ is a set of $n$ closed boxes; in the plane a box is $R = [a_1, b_1] \times [a_2, b_2]$ with $a_1 \le b_1$ and $a_2 \le b_2$. $q = (q_x, q_y)$ is the query point and $k$ the number of boxes reported. $d$ is the dimension. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

**Input.** $S$, preprocessed once. Then queries, each a point $q$.

**Output.** **Reporting**: the boxes $R \in S$ with $q \in R$, that is $a_1 \le q_x \le b_1$ and $a_2 \le q_y \le b_2$. **Counting**: their number. **Emptiness**: whether there is one.

**Degenerate input.** Boxes are closed, so a query point on a side or a corner is enclosed. Boxes may be degenerate (segments or points), may share coordinates, and may repeat.

## Variants

- **Dimension.** $d = 1$ is interval stabbing; $d = 2$ is rectangle stabbing; $d \ge 3$ is box stabbing.
- **Counting or reporting.** Counting reduces to dominance counting (see Reductions); reporting needs output-sensitive structures.
- **Dynamic.** Boxes are inserted and deleted between queries; segment trees and interval trees with balanced skeletons support this.
- **Batched.** All query points are known: a sweep over $x$ with an interval structure on $y$ answers them in $O((n + m) \log n + K)$ time for $m$ queries and $K$ reported pairs.
- **Rectangle intersection.** Reporting the boxes that intersect a query box combines point enclosure with range reporting; see [rectangle intersection reporting](/rectangle-intersection-reporting/).

## Examples

Take the boxes $R_1 = [1, 4] \times [2, 5]$, $R_2 = [3, 7] \times [1, 3]$, $R_3 = [5, 8] \times [4, 6]$, $R_4 = [3, 3] \times [3, 8]$ (a vertical segment) and $R_5 = [2, 6] \times [3, 7]$.

| query point | boxes containing it | $k$ | boundary cases |
|---|---|---|---|
| $(3, 3)$ | $R_1, R_2, R_4, R_5$ | 4 | $q$ is on the top side of $R_2$, on $R_4$, and on the bottom side of $R_5$ |
| $(6, 5)$ | $R_3, R_5$ | 2 | $q$ is on the right side of $R_5$ |
| $(8, 8)$ | none | 0 | |

For $(6, 5)$ the counting reduction below gives $N_{aa} - N_{ab} - N_{ba} + N_{bb} = 5 - 1 - 2 + 0 = 2$: all five boxes have $a_1 \le 6$ and $a_2 \le 5$; one ($R_2$) has $a_1 \le 6$ and $b_2 < 5$; two ($R_1$, $R_4$) have $b_1 < 6$ and $a_2 \le 5$; none has $b_1 < 6$ and $b_2 < 5$.

## Known algorithms

| structure | space | query | model and case | reference |
|---|---|---|---|---|
| linear scan | $O(n)$ | $O(n)$ | real RAM, worst case | |
| [interval tree](/interval-tree/), $d = 1$ | $O(n)$ | $O(\log n + k)$ | real RAM, worst case | Edelsbrunner; McCreight |
| [segment tree](/segment-tree/) on $x$ with interval trees on $y$, $d = 2$ | $O(n \log n)$ | $O(\log^2 n + k)$ | real RAM, worst case | de Berg et al., Section 10.3 |
| the same with fractional cascading, $d = 2$ | $O(n \log n)$ | $O(\log n + k)$ | real RAM, worst case | |
| filtering search, $d = 2$ | $O(n)$ | $O(\log n + k)$ | real RAM, worst case | Chazelle (1986) |
| $d - 1$ levels of segment trees over an interval tree, $d \ge 2$ | $O(n \log^{d-1} n)$ | $O(\log^{d} n + k)$ | real RAM, worst case | multi-level structure |
| counting by four dominance counts, $d = 2$ | $O(n \log n)$ | $O(\log n)$ | real RAM, worst case | [dominance counting](/dominance-counting/) |

In a segment tree on the $x$-intervals $[a_1, b_1]$, each box is stored at the $O(\log n)$ canonical nodes of its $x$-interval, and the query point visits the $O(\log n)$ nodes on one root-to-leaf path. Every box stored at a visited node contains $q_x$, so only its $y$-interval has to be tested, by an interval tree at the node.

## Bounds

- **Reporting.** $\Omega(\log n + k)$ in the comparison model, met in the plane with linear space by Chazelle (1986).
- **Higher dimensions.** For $d \ge 3$ the optimal space and time are not settled; the known pointer machine bounds are listed in the Handbook chapter.
- **Counting.** Point enclosure counting in the plane is as hard as [orthogonal range counting](/orthogonal-range-counting/) in the plane, up to constant factors, by the reductions in both directions.

## Reductions

- **To dominance in $\mathbb{R}^{2d}$.** Map $R = [a_1, b_1] \times [a_2, b_2]$ to the point $(a_1, -b_1, a_2, -b_2)$. Then $q \in R$ exactly when this point is dominated by $(q_x, -q_x, q_y, -q_y)$, so point enclosure is a four-dimensional dominance query.
- **Counting by inclusion and exclusion.** For $a \le b$, $[a \le t \le b] = [a \le t] - [b < t]$, because $b < t$ implies $a \le t$. Multiplying the $x$ and $y$ factors gives $|\{R \in S : q \in R\}| = N_{aa} - N_{ab} - N_{ba} + N_{bb}$, where $N_{aa}$ counts the boxes with $a_1 \le q_x$ and $a_2 \le q_y$, $N_{ab}$ those with $a_1 \le q_x$ and $b_2 < q_y$, $N_{ba}$ those with $b_1 < q_x$ and $a_2 \le q_y$, and $N_{bb}$ those with $b_1 < q_x$ and $b_2 < q_y$. Each term is a two-dimensional [dominance count](/dominance-counting/) over one corner of the boxes.
- **From dominance counting.** Conversely, a point $p$ is dominated by $q$ exactly when $q$ lies in the quadrant $[p_x, \infty) \times [p_y, \infty)$, a box with two infinite sides. So dominance counting, and with it [orthogonal range counting](/orthogonal-range-counting/) in the plane, is a special case of point enclosure counting.
- **Decomposability.** The answer for a union of box sets is the union of the answers, so the [logarithmic method](/decomposable-searching-problem/) makes any static structure dynamic.

## Applications

- **Geographic information systems**: which zones, map tiles or bounding boxes cover a clicked point.
- **Packet classification** with two fields given as ranges: which rules match a packet.
- **Spatial joins and hit testing** in graphics user interfaces.
- **Rectangle intersection** reporting, as a building block.

## References
