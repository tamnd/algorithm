---
tag: CHATDR
kind: concept
slug: min-weight-k-clique-hypothesis
name: Min-weight k-clique hypothesis
aliases:
- min-weight k-clique conjecture
area: complexity/fine-grained-complexity
level: research
summary: "The hypothesis that finding a minimum weight k-clique needs n^(k-o(1)) time. For k = 3 it is the APSP conjecture. A 2026 preprint refutes it for polynomial weights."
prereqs: [clique, negative-triangle, apsp-conjecture]
see_also: [zero-k-clique-hypothesis, apsp-conjecture, negative-triangle, apsp-negative-triangle-equivalence, hyperclique-hypothesis, parameterized-clique, valiant-lee-theorem, fine-grained-reduction]
sources:
  - paper: doi:10.1137/1.9781611975031.80
    title: "Andrea Lincoln, Virginia Vassilevska Williams and R. Ryan Williams, Tight hardness for shortest cycles and paths in sparse graphs, SODA 2018, 1236-1252 (arXiv:1712.08147)"
    locator: Hypothesis 1.1 of the arXiv version (Min Weight k-Clique, weights in [1, n^(ck)]) and the abstract (no O(n^2 + m n^(1-e)) algorithm for minimum weight (2l+1)-cycle in directed weighted graphs with m = Theta(n^(1+1/l)))
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the subcubic equivalence of APSP and negative triangle, and with it minimum weight triangle
  - paper: "Liam Roditty and Virginia Vassilevska Williams, Minimum weight cycles and triangles: equivalences and algorithms, Proceedings of the 52nd IEEE Symposium on Foundations of Computer Science (FOCS 2011), 180-189"
    locator: the equivalence of minimum weight triangle and minimum weight cycle with APSP
  - paper: doi:10.1109/FOCS.2015.16
    title: "Amir Abboud, Arturs Backurs and Virginia Vassilevska Williams, If the current clique algorithms are optimal, so is Valiant's parser, FOCS 2015, 98-117 (arXiv:1504.01431)"
    locator: the abstract (k-clique lower bounds for context-free parsing, RNA folding and Dyck edit distance)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: "Theorem 2 (APSP in O(n^2.9995) time), Section 5.3 and Corollary 39 (min-weight and max-weight k-clique in deterministic O(n^(k-0.0017 floor(k/3))) time; the hypotheses of [AL13, LVW18, BDT16] are refuted, also on general graphs); not yet refereed"
---

The min-weight k-clique hypothesis says that, for a constant $k \ge 3$, finding $k$ pairwise adjacent vertices of an edge-weighted graph with the least total weight on their $\binom{k}{2}$ edges needs time $n^{k - o(1)}$, for integer weights in a range polynomial in $n$. For $k = 3$, minimum weight triangle is subcubic equivalent to [all-pairs shortest paths](/all-pairs-shortest-paths/), so the case $k = 3$ is the [APSP conjecture](/apsp-conjecture/). Lincoln, Vassilevska Williams and Williams stated the hypothesis in 2018 and used larger $k$ to prove tight bounds for shortest cycles in sparse graphs.

In October 2026, preprints refuted the 3SUM conjecture and the APSP conjecture. Alman and Vassilevska Williams also find a minimum weight $k$-clique in deterministic time $O(n^{k - 0.0017 \lfloor k/3 \rfloor})$, so the min-weight k-clique hypothesis is refuted for every $k \ge 3$ with polynomial weights. The preprint is not yet refereed. The hypothesis for unweighted $k$-clique is a different statement and still stands.

## In plain words

Every pair of points is joined by a line with a cost. You want a fixed number of points, all joined to each other, whose lines cost the least in total.

The plain method tries every group. The hypothesis was a bet that no method does better by a real power of the number of points.

For groups of three, this is the same question as finding all the cheapest routes in a road map. The bet for groups of three was lost in 2026, and the same new method also wins for larger groups. The gain is very small, but it is a real power.

## The idea

### Hypothesis (min-weight k-clique)

For a constant $k \ge 3$, there is a constant $c > 1$ such that no algorithm finds a minimum weight $k$-clique in an $n$-vertex graph with integer edge weights in $[1, n^{ck}]$ in time $O(n^{k - \varepsilon})$ for any $\varepsilon > 0$ (Lincoln, Vassilevska Williams and Williams, SODA 2018, Hypothesis 1.1).

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits.
- The weights are positive integers bounded by a polynomial in $n$. Adding the same constant to every edge adds $\binom{k}{2}$ times that constant to every $k$-clique, so negative weights give the same problem.
- The graph is dense and given by its $\Theta(n^2)$ weights.
- Lincoln et al. do not single out randomized algorithms. The refuting algorithm is deterministic, so this choice does not matter for the refutation.

The max-weight form asks for the largest total weight. Negating every weight turns one form into the other.

### Relation to APSP and to the other forms

- **$k = 3$.** Minimum weight triangle is subcubic equivalent to APSP and to [negative triangle](/negative-triangle/) (Vassilevska Williams and Williams 2010; Roditty and Vassilevska Williams 2011). So the hypothesis for $k = 3$ is the APSP conjecture.
- **Larger $k$.** An $O(n^{k - \varepsilon})$ algorithm for minimum weight $k$-clique gives an $O(n^{k + 1 - \varepsilon})$ algorithm for $k + 1$: fix one vertex in all $n$ ways and move the weights of its edges onto the other edges. No reduction in the other direction is known. So the hypothesis for a larger $k$ implies the hypothesis for every smaller $k$; it is the stronger assumption, and it gave bounds that APSP alone could not give.
- **Exact weight.** For triangles, minimum weight reduces to exact weight (Vassilevska Williams and Williams 2013). See [zero-k-clique hypothesis](/zero-k-clique-hypothesis/).

### Status in 2026

- **The hypothesis: refuted, if the preprint is correct.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) prove in Corollary 39 that, for constants $k \ge 3$ and $\nu \ge 1$, the minimum and maximum weight $k$-cliques of a complete $k$-partite graph with integer weights of absolute value at most $n^{\nu}$ can be found in deterministic time $O(n^{k - 0.0017 \lfloor k/3 \rfloor})$. They state that the Zero-Weight, Min-Weight and Max-Weight $k$-Clique hypotheses with polynomially bounded weights are refuted, also on general graphs. For the max-weight case they use a reduction of Vassilevska Williams and Williams (2013, Theorem 3.3), at an extra cost of $O(\log^2 n)$, which does not change the exponent.
- **The case $k = 3$.** This is the refutation of the APSP conjecture: APSP and the min-plus product take time $O(n^{2.9995})$ (Theorem 2).
- **What still stands.** Unweighted $k$-clique is not affected; it takes time $O(n^{\omega k / 3})$ for $k$ divisible by 3, and no faster algorithm is claimed. The [hyperclique hypothesis](/hyperclique-hypothesis/), SETH and the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/) also stand. The conditional bounds proved from the min-weight k-clique hypothesis no longer hold as stated.

### Pitfalls

- The saving $0.0017 \lfloor k/3 \rfloor$ is the same for $k = 3, 4, 5$. A refutation for all $k$ does not mean a large saving for large $k$.
- The weight range matters. With weights of polylogarithmic size, minimum weight triangle was already faster, through the $\tilde{O}(M n^{\omega})$ algorithm for the min-plus product.
- "k-clique hypothesis" without "weight" means the unweighted problem, with the bound $n^{\omega k/3 - o(1)}$. It is a different statement.

## Examples

**A small instance.** Take $K_5$ on $0, \ldots, 4$ with the weights $w(0,1) = 3$, $w(0,2) = -1$, $w(0,3) = 4$, $w(0,4) = -5$, $w(1,2) = 2$, $w(1,3) = -2$, $w(1,4) = 6$, $w(2,3) = -3$, $w(2,4) = 1$ and $w(3,4) = -4$. The minimum weight triangle is $\{2, 3, 4\}$ with weight $-3 + 1 - 4 = -6$. The minimum weight 4-clique is $\{0, 2, 3, 4\}$ with weight $-8$, and the maximum weight 4-clique is $\{0, 1, 2, 4\}$ with weight 6.

**Positive weights.** Add 6 to every weight, so that all weights are in $[1, 12]$, as in Hypothesis 1.1. A triangle gains $3 \times 6 = 18$ and a 4-clique gains $6 \times 6 = 36$. The minimum weight triangle is still $\{2, 3, 4\}$, now with weight 12, and the minimum weight 4-clique is still $\{0, 2, 3, 4\}$, now with weight 28.

**The tight bound for cycles.** For $\ell = 2$, Lincoln et al. show, from the hypothesis for 5-cliques, that minimum weight 5-cycle in directed weighted graphs with $m = \Theta(n^{3/2})$ edges has no $O(n^2 + m n^{1 - \varepsilon})$ algorithm. The known algorithm takes time $\tilde{O}(m n) = \tilde{O}(n^{5/2})$. With the 2026 algorithm for 5-cliques, in time $O(n^{4.9983})$, this conditional bound no longer holds as stated.

## Where it is used

- **Shortest cycles in sparse graphs.** Lincoln, Vassilevska Williams and Williams prove that the $\tilde{O}(mn)$ algorithms for minimum weight $(2\ell+1)$-cycle and for shortest cycle in directed weighted graphs are optimal at the densities $m = \Theta(n^{1 + 1/\ell})$, conditional on the hypothesis.
- **Unweighted sparse problems.** The same paper derives bounds for $k$-cycle, shortest cycle, radius, the Wiener index and APSP in unweighted sparse graphs from related hypotheses.
- **Parsing and RNA folding.** Abboud, Backurs and Vassilevska Williams (FOCS 2015) prove lower bounds for context-free parsing with a fixed grammar, RNA folding and Dyck edit distance from the unweighted $k$-clique problem. Those bounds are not affected. See [Valiant and Lee theorem](/valiant-lee-theorem/).
- **Weighted geometric problems.** Backurs, Dikkala and Tzamos (ICALP 2016) used the max-weight form for bounds on maximum weight rectangles. Those bounds are lost if the preprint is correct.

## References
