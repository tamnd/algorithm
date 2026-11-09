---
tag: 54MNZM
kind: theorem
slug: range-searching-lower-bound
name: Range searching lower bound
aliases:
- Chazelle lower bound for range searching
- semigroup lower bound for range searching
- Fredman lower bound for range queries
area: geometry/range-searching
level: research
summary: Lower bounds on the space-time trade-off for orthogonal and simplex range searching in the semigroup model.
prereqs: [orthogonal-range-searching, simplex-range-searching, lower-bound]
see_also: [simplex-range-searching, halfspace-range-searching, orthogonal-range-counting, dynamic-range-searching, pointer-machine, cell-probe-model, discrepancy-method, partition-tree]
sources:
  - paper: doi:10.1145/322276.322281
    title: Michael L. Fredman, A lower bound on the complexity of orthogonal range queries, Journal of the ACM 28(4), 1981, pages 696 to 705
    locator: the semigroup model for dynamic range queries and the Omega(n log^d n) bound for n operations (DOI to be checked)
  - paper: doi:10.1145/79147.79149
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, II. The arithmetic model, Journal of the ACM 37(3), 1990, pages 439 to 463
    locator: the static bound Omega((log n / log(2m/n))^(d-1)) for d-dimensional box queries with m storage (DOI to be checked)
  - paper: doi:10.1145/77600.77614
    title: Bernard Chazelle, Lower bounds for orthogonal range searching, I. The reporting case, Journal of the ACM 37(2), 1990, pages 200 to 212
    locator: pointer machine space Omega(n (log n / log log n)^(d-1)) for polylogarithmic reporting time (DOI to be checked)
  - paper: doi:10.1090/S0894-0347-1989-1001852-0
    title: Bernard Chazelle, Lower bounds on the complexity of polytope range searching, Journal of the American Mathematical Society 2(4), 1989, pages 637 to 666
    locator: Omega(n / sqrt(m)) in the plane and Omega(n / (m^(1/d) log n)) in R^d for simplex queries on random points (DOI to be checked)
  - book: isbn:9780821806746
    title: Pankaj K. Agarwal and Jeff Erickson, Geometric range searching and its relatives, in Advances in Discrete and Computational Geometry, Contemporary Mathematics 223, American Mathematical Society, 1999, pages 1 to 56
    locator: Section 3, Lower bounds (the semigroup arithmetic model, the pointer machine and the summary tables)
  - paper: doi:10.1145/1250790.1250803
    title: Mihai Pătraşcu, Lower bounds for 2-dimensional range counting, Proceedings of the 39th ACM Symposium on Theory of Computing (STOC), 2007, pages 40 to 46
    locator: cell probe bound Omega(log n / log(S w / n)) for static two-dimensional range counting (DOI to be checked)
---

Range searching lower bounds show how much space and query time any data structure must spend, in a model that is precise enough to prove something but broad enough to cover the known structures. The main model is the **semigroup arithmetic model** of Fredman and Yao, extended by Chazelle: points carry weights from a commutative semigroup, the structure stores sums of weights over chosen subsets, and a query adds stored sums, with only the additions counted. In this model Chazelle proved that $d$-dimensional box queries with $m$ words of storage need $\Omega((\log n / \log(2m/n))^{d-1})$ additions, and that simplex queries need $\Omega(n / \sqrt{m})$ additions in the plane. The first bound shows that [range trees](/range-tree/) are close to optimal; the second shows that the $O(\sqrt{n})$ query of linear-space [partition trees](/partition-tree/) cannot be improved. For reporting, Chazelle's bounds on the [pointer machine](/pointer-machine/) play the same role.

## Statement

**The semigroup arithmetic model.** Let $(S, +)$ be a commutative semigroup and let each point $p$ of a set $P$ of $n$ points carry a weight $w(p) \in S$. A **storage scheme of size $m$** consists of $m$ generators $g_1, \dots, g_m$, each a sum $g_j = \sum_{p \in G_j} w(p)$ over a set $G_j \subseteq P$. A range $R$ is answered by picking generators whose sets are pairwise disjoint and have union $P \cap R$, and adding them. The **query time** of $R$ is the least number of generators needed. Finding them is free; only the additions count. The scheme must be correct for every assignment of weights in every commutative semigroup, which is why the sets must cover $P \cap R$ exactly: no subtraction and no idempotence ($x + x = x$) may be used. A lower bound in this model applies to any algorithm whose only use of the weights is to add them.

**Theorem 1 (orthogonal ranges; Chazelle 1990).** For each fixed $d \ge 2$, if $P$ is a set of $n$ points drawn uniformly at random from the unit cube $[0, 1]^d$, then with high probability every storage scheme of size $m \ge n$ for $P$ has a query box whose query time is
$$\Omega\left( \left( \frac{\log n}{\log (2m / n)} \right)^{d - 1} \right).$$

**Theorem 2 (simplex ranges; Chazelle 1989).** If $P$ is a set of $n$ points drawn uniformly at random from the unit square, then with high probability every storage scheme of size $m$ for $P$ has a query triangle (in fact a strip) whose query time is $\Omega(n / \sqrt{m})$. For fixed $d \ge 3$ and $n$ random points in the unit cube, the bound is $\Omega(n / (m^{1/d} \log n))$ for some query simplex.

**Theorem 3 (dynamic orthogonal ranges; Fredman 1981).** In the dynamic version of the model, where an insertion or deletion may change the generators and is charged one unit per addition, there is a sequence of $n$ insertions, deletions and box queries in $\mathbb{R}^d$ that costs $\Omega(n \log^{d} n)$ additions in total.

**Theorem 4 (orthogonal reporting on a pointer machine; Chazelle 1990).** On a [pointer machine](/pointer-machine/), a structure that reports the points of $P$ in any $d$-dimensional box in $O(\log^{c} n + k)$ time, for a constant $c$ and output size $k$, needs $\Omega(n (\log n / \log \log n)^{d - 1})$ space in the worst case.

**Theorem 5 (cell probe; Pătraşcu 2007).** In the [cell probe model](/cell-probe-model/) with cells of $w$ bits, a static structure of $S$ cells for two-dimensional orthogonal range counting needs query time $\Omega(\log n / \log(S w / n))$; with $S = n \log^{O(1)} n$ and $w = \Theta(\log n)$ this is $\Omega(\log n / \log \log n)$.

## In plain words

A data structure for range counting stores some precomputed totals. When a question comes in, it adds up a few of these totals to get the answer. The lower bounds say that, whatever totals are chosen, some question will need many additions, unless a huge number of totals is stored.

For rectangles the penalty is small: a few factors of the logarithm. For triangles it is large: with memory proportional to the number of points, some triangle needs about the square root of the number of points in additions. The reason is that thin slanted strips can be placed in very many different ways, and the stored totals cannot fit inside most of them. These results assume that the totals can only be added, never subtracted, which covers maximum and minimum queries as well as counting by most known structures.

## Proof

The full proofs fill long papers; we give the plan of each, with the step that carries the bound.

**Exact covers.** Suppose a query adds generators $g_{j_1}, \dots, g_{j_t}$ and is correct for every semigroup. Take $S = (\mathbb{N}, +)$ and weights that are distinct powers of a large base: the sum is correct only if every point of $P \cap R$ is counted exactly once and no other point is counted. So the sets $G_{j_1}, \dots, G_{j_t}$ partition $P \cap R$, each is contained in $R$, and the query time is at least $|P \cap R| / \max_i |G_{j_i}|$. Every lower bound in this model therefore shows that, for some range $R$, all generator sets inside $R$ are small compared with $|P \cap R|$.

**Theorem 2, plan.** Consider long thin strips of width $\Theta(1/\sqrt{m})$ in the unit square; each holds about $n / \sqrt{m}$ of the random points. A generator set $G$ that fits inside many such strips in different directions must lie in their intersection, which is a small region, and random points are spread out, so with high probability no large set of points lies in the intersection of strips in two directions that differ by more than a small angle. Chazelle counts, over a suitable family of strips, the pairs (generator, strip containing it) weighted by the generator's size, and shows that the total is at most about $m$ times a constant, while each strip needs its $n/\sqrt{m}$ points covered. Averaging over the family gives a strip whose generators have $O(1)$ points on average, so $\Omega(n / \sqrt{m})$ of them are needed. The bound in $\mathbb{R}^d$ uses slabs of width $\Theta(m^{-1/d})$ and the same averaging, with a loss of a $\log n$ factor.

**Theorem 1, plan.** Here the ranges are boxes, and a generator set inside a box is covered efficiently only by boxes of roughly matching shape. Chazelle uses boxes whose side lengths range over $\Theta(\log n / \log(2m/n))$ scales in each of $d - 1$ directions, and shows that a random point set forces generators to be useful for only a few combinations of scales; a box chosen at a random combination of scales then needs one generator per combination, giving the $(d - 1)$-th power.

**Theorem 3, plan.** Fredman shows that each insertion must be added into the generators of many future queries and that with deletions the additions cannot be reused; a counting argument over a random sequence of operations on a grid gives $\log n$ for each of the $d$ coordinates.

**Theorem 4, plan.** On a pointer machine, each output point must be reached by following pointers from the root, so a query with output $k$ visits $O(\log^{c} n + k)$ cells, and those cells must hold the reported points densely. Chazelle builds a family of boxes, each containing about $\log^{c} n$ points, such that two boxes share few points; the structure must store, for each box, its points in $O(1)$ dense groups, and the small overlaps force total space $\Omega(n (\log n / \log \log n)^{d - 1})$.

**Theorem 5, plan.** Pătraşcu reduces from a communication game in which one player holds the query and the other the stored array; a round elimination argument over $\log n / \log(Sw/n)$ rounds shows that the query cannot finish faster.

## Consequences

- **Range trees are nearly optimal.** A [range tree](/range-tree/) for semigroup counting uses $m = O(n \log^{d-1} n)$ and answers with $O(\log^{d} n)$ additions; Theorem 1 with this $m$ gives $\Omega((\log n / \log \log n)^{d-1})$, so the gap is at most about one logarithmic factor.
- **Partition trees are optimal.** With $m = O(n)$, Theorem 2 gives $\Omega(\sqrt{n})$ in the plane, matched by Chan's [partition tree](/partition-tree/); see [simplex range searching](/simplex-range-searching/). Matoušek's trade-off $O((n / m^{1/d}) \log^{O(1)} n)$ is optimal up to polylogarithmic factors for all $n \le m \le n^{d}$.
- **Subtraction helps.** If weights form a group, counting in boxes is answered with $O(\log^{d-1} n)$ operations and less space, for example by inclusion and exclusion over dominance counts; so Theorem 1 really depends on the semigroup restriction. See [orthogonal range counting](/orthogonal-range-counting/).
- **Dynamic structures.** By Theorem 3, the $O(\log^{d} n)$ amortized updates and queries of dynamic range trees are optimal in this model; see [dynamic range searching](/dynamic-range-searching/).
- **Halfspaces.** Brönnimann, Chazelle and Pach proved a weaker semigroup bound for halfspace queries; see [halfspace range searching](/halfspace-range-searching/).

## Tightness

The bounds hold for random point sets, so they are lower bounds for the worst case over inputs and for the typical case.

| problem | storage $m$ | lower bound | best upper bound |
|---|---|---|---|
| boxes in $\mathbb{R}^2$, semigroup | $n \log n$ | $\Omega(\log n / \log \log n)$ | $O(\log^{2} n)$ by a range tree |
| triangles in $\mathbb{R}^2$, semigroup | $n$ | $\Omega(\sqrt{n})$ | $O(\sqrt{n})$, Chan (2012) |
| triangles in $\mathbb{R}^2$, semigroup | $n^{2}$ | $\Omega(1)$ | $O(\log n)$ with cuttings |
| boxes in $\mathbb{R}^2$, cell probe counting | $n \log^{O(1)} n$ | $\Omega(\log n / \log \log n)$ | $O(\log n / \log \log n)$ with $O(n)$ words |

For $n = 2^{20}$ and triangles, Theorem 2 gives, up to the constant factor, $n / \sqrt{m} = 1024$ additions for $m = n$, $32$ for $m = n^{3/2}$, and $1$ for $m = n^{2}$. For boxes in the plane, Theorem 1 gives $\log_2 n / \log_2 (2m/n) = 20$ for $m = n$ and about $20 / \log_2 40 \approx 3.8$ for $m = n \log_2 n$. Rectangles are much easier than triangles.

## History

Fredman (1981) introduced the semigroup model and proved the dynamic bound of Theorem 3. Yao (1982) studied static one-dimensional range queries in the same model and found an inverse Ackermann trade-off. Chazelle proved the static orthogonal bounds, in the arithmetic model and on the pointer machine, in two papers published in 1990, and the polytope bound in 1989, using random point sets and averaging over families of ranges. Brönnimann, Chazelle and Pach (1993) treated halfspaces, Chazelle and Rosenberg (1996) proved pointer machine bounds for simplex reporting, and Pătraşcu (2007) and Larsen (2012) proved the cell probe bounds for counting. The links between these bounds and discrepancy theory are developed in Chazelle's book on the [discrepancy method](/discrepancy-method/).

## References
