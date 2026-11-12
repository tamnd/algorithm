---
tag: KSDEHS
kind: problem
slug: dominance-counting
name: Dominance counting
aliases:
- 2D dominance range counting
- dominance query
- dominance range counting
area: geometry/range-searching
level: core
summary: Count the points that dominate a query point in both coordinates, the basic two-dimensional counting case.
prereqs: [orthogonal-range-searching]
see_also: [orthogonal-range-counting, offline-orthogonal-range-counting, counting-inversions, inversion-count-with-fenwick-tree, persistent-segment-tree, wavelet-tree, range-searching-lower-bound, three-sided-range-query]
sources:
  - book: isbn:9781498711395
    title: Jacob E. Goodman, Joseph O'Rourke and Csaba D. Tóth (eds.), Handbook of Discrete and Computational Geometry, third edition, CRC Press, 2017
    locator: Chapter 40, Range searching, by Pankaj K. Agarwal, Section 40.1 (lower bounds stated for dominance queries) and Section 40.2
  - book: isbn:9780387961316
    title: Franco P. Preparata and Michael Ian Shamos, Computational Geometry, An Introduction, Springer, 1985
    locator: Chapter 2, Section 2.3, the locus approach to range counting through dominance numbers (section number to be checked)
  - paper: doi:10.1145/79147.79149
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, II. The arithmetic model, Journal of the ACM 37(3), 1990, pages 439 to 463
    locator: the semigroup lower bound holds already for dominance queries (DOI to be checked)
  - paper: doi:10.1145/1250790.1250797
    title: Mihai Pătraşcu, Lower bounds for 2-dimensional range counting, STOC 2007, pages 40 to 46
    locator: the cell probe lower bound for two-dimensional dominance counting (DOI to be checked)
---

Dominance counting is the problem of storing a set $P$ of $n$ points in the plane so that, for a query point $q$, the number of points $p \in P$ with $p_x \ge q_x$ and $p_y \ge q_y$ can be returned. It is [orthogonal range counting](/orthogonal-range-counting/) with a two-sided box $[q_x, \infty) \times [q_y, \infty)$, and every box count is a signed sum of four dominance counts. The lower bounds for orthogonal range counting in the semigroup and cell probe models are proved for dominance queries, so this special case is as hard as the general one.

## In plain words

One point dominates another if it is at least as far right and at least as far up. A set of points is stored, and a question gives a point. The answer is how many stored points dominate it, that is, how many lie in the quarter of the plane above and to the right of it, border included.

The count for any rectangle follows from four such counts, one for each corner, combined with plus and minus signs. So a fast method for this simple question gives a fast method for counting points in rectangles. Counting the pairs of points where one dominates the other is the same as counting the out-of-order pairs of a list.

## Definition

**Notation.** $P$ is the input point set, $n = |P|$, $p = (x, y)$ a point, $d = 2$ (the definition extends to any $d$). The output is a count, with no output size term; for the reporting version the output size is $k$. $\mathrm{orient}$ and $\mathrm{incircle}$ are not used.

A point $p$ *dominates* a point $q$ if $p_i \ge q_i$ for every coordinate $i$. Points with equal coordinates dominate each other, and every point dominates itself.

**Input.** A multiset $P$ of $n$ points in $\mathbb{R}^2$; repeated points count with multiplicity.

**Query.** A point $q$.

**Output.** $\mathrm{dom}(q) = |\{p \in P : p_x \ge q_x \text{ and } p_y \ge q_y\}|$.

The opposite orientation, counting the points dominated by $q$ ($p \le q$ in both coordinates), is the same problem after negating all coordinates. Strict dominance ($>$ instead of $\ge$) is the same problem after replacing $q$ by the next representable point; with integer coordinates, by $q + (1, 1)$.

## Variants

- **Dominance reporting.** Report the dominating points; a [priority search tree](/priority-search-tree/) does it in $O(\log n + k)$ time with linear space, since a two-sided query is a [three-sided query](/three-sided-range-query/).
- **Offline dominance counting.** All query points are known; one sweep over $x$ with a [Fenwick tree](/fenwick-tree/) over $y$ answers all of them; see [offline orthogonal range counting](/offline-orthogonal-range-counting/).
- **Dominance pairs within $P$.** Count the pairs $(p, p')$ of points of $P$ with $p'$ dominating $p$. For the points $(i, \pi(i))$ of a permutation, the non-dominance pairs are the inversions; see [counting inversions](/counting-inversions/).
- **Higher dimensions.** In $\mathbb{R}^d$, dominance counting has the same lower bounds as box counting, and a range tree answers it in $O(\log^{d-1} n)$ time with fractional cascading.

## Examples

Take $P = \{(2,3), (5,4), (9,6), (4,7), (8,1), (7,2), (3,8), (6,6)\}$.

| query $q$ | dominating points | $\mathrm{dom}(q)$ |
|---|---|---|
| $(4, 3)$ | $(5,4), (9,6), (4,7), (6,6)$ | 4 |
| $(6, 6)$ | $(9,6), (6,6)$ | 2 |
| $(5, 5)$ | $(9,6), (6,6)$ | 2 |
| $(0, 0)$ | all 8 points | 8 |
| $(10, 0)$ | none | 0 |

The query $(4, 3)$ counts $(4,7)$, whose $x$ equals $q_x$, because dominance is not strict. The query $(6,6)$ counts the point $(6,6)$ itself and the point $(9,6)$, which has the same $y$. For each point of $P$, the number of other points of $P$ that dominate it is $5, 2, 0, 0, 1, 1, 0, 1$ in the order listed, $10$ dominance pairs in all.

## Known algorithms

All bounds are worst case for $n$ points in the plane.

| method | preprocessing | space | query | model |
|---|---|---|---|---|
| linear scan | none | $O(n)$ | $O(n)$ | any |
| [range tree](/range-tree/) on $x$ with sorted $y$-lists | $O(n \log n)$ | $O(n \log n)$ | $O(\log^2 n)$ | real RAM |
| [layered range tree](/layered-range-tree/) | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$ | real RAM |
| [persistent segment tree](/persistent-segment-tree/) over $y$, versions by $x$ | $O(n \log n)$ | $O(n \log n)$ | $O(\log n)$ | real RAM, ranks |
| [wavelet tree](/wavelet-tree/) in rank space | $O(n \log n)$ | $O(n)$ words | $O(\log n)$ | word RAM |
| JaJa, Mortensen and Shi (2004) | see paper | $O(n)$ | $O(\log n / \log \log n)$ | word RAM, rank space |
| offline sweep with a [Fenwick tree](/fenwick-tree/), $q$ queries | | $O(n + q)$ | $O((n + q) \log (n + q))$ total | real RAM with ranks |

The persistent segment tree inserts the points in decreasing order of $x$; the version after the points with $x \ge q_x$ counts those with $y \ge q_y$ in one root-to-leaf walk.

## Bounds

- **Semigroup model.** Chazelle (1990) proved his lower bound for dominance queries: a structure storing $m$ semigroup sums needs $\Omega((\log n / \log (2m/n))^{d-1})$ additions for some query. In the plane, linear space forces $\Omega(\log n)$.
- **Cell probe model.** Pătraşcu (2007) proved that static two-dimensional dominance counting with $S$ words of space needs $\Omega(\log n / \log (S w / n))$ probes on a word RAM with $w$-digit words. Box counting is no harder than four dominance counts, so the bound is tight for both up to constants.
- **Offline.** Counting the dominance pairs of $n$ points is at least as hard as counting inversions; Chan and Pătraşcu (2010) do it in $O(n \sqrt{\log n})$ time on the word RAM.

See [range searching lower bounds](/range-searching-lower-bound/) for the models.

## Reductions

- **Box counting to dominance counting.** For integer coordinates, with $D(x, y)$ the number of points with $p_x \le x$ and $p_y \le y$ (the points dominated by $(x, y)$, the opposite orientation of $\mathrm{dom}$),

$$|P \cap [a_1, b_1] \times [a_2, b_2]| = D(b_1, b_2) - D(a_1 - 1, b_2) - D(b_1, a_2 - 1) + D(a_1 - 1, a_2 - 1).$$

This uses subtraction, so it is valid in groups, not in semigroups such as $\max$.

- **Inversions to dominance pairs.** For a permutation $\pi$, the pairs $i < j$ with $\pi(i) > \pi(j)$ are the pairs of points $(i, \pi(i))$ where neither dominates the other; their number is $\binom{n}{2}$ minus the number of dominance pairs.
- **Point enclosure.** Counting the rectangles that contain a query point is four-dimensional dominance counting; see [orthogonal point enclosure](/orthogonal-point-enclosure/).

## Applications

- Kendall's tau rank correlation, computed from the number of concordant pairs, which are dominance pairs.
- Skyline (Pareto front) queries in databases: a point is on the skyline when no other point dominates it.
- Two-dimensional cumulative frequency tables and summed-area tables.

## References
