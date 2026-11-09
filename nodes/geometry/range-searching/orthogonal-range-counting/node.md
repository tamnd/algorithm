---
tag: MQ952T
kind: problem
slug: orthogonal-range-counting
name: Orthogonal range counting
aliases:
- orthogonal range count
- box counting query
area: geometry/range-searching
level: core
summary: Count, rather than list, the points inside an axis-parallel query box.
prereqs: [orthogonal-range-searching]
see_also: [dominance-counting, offline-orthogonal-range-counting, orthogonal-range-reporting, range-tree, two-dimensional-fenwick-tree, merge-sort-tree, wavelet-tree, range-searching-lower-bound]
sources:
  - book: isbn:9783540779735
    title: Mark de Berg, Otfried Cheong, Marc van Kreveld and Mark Overmars, Computational Geometry, Algorithms and Applications, third edition, Springer, 2008
    locator: Chapter 5, Section 5.3 and the exercises of Chapter 5 on counting with range trees
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.2, counting queries and lower bounds
  - paper: doi:10.1137/0217026
    title: Bernard Chazelle, A functional approach to data structures and its use in multidimensional searching, SIAM Journal on Computing 17(3), 1988, pages 427 to 462
    locator: linear-space two-dimensional counting in O(log n) time (DOI to be checked)
  - paper: doi:10.1145/79147.79149
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, II. The arithmetic model, Journal of the ACM 37(3), 1990, pages 439 to 463
    locator: semigroup lower bound for static counting with m storage (DOI to be checked)
  - paper: doi:10.1145/1250790.1250797
    title: Mihai Pătraşcu, Lower bounds for 2-dimensional range counting, STOC 2007, pages 40 to 46
    locator: cell probe lower bound Ω(log n / log(S w / n)) (DOI to be checked)
---

Orthogonal range counting is the version of [orthogonal range searching](/orthogonal-range-searching/) in which a query box returns the number $|P \cap Q|$ of points of $P$ inside it, not the points themselves. The answer has constant size, so the query time does not depend on $k$, and in the plane $O(\log n)$ time is possible with $O(n \log n)$ space by a [range tree](/range-tree/) whose nodes store subtree sizes, or with $O(n)$ space by Chazelle's compressed structure. In the plane, counting is a signed sum of four [dominance counts](/dominance-counting/).

## In plain words

A set of points is stored, and a question gives a rectangle with sides along the axes. The answer is a single number: how many points lie inside the rectangle, including its border.

Counting can be faster than listing, because the answer is one number however many points it covers. A structure can keep counts for whole groups of points ready in advance and add a few of them together. Another trick is to count the points below and to the left of each corner of the rectangle and combine the four numbers with plus and minus signs.

## Definition

**Notation.** $P$ is the input point set, $n = |P|$, $d$ the dimension, $p = (x, y)$ a point in the plane. The output is one number, $|P \cap Q|$; there is no output size term. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

**Input.** A multiset $P$ of $n$ points in $\mathbb{R}^d$; repeated points count with multiplicity. No general position is assumed.

**Query.** A closed box $Q = [a_1, b_1] \times \dots \times [a_d, b_d]$.

**Output.** The integer $|P \cap Q|$, counting copies.

The *weighted* version gives each point a weight $w(p)$ in a commutative group $(G, +)$ and asks for $\sum_{p \in P \cap Q} w(p)$. In a semigroup, without subtraction, the problem is the semigroup range searching problem, for which the lower bounds below are stated.

## Variants

- **Static, dynamic, offline.** Dynamic counting supports insertions and deletions: a [two-dimensional Fenwick tree](/two-dimensional-fenwick-tree/) on a fixed grid does both in $O(\log^2 n)$ time. Offline counting with all queries known in advance is solved by [a sweep with a Fenwick tree](/offline-orthogonal-range-counting/).
- **Dominance counting.** Boxes of the form $(-\infty, b_1] \times (-\infty, b_2]$; see [dominance counting](/dominance-counting/).
- **Approximate counting.** Return a number between $(1 - \varepsilon)k$ and $(1 + \varepsilon)k$, which is easier in some models.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$ and the box $Q = [3, 7] \times [2, 6]$, which contains $(5,4), (7,2), (6,6)$, so the count is $3$.

By inclusion and exclusion, with $D(x, y) = |\{p \in P : p_x \le x, p_y \le y\}|$ and integer coordinates,

$$|P \cap Q| = D(7, 6) - D(2, 6) - D(7, 1) + D(2, 1) = 4 - 1 - 0 + 0 = 3 .$$

The four terms are computed from the lists: $D(7,6)$ counts $(2,3), (5,4), (7,2), (6,6)$ and no other point, so it is $4$; then $D(2, 6) = 1$ for $(2,3)$, $D(7, 1) = 0$ and $D(2, 1) = 0$, which gives $4 - 1 - 0 + 0 = 3$. The left side $a_1 = 3$ becomes $x \le 2$ because the coordinates are integers; for real coordinates use strict dominance $p_x < a_1$ in those two terms.

## Known algorithms

Bounds for $n$ points in the plane; all bounds are worst case.

| structure | preprocessing | space | query | model |
|---|---|---|---|---|
| linear scan | none | $O(n)$ | $O(n)$ | any |
| [kd-tree](/kd-tree/) with subtree sizes | $O(n \log n)$ | $O(n)$ | $O(\sqrt{n})$ | real RAM |
| [range tree](/range-tree/) with sorted $y$-arrays | $O(n \log n)$ | $O(n \log n)$ | $O(\log^2 n)$ | real RAM |
| [layered range tree](/layered-range-tree/) | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$ | real RAM |
| [merge sort tree](/merge-sort-tree/) or [wavelet tree](/wavelet-tree/) in rank space | $O(n \log n)$ | $O(n \log n)$ or $O(n)$ words | $O(\log^2 n)$ or $O(\log n)$ | word RAM |
| Chazelle (1988) | $O(n \log n)$ | $O(n)$ | $O(\log n)$ | word RAM |
| JaJa, Mortensen and Shi (2004) | $O(n \log n)$ (to be checked) | $O(n)$ | $O(\log n / \log \log n)$ | word RAM, rank space |
| [offline sweep](/offline-orthogonal-range-counting/), $q$ queries | | $O(n + q)$ | $O((n + q)\log(n + q))$ total | real RAM with ranks |

In $d$ dimensions the range tree counts in $O(\log^{d} n)$ time, or $O(\log^{d-1} n)$ with fractional cascading, with $O(n \log^{d-1} n)$ space.

## Bounds

- **Semigroup model, static.** Chazelle (1990): any structure that stores $m$ precomputed semigroup sums has a query (even a dominance query) that needs $\Omega((\log n / \log(2m/n))^{d-1})$ semigroup additions. So linear space forces $\Omega(\log^{d-1} n)$ time in the semigroup model.
- **Semigroup model, dynamic.** Fredman (1981): $n$ mixed insertions, deletions and queries need $\Omega(n \log^{d} n)$ semigroup operations.
- **Cell probe model.** Pătraşcu (2007): static two-dimensional counting with $S$ words of $w$ binary digits needs $\Omega(\log n / \log (S w / n))$ probes, so $\Omega(\log n / \log \log n)$ for near-linear space, matched by JaJa, Mortensen and Shi. Larsen (2012): for dynamic weighted two-dimensional counting, a structure with update time $t_u$ has query time $\Omega((\log n / \log (w t_u))^2)$ in the cell probe model; see [range searching lower bounds](/range-searching-lower-bound/).
- **Offline.** Chan and Pătraşcu (2010) count $n$ points in $n$ boxes offline in $O(n \sqrt{\log n})$ time on the word RAM.

## Reductions

- **To dominance counting.** In $d$ dimensions, $|P \cap Q|$ is the signed sum of $2^{d}$ dominance counts, one per corner of $Q$, so counting reduces to [dominance counting](/dominance-counting/) when subtraction is allowed.
- **From reporting.** A reporting structure counts in the time of reporting, $f(n) + O(k)$, which can be $\Theta(n)$; counting structures avoid the $k$ term.
- **Counting inversions.** The number of inversions of a permutation $\pi$ is the number of dominance pairs of the points $(i, \pi(i))$; see [counting inversions](/counting-inversions/) and [inversion count with a Fenwick tree](/inversion-count-with-fenwick-tree/).

## Applications

- Database query optimizers estimate the size of a selection before running it.
- Statistics: two-dimensional empirical distribution functions and Kendall's tau.
- Image processing: summed-area tables are the dense-grid version of dominance counting.

## References
