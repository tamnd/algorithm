---
tag: P4RD5K
kind: concept
slug: zero-k-clique-hypothesis
name: Zero-k-clique hypothesis
aliases:
- zero-weight k-clique hypothesis
area: complexity/fine-grained-complexity
level: research
summary: "The hypothesis that finding a k-clique of total edge weight 0 needs n^(k-o(1)) time. An October 2026 preprint refutes it for polynomial weights, with O(n^(k-0.0017 floor(k/3)))."
prereqs: [clique, negative-triangle, conditional-lower-bound]
see_also: [min-weight-k-clique-hypothesis, 3sum-conjecture, apsp-conjecture, k-sum, negative-triangle, hyperclique-hypothesis, parameterized-clique, fine-grained-reduction]
sources:
  - paper: doi:10.1137/1.9781611975031.80
    title: "Andrea Lincoln, Virginia Vassilevska Williams and R. Ryan Williams, Tight hardness for shortest cycles and paths in sparse graphs, SODA 2018, 1236-1252 (arXiv:1712.08147)"
    locator: Hypothesis 2.1 of the arXiv version (Exact Weight k-Clique, weights in [-n^(ck), n^(ck)]) and the remark on unweighted k-clique in O(n^(omega k/3)) time
  - paper: doi:10.1007/978-3-642-39206-1_1
    title: "Amir Abboud and Kevin Lewi, Exact weight subgraphs and the k-SUM conjecture, ICALP 2013, LNCS 7965, 1-12"
    locator: the exact weight subgraph problems and their relation to k-SUM
  - paper: doi:10.1137/09076619X
    title: "Virginia Vassilevska Williams and R. Ryan Williams, Finding, minimizing, and counting weighted subgraphs, SIAM Journal on Computing 42(3), 2013, 831-854 (conference version in STOC 2009)"
    locator: the reductions from 3SUM and from APSP to exact triangle (zero-weight triangle)
  - paper: arxiv:2610.06783
    title: "Josh Alman and Virginia Vassilevska Williams, Truly subquadratic 3SUM and truly subcubic APSP via triangles in sparse lopsided graphs, arXiv preprint, October 2026"
    locator: "Theorem 19 (Exact Triangle in deterministic O(n^(3-0.0017)) time), Section 5.3 and Corollary 39 (zero-weight k-clique in O(n^(k-0.0017 floor(k/3))) time; the hypotheses of [AL13, LVW18, BDT16] are refuted, also on general graphs), the section on methodology (the work began from cryptographic constructions based on average-case Zero-k-Clique [LLV19, AHY25]) and the section on the Lean certification; not yet refereed"
---

The zero-k-clique hypothesis says that, for a constant $k \ge 3$, finding $k$ vertices of an edge-weighted graph that are pairwise adjacent and whose $\binom{k}{2}$ edge weights sum to exactly 0 needs time $n^{k - o(1)}$. The weights are integers in a range polynomial in $n$. For $k = 3$ it is the exact triangle problem, which is hard under both the 3SUM conjecture and the APSP conjecture. So the hypothesis was a common base for both.

In October 2026, preprints refuted the 3SUM conjecture and the APSP conjecture. One of them, by Alman and Vassilevska Williams, also refutes the zero-k-clique hypothesis for every $k \ge 3$: their algorithm runs in deterministic time $O(n^{k - 0.0017 \lfloor k/3 \rfloor})$. The preprint is not yet refereed. The hypothesis for unweighted graphs is a different statement and still stands.

## In plain words

Every pair of points in a group is joined by a line, and each line carries a whole number, positive or negative. The task is to find a fixed number of points, all joined to each other, whose lines add up to exactly zero.

Checking every possible group takes time that grows with the group size as a power of the number of points. The hypothesis was a bet that no method does much better.

The bet was useful because many other questions, such as finding three numbers that add up to zero, can be turned into this one. In 2026, a new method did a little better than checking every group, so the bet is lost.

## The idea

### Hypothesis (zero-weight k-clique)

For a constant $k \ge 3$, there is a constant $c$ such that no algorithm finds a $k$-clique of total weight 0 in an $n$-vertex graph with integer edge weights in $[-n^{ck}, n^{ck}]$ in time $O(n^{k - \varepsilon})$ for any $\varepsilon > 0$ (Lincoln, Vassilevska Williams and Williams, SODA 2018, Exact Weight $k$-Clique Hypothesis; earlier forms by Abboud and Lewi, ICALP 2013).

- The model is the [word RAM](/word-ram/) with words of $\Theta(\log n)$ bits, so each weight fits in $O(1)$ words.
- The numbers are integers bounded in absolute value by a polynomial in $n$. Without a bound, the problem changes.
- The graph is dense: it may be the complete graph, and the input has $\Theta(n^2)$ weights.
- Lincoln et al. do not single out randomized algorithms. The refuting algorithm is deterministic, so this choice does not matter for the refutation.

The usual instance is complete $k$-partite with $n$ vertices per part, and a clique takes one vertex from each part. A general graph reduces to this form with $k$ copies of the vertex set.

### Why it mattered

- **3SUM and APSP meet here.** Vassilevska Williams and Williams (SICOMP 2013) reduce 3SUM to exact triangle and reduce the min-plus product, and so APSP, to exact triangle. So an $O(n^{3-\varepsilon})$ algorithm for exact triangle would refute both conjectures. The zero-3-clique hypothesis was weaker than each of them, and so a safer base.
- **k-SUM.** Abboud and Lewi (2013) relate exact weight subgraph problems to the [k-SUM](/k-sum/) conjecture.
- **Brute force is the best known.** Before 2026, no algorithm beat $n^k$ by a polynomial factor for any $k \ge 3$ with polynomial weights.

### Status in 2026

- **The hypothesis: refuted, if the preprint is correct.** Alman and Vassilevska Williams (arXiv:2610.06783, not yet refereed) solve exact triangle in deterministic time $O(n^{3 - 0.0017})$ (Theorem 19). By the classic reduction of Nešetřil and Poljak, Corollary 39 solves zero-weight $k$-clique on complete $k$-partite graphs with weights of absolute value at most $n^{\nu}$ in deterministic time $O(n^{k - 0.0017 \lfloor k/3 \rfloor})$, for every constant $k \ge 3$ and $\nu \ge 1$. They state that the Zero-Weight, Min-Weight and Max-Weight $k$-Clique hypotheses with polynomially bounded weights are refuted, also on general graphs.
- **The reduction.** Put $\lfloor k/3 \rfloor$ of the $k$ parts into each of three groups. A vertex of the new graph is a choice of one vertex in each part of its group, so there are $N = n^{\lfloor k/3 \rfloor}$ vertices per new part. When 3 does not divide $k$, fix the $t = k - 3\lfloor k/3 \rfloor$ remaining vertices in all $n^t$ ways. Each edge of a $k$-clique is counted on exactly one edge of the triangle. So the time is $n^t \cdot N^{3 - 0.0017}$.
- **Formal proof.** The authors report that, after the paper was written, Anthropic used an internal research model to certify the main results and the zero-weight case of Corollary 39 in the Lean 4 proof assistant.
- **How it was found.** The authors write that the work began when an Anthropic employee used an internal research model on cryptographic constructions based on average-case zero-$k$-clique (LaVigne, Lincoln and Vassilevska Williams 2019; Alman, Huang and Yeo 2025). Claude developed the algorithm, first for the average case and then for the worst case.
- **What still stands.** Unweighted $k$-clique is not affected: it takes time $O(n^{\omega k/3})$ for $k$ divisible by 3 (Nešetřil and Poljak 1985), and no faster algorithm is claimed. The [hyperclique hypothesis](/hyperclique-hypothesis/), SETH and the combinatorial forms are also not affected. The saving is only $0.0017 \lfloor k/3 \rfloor$, so a lower bound of the form $n^{k - c}$ for a larger constant $c$ is still open.

### Pitfalls

- The weight range is part of the hypothesis. The refutation is for weights bounded by a polynomial in $n$. With weights of $n^{k}$ bits, or real weights, the question is different.
- The exponent saving grows only with $\lfloor k/3 \rfloor$. For $k = 4$ and $k = 5$ it is the same as for $k = 3$.
- Exact weight is not the same as minimum weight. For triangles, minimum weight reduces to exact weight (Vassilevska Williams and Williams 2013), but no reduction in the other direction is known. See [min-weight k-clique hypothesis](/min-weight-k-clique-hypothesis/).

## Examples

**A small instance.** Take $K_5$ on $0, \ldots, 4$ with the weights $w(0,1) = 3$, $w(0,2) = -1$, $w(0,3) = 4$, $w(0,4) = -5$, $w(1,2) = 2$, $w(1,3) = -2$, $w(1,4) = 6$, $w(2,3) = -3$, $w(2,4) = 1$ and $w(3,4) = -4$. Of the 10 triangles, two have weight 0: $\{0, 2, 3\}$ with $-1 + 4 - 3$ and $\{1, 3, 4\}$ with $-2 + 6 - 4$. Of the five 4-cliques, one has weight 0: $\{1, 2, 3, 4\}$, with $2 - 2 + 6 - 3 + 1 - 4 = 0$.

**The exponents.** With $\varepsilon_T = 0.0017$, Corollary 39 gives these times:

| $k$ | groups $\lfloor k/3 \rfloor$ | fixed vertices $t$ | time |
|---|---|---|---|
| 3 | 1 | 0 | $O(n^{2.9983})$ |
| 4 | 1 | 1 | $O(n^{3.9983})$ |
| 5 | 1 | 2 | $O(n^{4.9983})$ |
| 6 | 2 | 0 | $O(n^{5.9966})$ |
| 9 | 3 | 0 | $O(n^{8.9949})$ |

For $k = 6$, each new part has $N = n^2$ vertices, and $N^{2.9983} = n^{5.9966}$. For comparison, unweighted 6-clique takes time $O(n^{2\omega}) = O(n^{4.743104})$ with $\omega < 2.371552$.

## Where it is used

- **Weighted subgraph problems.** Bounds for exact weight subgraphs and related problems (Abboud and Lewi 2013). These bounds are lost if the preprint is correct.
- **Fine-grained cryptography.** LaVigne, Lincoln and Vassilevska Williams (CRYPTO 2019) build public-key schemes on the average-case hardness of zero-$k$-clique. The new algorithm also works on average-case instances, so the $n^{k - o(1)}$ assumption behind such schemes no longer holds, if the preprint is correct.
- **Problems with 3SUM-hardness and APSP-hardness at once.** Exact triangle was the common base. See [negative triangle](/negative-triangle/) for the APSP side and [3SUM conjecture](/3sum-conjecture/) for the 3SUM side.

## References
