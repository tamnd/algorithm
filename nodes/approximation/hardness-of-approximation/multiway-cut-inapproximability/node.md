---
tag: 4GNDEM
kind: theorem
slug: multiway-cut-inapproximability
name: Multiway cut inapproximability
aliases:
- Freund-Karloff multiway cut hardness
- APX-hardness of multiway cut
- UGC hardness of multiway cut
- node multiway cut is as hard as vertex cover
area: approximation/hardness-of-approximation
level: advanced
summary: Multiway cut is APX-hard for each k ≥ 3. Under the unique games conjecture the CKR integrality gap, which tends to at least 1.2, is the exact threshold. The node version is as hard as vertex cover.
prereqs: [multiway-cut-problem, vertex-cover-inapproximability, unique-games-conjecture, integrality-gap, approximation-preserving-reduction]
see_also: [multicut-problem, parameterized-multiway-cut, max-cut-ugc-hardness, vertex-cover, l-reduction, apx-class, lp-relaxation, isolating-cuts]
sources:
  - paper: doi:10.1137/S0097539792225297
    title: E. Dahlhaus, D. S. Johnson, C. H. Papadimitriou, P. D. Seymour and M. Yannakakis, The complexity of multiterminal cuts, SIAM Journal on Computing 23(4), 1994
    locator: MAX SNP-hardness of edge multiway cut for every fixed k ≥ 3
  - paper: doi:10.1145/1374376.1374379
    title: R. Manokaran, J. Naor, P. Raghavendra and R. Schwartz, SDP gaps and UGC hardness for multiway cut, 0-extension, and metric labeling, STOC 2008
    locator: under the unique games conjecture, no ratio below the integrality gap of the earthmover relaxation, which for multiway cut is the CKR relaxation
  - paper: doi:10.1006/jcss.1999.1687
    title: G. Călinescu, H. Karloff and Y. Rabani, An improved approximation algorithm for multiway cut, Journal of Computer and System Sciences 60(3), 2000
    locator: the simplex relaxation and the ratio 3/2 - 1/k
  - paper: "D. R. Karger, P. Klein, C. Stein, M. Thorup and N. E. Young, Rounding algorithms for a geometric embedding of minimum multiway cut, Mathematics of Operations Research 29(3), 2004"
    locator: the integrality gap of the CKR relaxation is exactly 12/11 for k = 3
  - paper: "A. Freund and H. Karloff, A lower bound of 8/(7 + 1/(k - 1)) on the integrality ratio of the Călinescu-Karloff-Rabani relaxation for multiway cut, Information Processing Letters 75(1-2), 2000"
    locator: the integrality gap is at least 8/(7 + 1/(k - 1))
  - paper: "H. Angelidakis, Y. Makarychev and P. Manurangsi, An improved integrality gap for the Călinescu-Karloff-Rabani relaxation for multiway cut, IPCO 2017"
    locator: the integrality gap is at least 6/(5 + 1/(k - 1))
  - paper: "A. Sharma and J. Vondrák, Multiway cut, pairwise realizable distributions, and descending thresholds, STOC 2014"
    locator: the rounding with ratio 1.2965 for every k
  - paper: "N. Garg, V. V. Vazirani and M. Yannakakis, Multiway cuts in node weighted graphs, Journal of Algorithms 50(1), 2004"
    locator: the 2 - 2/k approximation for node multiway cut
---

Multiway cut inapproximability is a set of results on how well [multiway cut](/multiway-cut-problem/) can be approximated in polynomial time. Dahlhaus, Johnson, Papadimitriou, Seymour and Yannakakis (1994) showed that the edge version is APX-hard for every fixed number $k \ge 3$ of terminals, so it has no PTAS unless P = NP. Manokaran, Naor, Raghavendra and Schwartz (2008) showed that, under the [unique games conjecture](/unique-games-conjecture/), no polynomial algorithm beats the integrality gap of the Călinescu, Karloff and Rabani (CKR) relaxation, a number that is $\frac{12}{11}$ for $k = 3$ and at least about $1.2$ for large $k$. The node version is as hard as [vertex cover](/vertex-cover-inapproximability/), by a short reduction that this page proves in full. The two other results are cited.

## Statement

In **edge multiway cut**, the input is a graph with nonnegative edge weights and terminals $t_1, \ldots, t_k$, and a solution is a set of edges whose removal leaves no path between two terminals. In **node multiway cut**, a solution is a set of non-terminal vertices with this property, and the cost is the total vertex weight. Both are minimization problems, and a ratio $\rho \ge 1$ means a cost of at most $\rho \cdot \mathrm{OPT}$ on every instance. Let $\alpha_k$ be the integrality gap of the CKR relaxation with $k$ terminals: the supremum, over instances, of the ratio of $\mathrm{OPT}$ to the optimum of the relaxation.

**Theorem 1 (Dahlhaus et al. 1994).** For each fixed $k \ge 3$, edge multiway cut with unit weights is MAX SNP-hard. So there is a constant $\delta_k > 0$ such that a polynomial algorithm with ratio $1 + \delta_k$ gives P = NP.

**Theorem 2 (node version).** There is a polynomial reduction that maps a graph $G$ on $n$ vertices to a node multiway cut instance $H$ with unit weights, $2n$ vertices and $n$ terminals, such that the cuts of $H$ are exactly the vertex covers of $G$. So a ratio $\rho$ for node multiway cut gives a ratio $\rho$ for vertex cover. In particular, no ratio below $\sqrt2$ is possible unless P = NP, and none below 2 under the unique games conjecture.

**Theorem 3 (Manokaran, Naor, Raghavendra and Schwartz 2008).** Assume the unique games conjecture. For each fixed $k \ge 3$ and $\varepsilon > 0$, a polynomial algorithm for edge multiway cut with ratio $\alpha_k - \varepsilon$ gives P = NP. The known bounds are $\alpha_3 = \frac{12}{11}$ and
$$\frac{6}{5 + \frac{1}{k - 1}} \le \alpha_k \le 1.2965.$$

So the bound $1.2 - \varepsilon$ for large $k$ is known only under the unique games conjecture. Without it, only the small constant of Theorem 1 is known.

## In plain words

You must cut a network so that some special points can no longer reach each other, at the least cost. With three or more special points this is hard to do well. Even a fast method that only promises to come within a tiny fixed percentage of the best cut would show that P equals NP.

A stronger guess, the unique games conjecture, gives an exact answer. There is a standard way to relax the problem into a continuous one, and the relaxed answer can be below the true best by some factor. Under the conjecture, no fast method can do better than that factor, which is about 1.2 when there are many special points.

If you must cut vertices instead of lines, the problem is as hard as covering every line of a graph with few vertices.

## Proof

*Theorem 2.* Let $G = (V, E)$ with $V = \{0, \ldots, n - 1\}$. Form $H$ from $G$ by adding a new terminal $t_v$ for each vertex $v$ and the edge $v t_v$. Every non-terminal has weight 1, and terminals cannot be removed. No two terminals are adjacent, so a cut exists. Let $S \subseteq V$.

- If $S$ is not a vertex cover, some edge $uv$ of $G$ has $u, v \notin S$. Then $t_u, u, v, t_v$ is a path in $H - S$, so $S$ is not a cut.
- If $S$ is a vertex cover, then $V \setminus S$ is an independent set of $G$. A vertex $v \notin S$ has, in $H - S$, only the neighbour $t_v$, because each of its neighbours in $G$ is in $S$. So the components of $H - S$ are the pairs $\{v, t_v\}$ for $v \notin S$ and the single terminals $t_v$ for $v \in S$. Each component has one terminal, so $S$ is a cut.

So the cuts of $H$ are the vertex covers of $G$, with the same cost, and $\mathrm{OPT}(H) = \tau(G)$, the vertex cover number. A cut of cost $\rho \cdot \mathrm{OPT}(H)$ is a vertex cover of size $\rho \cdot \tau(G)$. This is an [L-reduction](/l-reduction/) with both constants equal to 1, so the bounds for vertex cover carry over: $\sqrt2 - \varepsilon$ from Khot, Minzer and Safra, and $2 - \varepsilon$ under the unique games conjecture from Khot and Regev, both on the [vertex cover inapproximability](/vertex-cover-inapproximability/) page. The same reduction with vertex weights carries over weighted vertex cover. $\blacksquare$

The number of terminals in $H$ is $n$, so Theorem 2 says nothing about a fixed $k$. For fixed $k$, node multiway cut contains the edge version, because each edge can be subdivided by a new vertex of the same weight, and the original vertices get a very large weight. So Theorem 1 holds for node multiway cut too.

*Theorem 1.* This is cited. Dahlhaus et al. reduce from a MAX SNP-hard cut problem on graphs of bounded degree to multiway cut with three terminals, using gadgets of fixed size, so the reduction is an L-reduction. More terminals are added as isolated vertices. The constant $\delta_k$ is not given explicitly.

*Theorem 3, sketch.* This is a sketch of a long proof.

1. Take an instance on which the CKR relaxation has value $\mathrm{LP}$ and the best cut has cost $\mathrm{OPT} \approx \alpha_k \cdot \mathrm{LP}$.
2. Use it to build a dictatorship test. Each vertex of the gap instance is replaced by a copy of a noisy cube, and a cut of the new instance is read as a function on the cube. Functions that depend on one coordinate give cuts of cost about $\mathrm{LP}$, and functions with no influential coordinate give cuts of cost at least about $\mathrm{OPT}$.
3. Compose the test with a unique games instance in the usual way. If the instance has a labeling that satisfies almost all constraints, the cut costs about $\mathrm{LP}$. If every labeling satisfies only a small fraction, every cut costs about $\mathrm{OPT}$. The ratio of the two is $\alpha_k - \varepsilon$.

The values of $\alpha_k$ come from separate work. Karger, Klein, Stein, Thorup and Young found $\alpha_3 = \frac{12}{11}$ exactly. Freund and Karloff gave instances with gap $\frac{8}{7 + 1/(k - 1)}$, and Angelidakis, Makarychev and Manurangsi improved this to $\frac{6}{5 + 1/(k - 1)}$. Sharma and Vondrák gave a rounding with ratio $1.2965$, which is an upper bound on $\alpha_k$ for every $k$.

### Example

For the 5-cycle with vertices $0, \ldots, 4$, the instance $H$ of Theorem 2 has 10 vertices, the 5 cycle edges and the 5 edges $v t_v$, and 5 terminals. The set $\{0, 2, 3\}$ is a vertex cover of the cycle, and in $H - \{0, 2, 3\}$ the components are $\{1, t_1\}$, $\{4, t_4\}$ and the three single terminals. The set $\{0, 2\}$ is not a cover, because the edge $34$ is not covered, and $t_3, 3, 4, t_4$ is a path in $H - \{0, 2\}$. So $\mathrm{OPT}(H) = \tau(C_5) = 3$. The code for this page checks, on random graphs with up to 7 vertices, that a vertex set is a cut of $H$ exactly when it is a vertex cover of $G$.

## Consequences

- **No PTAS.** For every fixed $k \ge 3$, edge multiway cut has no polynomial-time approximation scheme unless P = NP. For $k = 2$ it is a [minimum cut](/min-cut-problem/) and is solved exactly.
- **$k = 3$ is settled under the conjecture.** The rounding of Karger et al. reaches $\frac{12}{11}$, and Theorem 3 shows that nothing better is possible under the unique games conjecture.
- **One relaxation decides the question.** Under the conjecture, no polynomial algorithm of any kind beats the integrality gap of the CKR relaxation, so stronger relaxations cannot help, and the open problem for large $k$ is to find $\alpha_k$.
- **Node version.** The algorithm of Garg, Vazirani and Yannakakis has ratio $2 - \frac2k$ for node multiway cut. By Theorem 2, a ratio below 2 with $k$ part of the input would refute the unique games conjecture.
- **Parameterized view.** With the size of the cut as the parameter, both versions are fixed-parameter tractable; see [parameterized multiway cut](/parameterized-multiway-cut/).

## Tightness

The simple [isolating cut](/isolating-cuts/) heuristic has ratio $2 - \frac2k$, and the CKR rounding has $\frac32 - \frac1k$. Under the unique games conjecture, Theorem 3 shows that the threshold is at least $\alpha_k$. For $k = 3$ the rounding of Karger et al. reaches $\alpha_3 = \frac{12}{11}$, so the bound is tight there. For large $k$ the best rounding gives $1.2965$, and the open part is the value of $\alpha_k$, between about $1.2$ and $1.2965$. Without the conjecture, the gap between Theorem 1 and the upper bounds is wide, because $\delta_k$ is a small constant. For the node version with $k$ part of the input, Theorem 2 and the $2 - \frac2k$ algorithm match under the conjecture as $k$ grows.

## History

Dahlhaus, Johnson, Papadimitriou, Seymour and Yannakakis proved NP-hardness and MAX SNP-hardness in 1992, with the journal version in 1994. Călinescu, Karloff and Rabani introduced the simplex relaxation in 1998, and Freund and Karloff gave the first gap instances in 2000. Karger, Klein, Stein, Thorup and Young settled $k = 3$ for the relaxation in 1999. Garg, Vazirani and Yannakakis studied the node version in 1994. Manokaran, Naor, Raghavendra and Schwartz proved in 2008 that the integrality gap is the exact threshold under the unique games conjecture. Sharma and Vondrák (2014) and Angelidakis, Makarychev and Manurangsi (2017) narrowed the range of $\alpha_k$.

## References
