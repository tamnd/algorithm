---
tag: D3QD52
kind: problem
slug: hyperclique
name: Hyperclique detection
aliases:
- k-hyperclique detection
area: complexity/fine-grained-complexity
level: research
summary: "Decide whether a d-uniform hypergraph on n vertices has k vertices whose every d-subset is a hyperedge. For d at least 3, no known algorithm beats n^k by a polynomial factor."
prereqs: [hypergraph, clique]
see_also: [hyperclique-hypothesis, min-weight-k-clique-hypothesis, zero-k-clique-hypothesis, max-sat, max-2-sat, parameterized-clique, tensor-rank, maximum-csp]
sources:
  - paper: doi:10.1137/1.9781611975031.80
    title: "Andrea Lincoln, Virginia Vassilevska Williams and R. Ryan Williams, Tight hardness for shortest cycles and paths in sparse graphs, SODA 2018, 1236-1252 (arXiv:1712.08147)"
    locator: "Hypothesis 1.4 of the arXiv version ((l, k)-Hyperclique, an l-hyperclique in a k-uniform hypergraph), Section 7 (no known algorithm in n^(l-e) time for k > 2; the reduction of Max-k-SAT to hyperclique by Williams), Section 8 (the generalized matrix product tensor has maximal rank and border rank) and Appendix C (constraint satisfaction problems)"
  - paper: doi:10.1016/j.tcs.2005.09.023
    title: "R. Ryan Williams, A new algorithm for optimal 2-constraint satisfaction and its implications, Theoretical Computer Science 348(2-3), 2005, 357-365 (conference version in ICALP 2004)"
    locator: Max-2-SAT in O(2^(omega n/3) poly(n)) time through k-clique in graphs
  - paper: "R. Ryan Williams, Algorithms and resource requirements for fundamental problems, PhD thesis, Carnegie Mellon University, 2007"
    locator: the reduction from Max-3-SAT to 4-hyperclique in 3-uniform hypergraphs, as cited in Section 7 of Lincoln, Vassilevska Williams and Williams
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: the list of refuted hypotheses in the introduction and in Section 5.3, which does not include hyperclique; not yet refereed
---

Hyperclique detection asks whether a $d$-uniform hypergraph has $k$ vertices such that every $d$ of them form a hyperedge. For $d = 2$ it is the [clique](/clique/) problem in graphs, where fast matrix multiplication gives a polynomial speedup over trying all $k$-sets. For $d \ge 3$ no such speedup is known: the best algorithms take time $n^{k - o(1)}$. This gap is the basis of the [hyperclique hypothesis](/hyperclique-hypothesis/).

The problem matters because Max-$d$-SAT and other constraint problems with constraints on $d$ variables reduce to it. A polynomially faster algorithm for hyperclique would give exponentially faster algorithms for those problems.

## In plain words

A hypergraph is like a graph, but each link joins a fixed number of points at once, for example three. A hyperclique is a group of points such that every possible link of that size inside the group is present.

The question is: for a fixed group size, is there such a group? Checking every group of points works. For ordinary graphs, where each link joins two points, clever algebra does better. When each link joins three or more points, nobody knows a method that does better by a real power of the number of points.

## Definition

**Hyperclique detection**

- Instance: a $d$-uniform hypergraph $H = (V, E)$ with $|V| = n$ and $E \subseteq \binom{V}{d}$, for constants $k > d \ge 2$.
- Question: is there a set $S \subseteq V$ with $|S| = k$ such that every $d$-subset of $S$ is in $E$?

**The model.** The measure is the time on the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, as a function of $n$, for constant $k$ and $d$. The hypergraph is given as a list of hyperedges or as a $d$-dimensional table, and it may be dense, with $|E| = \Theta(n^d)$.

**Notation.** This page writes $k$ for the size of the hyperclique and $d$ for the size of a hyperedge. Lincoln, Vassilevska Williams and Williams (SODA 2018) write an $\ell$-hyperclique in a $k$-uniform hypergraph. So their $(\ell, k)$ is $(k, d)$ here.

**The $k$-partite form.** The vertex set is split into $k$ parts, each hyperedge has its $d$ vertices in $d$ different parts, and a hyperclique takes one vertex from each part. A general instance reduces to this form with $k$ copies of the vertex set.

## Variants

- **Graphs, $d = 2$.** This is $k$-clique, solvable in time $O(n^{\omega k/3})$ for $k$ divisible by 3, with $\omega < 2.371552$. It is $W[1]$-complete when $k$ is the parameter; see [parameterized clique](/parameterized-clique/).
- **Search and counting.** Find a hyperclique, or count them. In the $k$-partite form, search reduces to detection by halving the parts.
- **Weighted forms.** Hyperedges carry weights, and the question asks for a hyperclique of minimum total weight or of weight exactly 0. These generalize the [min-weight k-clique](/min-weight-k-clique-hypothesis/) and [zero-k-clique](/zero-k-clique-hypothesis/) problems.
- **Sparse hypergraphs.** The time is measured in the number $m$ of hyperedges. This is a different regime from the dense one above.

## Examples

**A 3-uniform hypergraph.** Take $V = \{0, 1, 2, 3, 4\}$ and the 8 hyperedges $\{0,1,2\}$, $\{0,1,3\}$, $\{0,2,3\}$, $\{1,2,3\}$, $\{0,1,4\}$, $\{0,2,4\}$, $\{1,2,4\}$ and $\{1,3,4\}$. Only $\{0,3,4\}$ and $\{2,3,4\}$ of the 10 triples are missing. With $k = 4$, the sets $\{0,1,2,3\}$ and $\{0,1,2,4\}$ are hypercliques. The other three 4-sets each contain a missing triple: $\{0,1,3,4\}$ contains $\{0,3,4\}$, $\{1,2,3,4\}$ contains $\{2,3,4\}$, and $\{0,2,3,4\}$ contains both. With $k = 5$ there is no hyperclique.

**Not a clique in the shadow.** In the same hypergraph, every pair of vertices lies in some hyperedge; for example $\{3, 4\}$ lies in $\{1,3,4\}$. So the graph of covered pairs is the complete graph on 5 vertices, and it has a 5-clique, but the hypergraph has no 5-hyperclique. Hyperclique cannot be reduced to clique in this simple way.

**A satisfiability instance.** Take the 3-CNF formula $(x_1 \vee x_2 \vee \neg x_3) \wedge (\neg x_1 \vee x_3 \vee x_4) \wedge (x_2 \vee \neg x_4) \wedge (\neg x_2 \vee \neg x_3 \vee \neg x_4) \wedge (x_1 \vee \neg x_2 \vee x_4)$. Make one part per variable with two vertices, true and false, so $k = 4$ and $d = 3$. Put in a hyperedge for three values in three different parts unless they falsify a clause whose variables all lie in those three parts. Of the $4 \times 8 = 32$ possible hyperedges, 24 remain. The 4-hypercliques are exactly the satisfying assignments, and there are 5 of each.

## Known algorithms

All bounds are unconditional.

- **Brute force.** Try all $\binom{n}{k}$ sets in time $O(n^k)$.
- **$d = 2$.** Time $O(n^{\omega k/3})$ by the method of Nešetřil and Poljak, for $k$ divisible by 3.
- **$d \ge 3$, dense.** No algorithm in time $O(n^{k - \varepsilon})$ for any $\varepsilon > 0$ is known (Lincoln, Vassilevska Williams and Williams, Section 7).
- **The 2026 preprints.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) give faster algorithms for weighted triangle and weighted clique problems in graphs. Their list of refuted hypotheses does not include hyperclique, and they do not claim a faster algorithm for it.

## Bounds

- **Lower bound, unconditional.** A dense instance has $\Theta(n^d)$ possible hyperedges, and an algorithm must read $\Omega(n^d)$ of them in the worst case.
- **Lower bound, conditional on the hyperclique hypothesis.** For $k > d \ge 3$, no $O(n^{k - \varepsilon})$ algorithm.
- **A barrier for algebraic methods.** Lincoln et al. (Section 8) show that the rank and the border rank of the tensor of the generalized matrix product behind hyperclique are maximal. So no method in the style of Strassen, which saves on the [tensor rank](/tensor-rank/), can give a speedup.

## Reductions

- **From Max-$d$-SAT.** Williams (2007) reduced Max-3-SAT to 4-hyperclique in 3-uniform hypergraphs, and Max-$d$-SAT reduces to $k$-hyperclique in $d$-uniform hypergraphs for $k > d$. Split the $n$ variables into $k$ groups and make one vertex for each assignment of a group, so there are $N = 2^{n/k}$ vertices per part. An $O(N^{k - \varepsilon})$ algorithm then solves Max-$d$-SAT in time $O(2^{(1 - \varepsilon/k) n})$ up to polynomial factors. See [Max-SAT](/max-sat/).
- **From $d = 2$.** For [Max-2-SAT](/max-2-sat/), the same construction gives graphs, and fast matrix multiplication gives time $O(2^{\omega n/3})$ up to polynomial factors (Williams 2005). No such method is known for $d \ge 3$, and Lincoln et al. state a Max-$k$-SAT hypothesis next to the hyperclique hypothesis.
- **From constraint problems.** Lincoln et al. (Appendix C) reduce constraint satisfaction problems with constraints given by polynomials of degree $d$ to hyperclique. See [maximum CSP](/maximum-csp/).

## Applications

- **A source of conditional bounds.** It is the source problem of the [hyperclique hypothesis](/hyperclique-hypothesis/). Lincoln et al. use it with related hypotheses for bounds on sparse graph problems.
- **A link from polynomial to exponential time.** A polynomial speedup here gives an exponential speedup for Max-3-SAT. This connects fine-grained bounds for polynomial problems with exact algorithms for NP-hard problems.

## References
