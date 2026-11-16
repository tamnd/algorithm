---
tag: APHJEF
kind: concept
slug: hyperclique-hypothesis
name: Hyperclique hypothesis
aliases:
- hyperclique conjecture
area: complexity/fine-grained-complexity
level: research
summary: "The hypothesis that finding a k-hyperclique in a d-uniform hypergraph with k > d >= 3 needs n^(k-o(1)) time. The 2026 preprints do not refute it."
prereqs: [hyperclique, conditional-lower-bound]
see_also: [hyperclique, min-weight-k-clique-hypothesis, zero-k-clique-hypothesis, strong-exponential-time-hypothesis, max-sat, tensor-rank, combinatorial-bmm-conjecture, maximum-csp]
sources:
  - paper: doi:10.1137/1.9781611975031.80
    title: "Andrea Lincoln, Virginia Vassilevska Williams and R. Ryan Williams, Tight hardness for shortest cycles and paths in sparse graphs, SODA 2018, 1236-1252 (arXiv:1712.08147)"
    locator: "Hypothesis 1.4 of the arXiv version ((l, k)-Hyperclique), Section 7 (the evidence: no faster algorithm for k > 2, the reduction from Max-k-SAT, and the result of Abboud, Bringmann, Dell and Nederlof that a faster algorithm for (l, 4)-hyperclique refutes the Exact Weight l-Clique hypothesis), Section 8 (maximal rank and border rank of the generalized matrix product tensor) and Appendix C"
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "R. Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: Max-2-SAT in O(2^(omega n/3) poly(n)) time, the case d = 2
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: Section 5.3 and Corollary 39 (the zero-weight, min-weight and max-weight k-clique hypotheses are refuted) and the list of refuted hypotheses in the introduction, which does not include hyperclique; not yet refereed
---

The hyperclique hypothesis says that, for constants $k > d \ge 3$, deciding whether a $d$-uniform hypergraph on $n$ vertices has a [hyperclique](/hyperclique/) of $k$ vertices needs time $n^{k - o(1)}$. So for hypergraphs, unlike graphs, trying all $k$-sets is essentially optimal. Lincoln, Vassilevska Williams and Williams stated it in 2018. Its main support is that Max-3-SAT and related problems reduce to it, and that the algebraic methods that help for graphs provably fail for hypergraphs.

In October 2026, preprints refuted the 3SUM conjecture, the APSP conjecture, and the zero-weight and min-weight k-clique hypotheses. They do not mention the hyperclique hypothesis, and their methods are about triangles in graphs. So the hyperclique hypothesis still stands. One piece of support for it is gone: a faster hyperclique algorithm used to imply a refutation of the exact weight clique hypothesis, which is now refuted anyway.

## In plain words

A hypergraph has links that each join a fixed number of points, such as three. A hyperclique is a group of points where every possible link inside the group is present.

For ordinary graphs, with links of two points, clever algebra finds such groups faster than checking every group. The hypothesis is a bet that, for links of three or more points, nothing beats checking every group by a real power of the number of points.

If the bet is wrong, some hard puzzles about true and false values, which now take time close to two to the power of the number of variables, could be solved much faster.

## The idea

### Hypothesis (hyperclique)

For all constants $k > d \ge 3$ and every $\varepsilon > 0$, no algorithm finds a $k$-hyperclique in a $d$-uniform hypergraph on $n$ vertices in time $O(n^{k - \varepsilon})$ (Lincoln, Vassilevska Williams and Williams, SODA 2018, Hypothesis 1.4).

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits.
- There are no numbers in the input: the hypergraph is unweighted, and it may be dense, with $\Theta(n^d)$ hyperedges.
- Lincoln et al. do not single out randomized algorithms. No algorithm of either kind is known that beats the bound.
- Notation: Lincoln et al. write the $(\ell, k)$-Hyperclique Hypothesis, with $\ell$ the size of the hyperclique and $k$ the size of a hyperedge. This page writes $k$ and $d$.

### Why $d \ge 3$

For $d = 2$ the hypothesis is false: $k$-clique in graphs takes time $O(n^{\omega k/3})$ for $k$ divisible by 3, with $\omega < 2.371552$. The method groups the $k$ parts into three and multiplies matrices. For $d \ge 3$, a hyperedge can join vertices from three groups at once, and the grouping no longer gives a matrix product. Lincoln et al. (Section 8) show more: the rank and the border rank of the tensor of the generalized matrix product that hyperclique needs are maximal. So no method in the style of Strassen, which saves on the [tensor rank](/tensor-rank/), can give any speedup.

### Evidence

- **Algorithms.** For $d \ge 3$, no algorithm in time $O(n^{k - \varepsilon})$ is known (Lincoln et al., Section 7).
- **Max-SAT.** Williams (2007) reduced Max-3-SAT to 4-hyperclique in 3-uniform hypergraphs, and Max-$d$-SAT reduces to $k$-hyperclique in $d$-uniform hypergraphs for $k > d$. So the hypothesis is implied by the hypothesis that Max-$d$-SAT has no algorithm in time $O(2^{(1 - \delta) n})$. For [Max-2-SAT](/max-2-sat/), the case $d = 2$, the reduction gives the algorithm in time $O(2^{\omega n/3})$ up to polynomial factors (Williams 2005), and no such algorithm is known for [Max-3-SAT](/max-sat/).
- **Constraint problems.** Lincoln et al. (Appendix C) extend the reduction to constraint satisfaction problems with constraints given by polynomials of degree $d$. See [maximum CSP](/maximum-csp/).
- **A link to weighted cliques.** Lincoln et al. cite a result of Abboud, Bringmann, Dell and Nederlof: if the hypothesis is false for $d = 4$ and some $k$, then the Exact Weight $k$-Clique hypothesis is false.

### Status in 2026

- **The hypothesis: open.** The preprints of Alman and Vassilevska Williams (arXiv:2610.06783) and of Chan, Itakura, Ma and Yu (arXiv:2610.42012), both not yet refereed, do not mention it. Their algorithms solve weighted triangle problems in graphs with algebraic methods, and by the rank barrier above, methods of the Strassen type cannot by themselves give a speedup for $d \ge 3$.
- **Lost support.** By the result of Abboud, Bringmann, Dell and Nederlof, a refutation of the hyperclique hypothesis for $d = 4$ would also refute the Exact Weight $k$-Clique hypothesis. This was evidence, because it meant that a fast hyperclique algorithm would also need a breakthrough for weighted cliques. Alman and Vassilevska Williams now refute the [zero-k-clique hypothesis](/zero-k-clique-hypothesis/) for polynomial weights, if the preprint is correct, so this evidence is gone. The link goes only from hyperclique to weighted cliques, so the refutation does not refute the hyperclique hypothesis.
- **What else stands.** SETH, the plain OMv conjecture, the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/) and the triangle detection hypothesis are also not affected. The Max-$k$-SAT hypothesis is not affected.

### Pitfalls

- The case $d = 2$ is excluded. A statement of the hypothesis "for all $d$" is false.
- Dense and sparse instances differ. The hypothesis is about dense hypergraphs, with the time measured in $n$.
- Hyperclique is not clique in the graph of covered pairs. A set can be a clique there without being a hyperclique; see the example on [hyperclique detection](/hyperclique/).

## Examples

**From Max-3-SAT.** Split $n$ variables into $k = 4$ groups of $n/4$, so each part has $N = 2^{n/4}$ vertices, one for each assignment of its group. An algorithm for 4-hyperclique in time $O(N^{4 - \varepsilon})$ would give time $O(2^{(1 - \varepsilon/4) n})$ up to polynomial factors. With $\varepsilon = 0.5$ the base is $2^{1 - 0.125} \approx 1.834$, and with $\varepsilon = 0.1$ it is about $1.966$. Any constant $\varepsilon > 0$ gives a base below 2.

**A small instance.** In the 3-uniform hypergraph on $\{0, 1, 2, 3, 4\}$ with all triples except $\{0,3,4\}$ and $\{2,3,4\}$, the 4-hypercliques are $\{0,1,2,3\}$ and $\{0,1,2,4\}$, and there is no 5-hyperclique. The detection page works this out.

## Where it is used

- **Max-SAT and constraint problems.** The reduction makes the hypothesis a fine-grained form of the belief that Max-3-SAT needs time close to $2^n$.
- **Sparse graph problems.** Lincoln et al. use it with related hypotheses for conditional bounds on sparse graph problems.
- **After 2026.** With the weighted clique hypotheses refuted, hyperclique is one of the few clique-type hypotheses that still stand, together with the unweighted $k$-clique hypothesis.

## References
