---
tag: Q65TRK
kind: problem
slug: range-emptiness-query
name: Range emptiness query
aliases:
- orthogonal range emptiness
- range existence query
area: geometry/range-searching
level: core
summary: Decide whether a query range contains any point, without reporting or counting them.
prereqs: [orthogonal-range-searching]
see_also: [orthogonal-range-reporting, orthogonal-range-counting, halfspace-range-searching, priority-search-tree, range-tree, kd-tree-range-search, range-searching-lower-bound, one-dimensional-range-search]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2 (orthogonal emptiness) and Section 40.3 (halfspace emptiness)
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5 (reporting structures, which answer emptiness by stopping at the first point)
  - paper: doi:10.1145/1998196.1998198
    title: Timothy M. Chan, Kasper Green Larsen and Mihai Pătraşcu, Orthogonal range searching on the RAM, revisited, SoCG 2011, pages 1 to 10
    locator: two-dimensional emptiness on the word RAM in O(n log log n) space and O(log log n) time (DOI to be checked)
  - paper: doi:10.1016/0925-7721(92)90006-E
    title: Jiří Matoušek, Reporting points in halfspaces, Computational Geometry, Theory and Applications 2(3), 1992, pages 169 to 186
    locator: halfspace emptiness and reporting with shallow cuttings
---

A range emptiness query asks whether a query range $Q$ contains at least one point of a stored set $P$. It is the weakest of the three standard questions of range searching (reporting, counting, emptiness): a reporting structure answers it by stopping at the first point found, and a counting structure by comparing the count with zero. For orthogonal boxes it is the case $k \le 1$ of [orthogonal range reporting](/orthogonal-range-reporting/), and for halfspaces it is the base of halfspace reporting through [shallow cuttings](/shallow-cutting/).

## In plain words

A set of points is stored, and a question gives a region, for example a rectangle. The answer is yes or no: is there any point inside the region?

This is easier than listing the points or counting them. A method that lists points can stop as soon as it finds the first one, and a method that counts can check whether the count is zero. Some methods answer the yes or no question faster than either. Questions of this kind arise in collision tests: is any obstacle inside this box?

## Definition

**Notation.** $P$ is the input point set, $n = |P|$, $d$ the dimension, $p = (x, y)$ a point in the plane. The output is a yes or no answer, so there is no output size term $k$. $\mathrm{orient}$ is used only for the halfspace version in the plane; $\mathrm{incircle}$ is not used.

**Input.** A multiset $P$ of $n$ points in $\mathbb{R}^d$; repeated points are allowed.

**Query.** A range $Q$ from a fixed family, in the orthogonal case a closed box $[a_1, b_1] \times \dots \times [a_d, b_d]$.

**Output.** "Empty" if $P \cap Q = \emptyset$, "not empty" otherwise. A *witness* version also returns one point of $P \cap Q$ when there is one.

**Degenerate input.** Points on the boundary of a closed box are in the box; a box with $a_i > b_i$ is empty.

## Variants

- **Orthogonal emptiness.** Boxes in $\mathbb{R}^d$; the subject of this page.
- **Halfspace emptiness.** Is any point of $P$ above a query hyperplane? By duality this is the question whether a query point lies below the upper envelope of hyperplanes, so in $\mathbb{R}^2$ and $\mathbb{R}^3$ it reduces to [convex hull](/convex-hull/) queries and point location. See [halfspace range searching](/halfspace-range-searching/).
- **Disk emptiness.** Is any point of $P$ within distance $r$ of $q$? This is a [nearest neighbor](/nearest-neighbor-search/) query compared with $r$, answered with the [Voronoi diagram](/voronoi-diagram/).
- **Dynamic emptiness.** Points are inserted and deleted between queries.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| query box | empty | witness |
|---|---|---|
| $[3, 7] \times [2, 6]$ | no | $(5,4)$ |
| $[4.5, 5.5] \times [6.5, 9]$ | yes | none |
| $[9, 12] \times [6, 6]$ | no | $(9,6)$, on a corner of the box |
| $[6, 8] \times [3, 5]$ | yes | none |
| $[0, 1] \times [0, 10]$ | yes | none |

A three-sided query $[a_1, b_1] \times (-\infty, b_2]$ is empty exactly when the lowest point with $x$ in $[a_1, b_1]$ lies above $b_2$, so a structure for "minimum $y$ in an $x$-interval" answers it: for $[3, 7] \times (-\infty, 1]$ the lowest point with $3 \le x \le 7$ is $(7,2)$, and $2 > 1$, so the range is empty.

## Known algorithms

| structure | space | query | model and case |
|---|---|---|---|
| sorted array, $d = 1$ | $O(n)$ | $O(\log n)$ | comparison model, worst case |
| [priority search tree](/priority-search-tree/), three-sided, $d = 2$ | $O(n)$ | $O(\log n)$ | real RAM, worst case |
| [range minimum query](/range-minimum-query/) over $x$-sorted points, three-sided, $d = 2$ | $O(n)$ | $O(\log n)$ | real RAM, worst case |
| [range tree](/range-tree/) stopped at the first point | $O(n \log^{d-1} n)$ | $O(\log^{d} n)$ | real RAM, worst case |
| [layered range tree](/layered-range-tree/) | $O(n \log^{d-1} n)$ | $O(\log^{d-1} n)$ | real RAM, worst case |
| [kd-tree](/kd-tree/) stopped at the first point | $O(n)$ | $O(n^{1-1/d})$ | real RAM, worst case |
| Chan, Larsen and Pătraşcu (2011), $d = 2$ | $O(n \log \log n)$ | $O(\log \log n)$ | word RAM, rank space, worst case |
| halfspace emptiness, $d \le 3$ | $O(n)$ | $O(\log n)$ | real RAM, worst case |
| halfspace emptiness, $d > 3$ | $O(n)$ | $n^{1 - 1/\lfloor d/2 \rfloor} 2^{O(\log^{*} n)}$ | real RAM, worst case |

The three-sided case uses the identity above: the range is nonempty if and only if the minimum $y$ over the points with $x$ in $[a_1, b_1]$ is at most $b_2$.

## Bounds

- **Comparison model.** Already in one dimension, emptiness of $[x, x]$ is membership, which needs $\Omega(\log n)$ comparisons; see the [sorted search lower bound](/sorted-search-lower-bound/).
- **Emptiness is easier than counting.** On the word RAM, two-dimensional orthogonal emptiness takes $O(\log \log n)$ time with $O(n \log \log n)$ space, below the $\Omega(\log n / \log \log n)$ cell probe bound of Pătraşcu for counting with near-linear space; see [range searching lower bounds](/range-searching-lower-bound/).
- **Halfspaces.** Halfspace emptiness in $\mathbb{R}^d$ is much easier than halfspace counting: its complexity is governed by $\lfloor d/2 \rfloor$, the complexity of the upper envelope, while counting is governed by $d$. See [shallow cutting](/shallow-cutting/).

## Reductions

- **From reporting.** Run a reporting query and stop after the first point. With an output sensitive query time $f(n) + O(k)$, emptiness costs $O(f(n))$.
- **From counting.** Compare the count with zero.
- **Reporting from emptiness.** For halfspaces, a structure that answers emptiness can drive a reporting query: Matoušek's shallow partition trees and Chan's methods turn emptiness bounds into reporting bounds of the form emptiness time plus $O(k)$.
- **From membership.** Membership of $x$ in $P \subset \mathbb{R}$ is emptiness of $[x, x]$.

## Applications

- Collision detection and motion planning: is any obstacle inside a box or a halfspace?
- Linear optimization queries: Matoušek and Schwarzkopf (1992) build them on halfspace emptiness structures.
- Database existence queries ("is there any customer in this age and income range").

## References
