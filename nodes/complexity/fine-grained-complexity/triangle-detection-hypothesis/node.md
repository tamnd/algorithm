---
tag: BJ3GKM
kind: concept
slug: triangle-detection-hypothesis
name: Triangle detection hypothesis
aliases:
- triangle hypothesis
area: complexity/fine-grained-complexity
level: research
summary: "The hypothesis that triangle detection in m-edge graphs needs m^(4/3-o(1)) time, a form that still holds if omega = 2. The 2026 preprints do not affect it."
prereqs: [triangle-counting, matrix-multiplication-exponent, conditional-lower-bound]
see_also: [combinatorial-bmm-conjecture, negative-triangle, triangle-listing-by-degree, triangle-finding, omv-conjecture, dynamic-lower-bounds, zero-k-clique-hypothesis, boolean-matrix-multiplication]
sources:
  - paper: doi:10.1137/0207033
    title: "Alon Itai and Michael Rodeh, Finding a minimum circuit in a graph, SIAM Journal on Computing 7(4), 1978, 413-423"
    locator: the triangle algorithms in O(n^omega) time with matrix multiplication and in O(m^(3/2)) time
  - paper: doi:10.1007/BF02523189
    title: "Noga Alon, Raphael Yuster and Uri Zwick, Finding and counting given length cycles, Algorithmica 17(3), 1997, 209-223"
    locator: the triangle algorithm in O(m^(2 omega/(omega+1))) time
  - paper: doi:10.1109/FOCS.2014.53
    title: "Amir Abboud and Virginia Vassilevska Williams, Popular conjectures imply strong lower bounds for dynamic problems, FOCS 2014, 434-443"
    locator: Conjecture 4 (No almost linear time triangle) and the remark that there may be no O(m^(4/3)) algorithm
  - paper: doi:10.1145/3519935.3520066
    title: "Amir Abboud, Karl Bringmann, Seri Khoury and Or Zamir, Hardness of approximation in P via short cycle removal: cycle detection, distance oracles, and beyond, STOC 2022, 1487-1500 (arXiv:2204.10465)"
    locator: Section 7 of the arXiv version, Conjecture 7.1 (the m^(4/3-o(1)) form, which holds even if omega = 2) and Observation 7.2 (the equivalent n^(2-o(1)) form for average degree Theta(sqrt(n)))
  - paper: doi:10.1145/3186893
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Subcubic equivalences between path, matrix, and triangle problems, Journal of the ACM 65(5), 2018, article 27 (conference version in FOCS 2010, 645-654)"
    locator: the subcubic equivalence of triangle detection and Boolean matrix multiplication for combinatorial algorithms
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: "the paragraph Other parameter regimes in the introduction (the technique needs a middle part of at most n^0.12 vertices; balanced sparse instances give bounds of m^(4/3-o(1))); not yet refereed"
---

The triangle detection hypothesis says that deciding whether a graph with $m$ edges has a triangle needs more than linear time. Its usual form, stated by Abboud, Bringmann, Khoury and Zamir in 2022, is the bound $m^{4/3 - o(1)}$. This form still holds if the matrix multiplication exponent is $\omega = 2$, because the best algorithm, by Alon, Yuster and Zwick, then runs in time $m^{4/3 + o(1)}$. Weaker and stronger forms are also in use, so a bound "from the triangle hypothesis" must say which form it uses.

In October 2026, preprints refuted the 3SUM conjecture, the APSP conjecture, and the zero-weight and min-weight k-clique hypotheses. These are about weighted triangles. The triangle detection hypothesis is about unweighted graphs, and the preprints do not affect it.

## In plain words

A triangle is three people who all know each other. Given a list of who knows whom, is there such a group?

For a crowded list, fast matrix methods do much better than checking every group of three. For a short list, the best known methods take somewhat more than the length of the list times its cube root.

The hypothesis is a bet that this cannot be pushed down to about the length of the list. The common form of the bet stays fair even if matrix methods get as fast as they possibly can.

## The idea

### Hypothesis (triangle detection)

There are several forms. In each, the model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, the graph is unweighted and given by adjacency lists, and the bound is on the expected time, so randomized algorithms are excluded too.

- **The $m^{4/3}$ form.** For some density $m = \Theta(n^{\alpha})$, no algorithm detects a triangle in an $m$-edge graph in time $O(m^{4/3 - \varepsilon})$ for any $\varepsilon > 0$ (Abboud, Bringmann, Khoury and Zamir, Conjecture 7.1, who credit it to Abboud and Vassilevska Williams 2014). By their Observation 7.2, it is equivalent to the bound $n^{2 - o(1)}$ for graphs with $n$ vertices and average degree $\Theta(\sqrt{n})$, that is, $m = \Theta(n^{3/2})$.
- **The weak form.** There is a constant $\delta > 0$ such that triangle detection needs time $m^{1 + \delta - o(1)}$ (Abboud and Vassilevska Williams, FOCS 2014, Conjecture 4).
- **The strong form.** Triangle detection needs time $m^{2\omega/(\omega+1) - o(1)}$, so the algorithm of Alon, Yuster and Zwick is optimal for the true value of $\omega$. Abboud, Bringmann, Khoury and Zamir note that Abboud and Vassilevska Williams also considered this form.
- **The dense combinatorial form.** No combinatorial algorithm detects a triangle in an $n$-vertex graph in time $O(n^{3 - \varepsilon})$. This is equivalent to the [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/) (Vassilevska Williams and Williams 2010).

The strong form implies the $m^{4/3}$ form, because $2\omega/(\omega+1) \ge 4/3$ for $\omega \ge 2$, and the $m^{4/3}$ form implies the weak form.

### The algorithms behind it

All of these bounds are unconditional.

- **Dense graphs.** A graph with adjacency matrix $A$ has a triangle if and only if some edge $(i, k)$ has $(A^2)[i,k] > 0$. So triangle detection takes time $O(n^{\omega})$ (Itai and Rodeh 1978). With $\omega < 2.371552$ this is $O(n^{2.371552})$.
- **Sparse graphs.** Listing all triangles takes time $O(m^{3/2})$ (Itai and Rodeh 1978); see [triangle listing by degree](/triangle-listing-by-degree/).
- **Both.** Alon, Yuster and Zwick (1997) split the vertices at degree $\Delta = m^{(\omega-1)/(\omega+1)}$: they check the triangles through a low-degree vertex one by one and use matrix multiplication on the high-degree vertices. This takes time $O(m^{2\omega/(\omega+1)})$. With $\omega < 2.371552$ the exponent is $2\omega/(\omega+1) < 1.40680$. With $\omega = 2$ it would be $4/3$.

So the $m^{4/3}$ form says: even if matrix multiplication takes time $n^{2+o(1)}$, the method of Alon, Yuster and Zwick cannot be beaten by a polynomial factor at every density.

### Status in 2026

- **The hypothesis: open, in every form.** The preprints of Alman and Vassilevska Williams (arXiv:2610.06783) and of Chan, Itakura, Ma and Yu (arXiv:2610.42012), both not yet refereed, give faster algorithms for weighted triangle problems. They do not give a faster algorithm for unweighted triangle detection.
- **Why the methods differ.** Alman and Vassilevska Williams solve All-Edges Sparse Triangle faster only when the middle part of the tripartite graph has at most $n^{0.12}$ vertices. They note that most known reductions produce balanced instances, with parts of about equal size, and give bounds of $m^{4/3 - o(1)}$; their technique does not reach that case.
- **What else stands.** The [combinatorial BMM conjecture](/combinatorial-bmm-conjecture/), SETH and the plain OMv conjecture also stand. A bound that was proved from 3SUM through a triangle problem does not move to this hypothesis by itself: it needs a new reduction from unweighted triangle detection.

### Pitfalls

- The forms differ. A bound proved from the weak form holds for some $\delta$, not for $\delta = 1/3$. A bound proved from the strong form fails if $\omega$ turns out smaller than the value used.
- The size measure matters. A bound in $m$ is not a bound in $n$: the $m^{4/3}$ form is about sparse graphs, and for dense graphs the time $n^{\omega}$ is already below $m^{4/3} = n^{8/3}$.
- The dense combinatorial form is only about combinatorial algorithms. For general algorithms, dense triangle detection is truly subcubic.

## Examples

**Detection with a matrix product.** Take the 5-cycle $0, 1, 2, 3, 4$ with the chord $\{0, 2\}$, so $n = 5$ and $m = 6$. The square of the adjacency matrix is

$$A^2 = \begin{pmatrix} 3&1&1&2&0 \\ 1&2&1&1&1 \\ 1&1&3&0&2 \\ 2&1&0&2&0 \\ 0&1&2&0&2 \end{pmatrix}.$$

The edges $\{0,1\}$, $\{0,2\}$ and $\{1,2\}$ have $(A^2)[i,k] = 1$, so each lies on a triangle. The trace of $A^3$ is 6, and $6 / 6 = 1$ triangle, $\{0, 1, 2\}$. Without the chord, the trace is 0 and there is no triangle.

**The degree threshold.** For this graph, $\Delta = 6^{(\omega-1)/(\omega+1)}$ is about $2.07$ with $\omega = 2.371552$. The vertices 0 and 2 have degree 3 and are heavy; the others have degree 2 and are light.

**The exponents.** With $m = n^{3/2}$, the regime of Observation 7.2, the bound $m^{4/3}$ is $n^2$, the method of Alon, Yuster and Zwick takes $n^{1.5 \times 1.40680} = n^{2.11020}$, and listing takes $n^{2.25}$. For $m = n^2$, the time $n^{\omega} = n^{2.371552}$ is best.

## Where it is used

- **[Dynamic lower bounds](/dynamic-lower-bounds/).** Abboud and Vassilevska Williams prove bounds for Pagh's problem and other dynamic problems from the weak form. Many of them were later proved from the [OMv conjecture](/omv-conjecture/).
- **Hardness of approximation in P.** Abboud, Bringmann, Khoury and Zamir use the $m^{4/3}$ form to prove bounds for approximate short cycle detection and for distance oracles.
- **Triangle counting and listing.** Bounds for listing all triangles in sparse graphs, since listing also detects. See [triangle counting](/triangle-counting/).
- **Quantum algorithms.** In the query model, finding a triangle is a separate question with its own bounds; see [triangle finding](/triangle-finding/).

## References
