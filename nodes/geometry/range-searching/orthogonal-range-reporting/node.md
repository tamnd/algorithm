---
tag: AC39DS
kind: problem
slug: orthogonal-range-reporting
name: Orthogonal range reporting
aliases:
- orthogonal range listing
- box reporting query
area: geometry/range-searching
level: core
summary: List all points inside an axis-parallel query box, with output-sensitive time O(log n + k) type bounds as the goal.
prereqs: [orthogonal-range-searching]
see_also: [orthogonal-range-counting, range-emptiness-query, range-tree, layered-range-tree, kd-tree-range-search, priority-search-tree, three-sided-range-query, range-searching-lower-bound]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Sections 5.2 to 5.6 (kd-trees, range trees, fractional cascading)
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, orthogonal range reporting and Table 40.2.1
  - paper: doi:10.1137/0215051
    title: Bernard Chazelle, Filtering search, a new approach to query-answering, SIAM Journal on Computing 15(3), 1986, pages 703 to 724
    locator: two-dimensional reporting in O(n log n / log log n) space and O(log n + k) time (DOI to be checked)
  - paper: doi:10.1145/77600.77614
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, I. The reporting case, Journal of the ACM 37(2), 1990, pages 200 to 212
    locator: pointer machine lower bound Ω(n (log n / log log n)^(d-1)) on the space (DOI to be checked)
  - paper: doi:10.1145/1998196.1998198
    title: Timothy M. Chan, Kasper Green Larsen and Mihai Pătraşcu, Orthogonal range searching on the RAM, revisited, SoCG 2011, pages 1 to 10
    locator: word RAM structures for two-dimensional reporting (DOI to be checked)
---

Orthogonal range reporting is the version of [orthogonal range searching](/orthogonal-range-searching/) in which a query box must return every point of $P$ that it contains. Since the answer itself has $k$ points, the time of a query has the form $f(n) + O(k)$, and the goal is a small search term $f(n)$, ideally $O(\log n)$, with near-linear space. In the plane, a [range tree](/range-tree/) with fractional cascading reaches $O(\log n + k)$ with $O(n \log n)$ space, and a [kd-tree](/kd-tree/) uses linear space but needs $O(\sqrt{n} + k)$.

## In plain words

A set of points is stored, and a question gives a rectangle with sides along the axes. The answer is the full list of points inside the rectangle, including those on its border.

A good method spends a short time finding where the answer is and then one step per point of the answer. If the answer has a million points, any method has to spend a million steps to write them, so the interesting part is the time spent on top of that. Methods differ in how much memory they need to keep this extra time small.

## Definition

**Notation.** $P$ is the input point set, $n = |P|$, $d$ the dimension, $p = (x, y)$ a point in the plane, and $k = |P \cap Q|$ the output size of the query $Q$. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

**Input.** A multiset $P$ of $n$ points in $\mathbb{R}^d$. Repeated points and repeated coordinates are allowed; no general position is assumed.

**Query.** A closed box $Q = [a_1, b_1] \times \dots \times [a_d, b_d]$. A point on the boundary belongs to $Q$.

**Output.** The list of all $p \in P$ with $p \in Q$, each copy once, in any order.

A structure is called *output sensitive* if its query time is $O(f(n) + k)$ with $f(n) = o(n)$. The term $k$ is unavoidable, since each reported point costs at least one step.

## Variants

- **Static or dynamic.** Points are fixed, or inserted and deleted; see [dynamic range searching](/dynamic-range-searching/).
- **Three-sided and two-sided.** If one side of the box is at infinity, a [priority search tree](/priority-search-tree/) answers the [three-sided query](/three-sided-range-query/) in $O(\log n + k)$ time with linear space. A two-sided (dominance) box is a special case.
- **Reporting the first $t$ points** or reporting in sorted order of one coordinate, used in top-$t$ queries.
- **External memory.** With blocks of $B$ points, the goal is $O(\log_B n + k/B)$ I/Os.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| query box | reported points | $k$ |
|---|---|---|
| $[3, 7] \times [2, 6]$ | $(5,4), (7,2), (6,6)$ | 3 |
| $[0, 10] \times [0, 10]$ | all 8 points | 8 |
| $[5, 5] \times [4, 4]$ | $(5,4)$ | 1 |
| $[4.5, 5.5] \times [6.5, 9]$ | none | 0 |
| $[8, 9] \times [1, 6]$ | $(9,6), (8,1)$ | 2 |

The third query is a single point, and it is reported because the box is closed.

## Known algorithms

Space, query time and preprocessing for $n$ points in the plane ($d = 2$); "w.c." means worst case.

| structure | preprocessing | space | query | model |
|---|---|---|---|---|
| linear scan | none | $O(n)$ | $O(n)$ w.c. | any |
| [kd-tree](/kd-tree/), [kd-tree range search](/kd-tree-range-search/) | $O(n \log n)$ w.c. | $O(n)$ | $O(\sqrt{n} + k)$ w.c. | real RAM |
| [range tree](/range-tree/), [range tree query](/range-tree-query/) | $O(n \log n)$ w.c. | $O(n \log n)$ | $O(\log^2 n + k)$ w.c. | real RAM |
| [layered range tree](/layered-range-tree/) | $O(n \log n)$ w.c. | $O(n \log n)$ | $O(\log n + k)$ w.c. | real RAM |
| Chazelle's filtering search (1986) | $O(n \log n)$ w.c. | $O(n \log n / \log \log n)$ | $O(\log n + k)$ w.c. | pointer machine |
| Chazelle's compressed range tree (1988) | $O(n \log n)$ w.c. | $O(n)$ | $O(\log n + k \log^{\varepsilon} n)$ w.c. | word RAM |
| Chan, Larsen and Pătraşcu (2011) | see paper | $O(n \log^{\varepsilon} n)$ | $O(\log \log n + k)$ w.c. | word RAM, rank space |

In $d$ dimensions the kd-tree gives $O(n^{1-1/d} + k)$ with linear space ([kd-tree range query complexity](/kd-tree-range-query-complexity/)), the range tree $O(\log^{d} n + k)$ with $O(n \log^{d-1} n)$ space, and the layered range tree $O(\log^{d-1} n + k)$ with the same space.

## Bounds

- **Search term.** In the comparison model, $\Omega(\log n)$ comparisons are needed even in one dimension, since emptiness of a one-point box is a membership test.
- **Space on the pointer machine.** Chazelle (1990) proved that a pointer machine structure with query time $O(\log^{c} n + k)$, for any constant $c$, needs $\Omega(n (\log n / \log \log n)^{d-1})$ space. In the plane the filtering search structure matches this bound, so on the pointer machine $O(\log n + k)$ time and $O(n \log n / \log \log n)$ space is optimal. See [range searching lower bounds](/range-searching-lower-bound/).
- **Linear space.** On the pointer machine, the bound above rules out a query time of $O(\log^{c} n + k)$ with $O(n)$ space, and the kd-tree gives $O(\sqrt{n} + k)$ in the plane. On the word RAM, Chazelle's compressed range tree reaches $O(\log n + k \log^{\varepsilon} n)$ with $O(n)$ space.

## Reductions

- **From one dimension.** With $d = 1$, the problem is [one-dimensional range search](/one-dimensional-range-search/).
- **To counting.** A counting structure plus a reporting structure can answer "report if at most $t$ points, otherwise say too many" in time independent of $k$.
- **From emptiness, with a constant factor.** A reporting structure answers [emptiness](/range-emptiness-query/) by stopping at the first reported point, so emptiness costs the search term $f(n)$ only.
- **Rectangle intersection.** Reporting all pairs of intersecting axis-parallel rectangles uses range reporting on corners plus segment intersection; see [rectangle intersection reporting](/rectangle-intersection-reporting/).

## Applications

- Window queries in geographic information systems and map viewers.
- Database selections with range conditions on several numeric attributes.
- Collision broad phase: all objects whose reference point lies in a box around a moving object.

## References
