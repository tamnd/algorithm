---
tag: EF856F
kind: problem
slug: orthogonal-range-searching
name: Orthogonal range searching
aliases:
- orthogonal range query
- axis-parallel range searching
- rectangular range searching
- box query
area: geometry/range-searching
level: core
summary: Range searching where each query range is an axis-parallel box.
prereqs: [one-dimensional-range-search, binary-search-tree]
see_also: [orthogonal-range-reporting, orthogonal-range-counting, range-emptiness-query, dominance-counting, three-sided-range-query, range-tree, range-searching-lower-bound, simplex-range-searching]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Orthogonal Range Searching, Sections 5.1 to 5.7
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.1 (models of computation) and Section 40.2 (orthogonal range searching, Table 40.2.1)
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.3, Range-searching problems (section number to be checked)
  - paper: doi:10.1145/358841.358850
    title: Jon Louis Bentley, Multidimensional divide-and-conquer, Communications of the ACM 23(4), 1980, pages 214 to 229
    locator: the range tree and its analysis for d dimensions
  - paper: doi:10.1145/77600.77614
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, I. The reporting case, Journal of the ACM 37(2), 1990, pages 200 to 212
    locator: the pointer machine space lower bound (DOI to be checked)
  - paper: doi:10.1145/79147.79149
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, II. The arithmetic model, Journal of the ACM 37(3), 1990, pages 439 to 463
    locator: the semigroup query time lower bound (DOI to be checked)
---

Orthogonal range searching is the problem of storing a set $P$ of $n$ points in $\mathbb{R}^d$ so that, for a query box $[a_1, b_1] \times \dots \times [a_d, b_d]$ with sides parallel to the axes, the points of $P$ inside the box can be reported, counted, tested for existence or summed. It is the most studied case of range searching because database queries such as "age between 30 and 40 and salary between 2000 and 3000" have this form. The main structures are the [kd-tree](/kd-tree/), with linear space and $O(n^{1-1/d} + k)$ query time, and the [range tree](/range-tree/), with $O(n \log^{d-1} n)$ space and $O(\log^{d} n + k)$ query time, improved by one logarithmic factor with fractional cascading.

## In plain words

A table of records has several numeric columns, and each record is a point whose coordinates are its column values. A question names, for each column, a lowest and a highest allowed value. The answer is every record whose values all lie in their allowed ranges. In two columns, the allowed region is a rectangle on a map, and the answer is every point inside the rectangle.

Some versions of the question ask for the list of matching records, some only for how many there are, some only whether there is one, and some for a total, such as the sum of the salaries of the matching records. Checking every record works but is slow when the table is large and the questions are many. The structures for this problem prepare the points once so that each question looks at only a small part of them.

## Definition

**Notation.** $P$ is the input point set, $n = |P|$ the input size, $d$ the dimension, and $p = (p_1, \dots, p_d)$ a point, with $p = (x, y)$ in the plane. The output size of a reporting query is $k = |P \cap Q|$; it plays the role that $h$ plays on other geometry pages. The predicates $\mathrm{orient}(p, q, r)$ and $\mathrm{incircle}$ are not needed: orthogonal queries compare one coordinate at a time.

**Input.** A multiset $P$ of $n$ points in $\mathbb{R}^d$ with coordinates from a totally ordered set (integers or rationals in the code of this site). Points may coincide and may share coordinates. No general position is assumed.

**Query.** A box $Q = [a_1, b_1] \times \dots \times [a_d, b_d]$. The box is closed: $p \in Q$ if and only if $a_i \le p_i \le b_i$ for every $i$. A box with $a_i > b_i$ for some $i$ is empty. Open or half-open sides change $\le$ into $<$ on that side, and with integer coordinates they reduce to closed ones.

**Output.** One of the following.

- [Reporting](/orthogonal-range-reporting/): the points of $P \cap Q$, each copy once.
- [Counting](/orthogonal-range-counting/): $|P \cap Q|$.
- [Emptiness](/range-emptiness-query/): whether $P \cap Q = \emptyset$.
- *Semigroup or group aggregate*: given weights $w(p)$ in a commutative semigroup $(S, +)$, the sum $\sum_{p \in P \cap Q} w(p)$. Counting is the case $w \equiv 1$ in the integers. If $S$ is a group, subtraction is allowed; if it is only a semigroup (for example $\max$), it is not.

**Degenerate input.** Equal coordinates are handled by comparing points as composite keys. de Berg et al. (Section 5.5) replace each coordinate $p_i$ by the tuple $(p_i, p_{i+1}, \dots, p_d, p_1, \dots, p_{i-1})$ compared in lexicographic order, which makes all coordinates distinct without changing the answer, if the query box is transformed to $[(a_i, -\infty, \dots), (b_i, +\infty, \dots)]$. The code on this site uses $(p_i, \text{index})$ keys or index intervals found with lower and upper bound searches, which has the same effect.

## Variants

- **Static, dynamic, offline.** Static structures are built once. [Dynamic range searching](/dynamic-range-searching/) also supports insertions and deletions. In the offline version all queries are known in advance, and a [sweep with a Fenwick tree](/offline-orthogonal-range-counting/) counts in $O((n + q) \log (n + q))$ total time for $n$ points and $q$ boxes in the plane.
- **Fewer sides.** A query with some sides at infinity is easier. A box $[a_1, \infty) \times [a_2, \infty)$ is a [dominance](/dominance-counting/) query, and $[a_1, b_1] \times (-\infty, b_2]$ is a [three-sided query](/three-sided-range-query/), answered by a [priority search tree](/priority-search-tree/) in linear space.
- **Inverse problem.** Store boxes and query with a point: [orthogonal point enclosure](/orthogonal-point-enclosure/), related to [interval trees](/interval-tree/) and [segment trees](/segment-tree/).
- **Other range shapes.** Halfspaces, simplices and disks give [halfspace](/halfspace-range-searching/), [simplex](/simplex-range-searching/) and [circular](/circular-range-searching/) range searching, which need different tools.

## Examples

Take the eight points $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ and the box $Q = [3, 7] \times [2, 6]$.

| point | $3 \le x \le 7$ | $2 \le y \le 6$ | in $Q$ |
|---|---|---|---|
| $(2,3)$ | no | yes | no |
| $(5,4)$ | yes | yes | yes |
| $(9,6)$ | no | yes | no |
| $(4,7)$ | yes | no | no |
| $(8,1)$ | no | no | no |
| $(7,2)$ | yes | yes, on the boundary | yes |
| $(3,8)$ | yes | no | no |
| $(6,6)$ | yes | yes, on the boundary | yes |

Reporting returns $(5,4), (7,2), (6,6)$; counting returns $3$; emptiness returns "not empty". With weights $w(p) = y$ and the semigroup $\max$, the answer is $6$. The point $(7,2)$ lies on two sides of the box at once and is still reported, because the box is closed.

## Known algorithms

Bounds for $n$ points in $\mathbb{R}^d$, $d \ge 2$ fixed, reporting $k$ points. All are worst case unless stated, on the [real RAM](/real-ram/) or the [pointer machine](/pointer-machine/) unless marked word RAM.

| structure | build | space | reporting query | counting query |
|---|---|---|---|---|
| linear scan | none | $O(n)$ | $O(n)$ | $O(n)$ |
| [kd-tree](/kd-tree/) with [kd-tree range search](/kd-tree-range-search/) | $O(n \log n)$ | $O(n)$ | $O(n^{1-1/d} + k)$ | $O(n^{1-1/d})$ |
| [range tree](/range-tree/) with [range tree query](/range-tree-query/) | $O(n \log^{d-1} n)$ | $O(n \log^{d-1} n)$ | $O(\log^{d} n + k)$ | $O(\log^{d} n)$ |
| [layered range tree](/layered-range-tree/) (fractional cascading) | $O(n \log^{d-1} n)$ | $O(n \log^{d-1} n)$ | $O(\log^{d-1} n + k)$ | $O(\log^{d-1} n)$ |
| Chazelle's filtering search, $d = 2$ | $O(n \log n)$ | $O(n \log n / \log \log n)$ | $O(\log n + k)$ | |
| Chazelle's compressed range tree, $d = 2$ | $O(n \log n)$ | $O(n)$ | $O(\log n + k \log^{\varepsilon} n)$ | $O(\log n)$ |
| [priority search tree](/priority-search-tree/), 3-sided, $d = 2$ | $O(n \log n)$ | $O(n)$ | $O(\log n + k)$ | |
| Chan, Larsen and Pătraşcu, word RAM, $d = 2$ | | $O(n \log^{\varepsilon} n)$ | $O(\log \log n + k)$ | |

The $\varepsilon$ is any fixed positive constant. The kd-tree query bound is from [the kd-tree range query theorem](/kd-tree-range-query-complexity/). With dynamic updates, a range tree built on weight-balanced trees keeps $O(\log^{d} n + k)$ query time with $O(\log^{d} n)$ amortized update time (Lueker 1978, Willard and Lueker 1985); see [dynamic range searching](/dynamic-range-searching/).

## Bounds

Lower bounds hold in specific models; [range searching lower bounds](/range-searching-lower-bound/) states them with proofs or sketches.

- **Pointer machine, reporting.** Chazelle (1990): a structure that answers $d$-dimensional reporting queries in $O(\log^{c} n + k)$ time must use $\Omega(n (\log n / \log \log n)^{d-1})$ space. In the plane this matches the filtering search structure.
- **Semigroup model, static.** Chazelle (1990): a structure that stores $m$ precomputed semigroup sums answers some query only after $\Omega((\log n / \log (2m/n))^{d-1})$ additions, already for dominance queries. With $m = O(n)$ that is $\Omega(\log^{d-1} n)$, which the layered range tree matches up to the space.
- **Semigroup model, dynamic.** Fredman (1981): a sequence of $n$ insertions, deletions and queries takes $\Omega(n \log^{d} n)$ semigroup operations in total.
- **Cell probe model, counting.** Pătraşcu (2007): in the plane, static counting with $S$ words of space needs $\Omega(\log n / \log (S w / n))$ time on a word RAM with words of $w$ binary digits, so $\Omega(\log n / \log \log n)$ with near-linear space. JaJa, Mortensen and Shi (2004) match it with linear space.
- **One dimension.** Every query needs $\Omega(\log n)$ comparisons in the comparison model, by reduction from membership; see [one-dimensional range search](/one-dimensional-range-search/).

## Reductions

- **Dominance is enough for counting.** In the plane, $|P \cap [a_1, b_1] \times [a_2, b_2]|$ is a signed sum of four dominance counts, by inclusion and exclusion; in $d$ dimensions, of $2^{d}$ counts. This needs subtraction, so it works for groups but not for semigroups.
- **Rank space.** Replacing each coordinate by its rank among the $n$ values does not change any answer, if the query sides are mapped by lower and upper bound searches. After this, coordinates are integers in $[0, n)$, which is what word RAM structures assume.
- **Point enclosure to dominance.** A box $[a_1, b_1] \times [a_2, b_2]$ contains the point $q$ if and only if the point $(a_1, a_2, b_1, b_2) \in \mathbb{R}^4$ satisfies $a_1 \le q_1$, $a_2 \le q_2$, $b_1 \ge q_1$, $b_2 \ge q_2$, a dominance query in four dimensions; see [orthogonal point enclosure](/orthogonal-point-enclosure/).
- **Decomposability.** Counting, reporting and emptiness are [decomposable searching problems](/decomposable-searching-problem/), so any static structure can be made dynamic by the logarithmic method.

## Applications

- Database queries with a range condition on several attributes.
- Geographic information systems: all objects in a map window.
- Rectangle intersection: two axis-parallel rectangles intersect if a corner of one lies in the other or their edges cross, which reduces [rectangle intersection reporting](/rectangle-intersection-reporting/) to range queries and segment intersection.
- Computational statistics: empirical distribution functions and dominance counts in nonparametric tests.

## References
