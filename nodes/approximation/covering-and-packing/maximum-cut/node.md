---
tag: GGEXNT
kind: problem
slug: maximum-cut
name: Maximum-cut problem
aliases:
- max cut
- MAX-CUT
area: approximation/covering-and-packing
level: core
summary: Split the vertices into two sets to maximize the weight of crossing edges; a random cut, greedy and local search give 1/2, and the SDP of Goemans and Williamson gives 0.878.
prereqs: [np-hard, linearity-of-expectation]
see_also: [semidefinite-programming, max-cut-ugc-hardness, dense-max-cut-ptas, local-search, method-of-conditional-expectations, max-2-sat, ising-model, quartet-max-cut]
sources:
  - book: isbn:9780521195270
    title: David P. Williamson and David B. Shmoys, The Design of Approximation Algorithms
    locator: Section 5.1 (the random cut) and Section 6.2 (the semidefinite programming algorithm)
  - book: isbn:9780321295354
    title: Jon Kleinberg and Éva Tardos, Algorithm Design
    locator: Chapter 12, Section 12.4 (local search for maximum cut)
  - book: isbn:9780716710455
    title: Michael R. Garey and David S. Johnson, Computers and Intractability
    locator: Appendix A2, problem ND16 (max cut)
  - paper: doi:10.1145/321958.321975
    title: Sartaj Sahni and Teofilo Gonzalez, P-complete approximation problems, Journal of the ACM 23(3), 1976
    locator: pages 555 to 565
  - paper: doi:10.1145/227683.227684
    title: Michel X. Goemans and David P. Williamson, Improved approximation algorithms for maximum cut and satisfiability problems using semidefinite programming, Journal of the ACM 42(6), 1995
    locator: pages 1115 to 1145
  - paper: doi:10.1145/502090.502098
    title: Johan Håstad, Some optimal inapproximability results, Journal of the ACM 48(4), 2001
    locator: pages 798 to 859
  - paper: doi:10.1137/S0097539705447372
    title: Subhash Khot, Guy Kindler, Elchanan Mossel and Ryan O'Donnell, Optimal inapproximability results for MAX-CUT and other 2-variable CSPs?, SIAM Journal on Computing 37(1), 2007
    locator: pages 319 to 357
---

The maximum-cut problem asks for a partition of the vertices of a graph into two sides that maximizes the total weight of the edges between the sides. It is NP-hard, one of [Karp's 21 NP-complete problems](/karps-21-np-complete-problems/), while the minimum cut is solved in polynomial time by flows. Three simple methods each give ratio $1/2$, and this page proves all three: a uniformly random cut, the greedy placement of the vertices one at a time, and [local search](/local-search/) that moves single vertices. For about twenty years no constant ratio above $1/2$ was known, until Goemans and Williamson (1995) gave ratio $\alpha_{GW} \approx 0.878$ by rounding a [semidefinite program](/semidefinite-programming/). Under the [Unique Games Conjecture](/unique-games-conjecture/), $\alpha_{GW}$ is the best possible ratio.

## In plain words

You have a network of points and links, and each link has a value. You must put each point in one of two groups. A link scores its value if its two ends are in different groups. You want the highest score.

Toss a coin for each point. Each link then has an even chance to score, so on average you get half of all the value. Since the best score is at most all the value, this gives at least half the best score. You can also get half without luck: place the points one by one, each in the group opposite to most of its placed links. Or start anywhere and move single points while a move helps. Doing much better than half needs stronger tools.

## Definition

**Input.** An undirected graph $G = (V, E)$ with $n$ vertices and $m$ edges, and a weight $w_e \ge 0$ for each edge. Unit weights give the unweighted problem. Let $W = \sum_{e \in E} w_e$.

**Output.** A set $S \subseteq V$. The *cut* $\delta(S)$ is the set of edges with exactly one endpoint in $S$.

**Goal.** Maximize $w(\delta(S)) = \sum_{e \in \delta(S)} w_e$. OPT is the largest cut weight. This is a maximization problem, so an $\alpha$-approximation returns ALG $\ge \alpha \cdot$ OPT, with $\alpha \le 1$.

**Quadratic form.** With $x_v \in \{-1, +1\}$ for the side of $v$,

$$\text{OPT} = \max_{x \in \{-1, 1\}^V} \sum_{\{u, v\} \in E} w_{uv} \frac{1 - x_u x_v}{2}.$$

Replacing each $x_v$ by a unit vector in $\mathbb{R}^n$ gives the semidefinite relaxation of Goemans and Williamson.

**The trivial upper bound.** Each cut has weight at most $W$, so OPT $\le W$. The three algorithms below compare their cut with $W$, not with OPT.

## Variants

- **Weighted with signs.** If weights may be negative, OPT can be 0 or close to it and multiplicative ratios break; the problem is then studied as an Ising ground state.
- **Max $k$-cut.** Split into $k$ parts. A random part for each vertex gives $1 - 1/k$, and an SDP improves it (Frieze and Jerrum 1997).
- **Max bisection.** Both sides must have $n/2$ vertices. The random balanced cut still gives $1/2$, and SDP methods give more than 0.85.
- **Max directed cut.** Count the arcs from $S$ to $V \setminus S$. A random cut gives $1/4$, and SDP gives about 0.874 (Lewin, Livnat and Zwick 2002).
- **Dense graphs.** If $m \ge \varepsilon n^2$, a PTAS exists; see [dense max cut](/dense-max-cut-ptas/).
- **Quartet max cut.** A variant from phylogenetics, where the constraints are on four vertices; see [quartet max cut](/quartet-max-cut/).

## Examples

**A small graph.** Let $G$ have the vertices 0 to 6 and the edges 0-1, 0-2, 1-2, 1-3, 2-3, 3-4, 4-5, 4-6 and 5-6, all of weight 1, so $W = 9$. The triangles $\{0, 1, 2\}$ and $\{4, 5, 6\}$ share no edge, and each cut misses at least one edge of each triangle, so OPT $\le 7$. The side $S = \{0, 3, 5, 6\}$ cuts 7 edges, so OPT $= 7$.

- *Greedy.* Place the vertices in the order 0 to 6, each on the side with fewer placed neighbours, with ties to side $A$. Then 0, 2, 3, 5 and 6 go to $A$, and 1 and 4 go to $B$. The cut has 6 edges.
- *Local search from this cut.* Vertex 2 is in $A$ with the neighbours 0 and 3 in $A$ and 1 in $B$. Moving it to $B$ adds 2 cut edges and removes 1, so the cut grows to 7. Now no single move helps, and the cut is optimal.

**A bad local optimum.** On the 4-cycle 1-2-3-4-1, the cut $S = \{1, 2\}$ cuts the edges 2-3 and 4-1. Each vertex has one neighbour on each side, so no move gains, and the cut is a local optimum of weight 2. OPT $= 4$, with $S = \{1, 3\}$. So the ratio $1/2$ of local search is tight.

**Standard graphs.**

| graph | $m$ | OPT |
|---|---|---|
| complete graph $K_n$ | $n(n - 1)/2$ | $\lfloor n/2 \rfloor \lceil n/2 \rceil$ |
| $K_2, K_3, K_4, K_5, K_6$ | 1, 3, 6, 10, 15 | 1, 2, 4, 6, 9 |
| cycle $C_n$ | $n$ | $n$ if $n$ is even, $n - 1$ if $n$ is odd |
| bipartite graph | $m$ | $m$ |
| Petersen graph | 15 | 12 |

A graph is bipartite exactly when OPT $= m$. For $K_n$, OPT/$m$ tends to $1/2$, so no algorithm can promise more than about $W/2$ in terms of $W$ alone.

## Known algorithms

| algorithm | ratio | time |
|---|---|---|
| Random cut | $1/2$ in expectation | $O(n + m)$ |
| Greedy placement (Sahni and Gonzalez 1976) | $1/2$ | $O(n + m)$ |
| Local search with single-vertex moves | $1/2$ | $O(mn)$ for unit weights |
| SDP and random hyperplane rounding (Goemans and Williamson 1995) | $\alpha_{GW} \approx 0.87856$ | polynomial |
| Planar graphs, by matching in the dual (Hadlock 1975) | 1 | polynomial |
| Dense graphs, [PTAS](/dense-max-cut-ptas/) | $1 - \varepsilon$ | polynomial for fixed $\varepsilon$ |

**Proof that the random cut gives $1/2$.** Put each vertex in $S$ with probability $1/2$, independently. An edge $\{u, v\}$ is cut exactly when $u$ and $v$ get different sides, which has probability $1/2$. By [linearity of expectation](/linearity-of-expectation/), $\mathbb{E}[w(\delta(S))] = \sum_e w_e / 2 = W/2 \ge \text{OPT}/2$. Pairwise independence of the choices is enough, so a [pairwise independent](/pairwise-independence/) family of $O(n)$ cuts holds one of weight at least $W/2$. $\square$

**Proof that greedy gives $1/2$.** Take the vertices in any order $v_1, \ldots, v_n$. When $v_i$ is placed, let $a$ and $b$ be the total weights of its edges to placed vertices on the two sides. Put $v_i$ on the side with the smaller total, so at least $\max(a, b) \ge (a + b)/2$ of this weight is cut. Each edge belongs to exactly one such step, the step of its later endpoint, and its side is not changed later. Summing over all steps gives a cut of weight at least $W/2 \ge \text{OPT}/2$. This is the [method of conditional expectations](/method-of-conditional-expectations/) applied to the random cut. $\square$

**Proof that local search gives $1/2$.** Start with any cut and move a single vertex to the other side while this makes the cut heavier. At a cut $S$ where no move helps, let $c(v)$ be the weight of the cut edges at $v$ and $u(v)$ the weight of the uncut edges at $v$. Moving $v$ would change the cut by $u(v) - c(v)$, so $c(v) \ge u(v)$, and $c(v) \ge (c(v) + u(v))/2$. Sum over all $v$. Each cut edge is counted twice on the left, and each edge is counted twice in the sum of $c(v) + u(v)$. So $2 w(\delta(S)) \ge W$, and $w(\delta(S)) \ge W/2 \ge \text{OPT}/2$. With unit weights, each move gains at least 1 and the cut is at most $m$, so at most $m$ moves happen. $\square$

With general weights, the number of moves can be exponential, and finding a local optimum is PLS-complete (Schäffer and Yannakakis 1991). Allowing only moves that gain a factor $1 + \varepsilon/n$ gives ratio $1/(2 + \varepsilon)$ in polynomial time (Kleinberg and Tardos, Section 12.4).

## Bounds

- **NP-hardness.** The weighted decision problem is NP-complete (Karp 1972), and so is the unweighted one (Garey, Johnson and Stockmeyer 1976).
- **Upper bounds (proved above).** Ratio $1/2$ for the random cut, greedy and local search. The bound $W/2$ is tight in terms of $W$: OPT/$W$ tends to $1/2$ on $K_n$. The 4-cycle above shows that local search can stop at OPT/2.
- **The SDP bound (cited, not proved here).** Goemans and Williamson (1995) solve the vector relaxation and cut with a random hyperplane. An edge at angle $\theta$ is cut with probability $\theta/\pi$, and $\theta/\pi \ge \alpha_{GW} (1 - \cos\theta)/2$ with $\alpha_{GW} = \min_{0 < \theta \le \pi} \frac{2\theta}{\pi(1 - \cos\theta)} \approx 0.87856$. The integrality gap of the SDP is also $\alpha_{GW}$ (Feige and Schechtman 2002).
- **NP-hardness of approximation (cited).** A $(16/17 + \varepsilon)$-approximation is NP-hard, about 0.941 (Håstad 2001, with a gadget of Trevisan, Sorkin, Sudan and Williamson 2000). The problem is APX-complete (Papadimitriou and Yannakakis 1991).
- **Under the Unique Games Conjecture (cited).** A ratio of $\alpha_{GW} + \varepsilon$ is NP-hard for each $\varepsilon > 0$ (Khot, Kindler, Mossel and O'Donnell 2007, with the Majority Is Stablest theorem of Mossel, O'Donnell and Oleszkiewicz). See [max cut UGC hardness](/max-cut-ugc-hardness/).
- **Linear programs (cited).** Each LP relaxation of polynomial size has integrality gap close to 2, so LPs cannot beat $1/2$ by much (Chan, Lee, Raghavendra and Steurer 2016).
- **Lower bound on OPT.** Each connected graph has OPT $\ge m/2 + (n - 1)/4$, and each graph has OPT $\ge m/2 + (\sqrt{8m + 1} - 1)/8$ (Edwards 1973 and 1975). The second bound is exact for $K_n$ with $n$ odd: for $K_5$, it gives $5 + 1 = 6$.

## Reductions

- **From NAE-3SAT.** The standard NP-completeness proof (Garey and Johnson) maps not-all-equal 3-SAT to max cut.
- **To and from MAX 2-LIN mod 2.** A cut is an assignment $x_v \in \{0, 1\}$, and the edge $\{u, v\}$ is cut exactly when $x_u + x_v \equiv 1 \pmod 2$. So max cut is the problem of satisfying the most equations of the form $x_u + x_v = 1$, a 2-variable CSP like [MAX 2-SAT](/max-2-sat/).
- **Minimum cut is easy.** The minimization version, with nonnegative weights, is solved by [Stoer-Wagner](/stoer-wagner/) or [Karger's algorithm](/karger-min-cut/). The sign of the objective changes the complexity.
- **Ising model.** For an antiferromagnetic [Ising model](/ising-model/) with couplings $J_{uv} \ge 0$, the ground state minimizes $\sum J_{uv} x_u x_v$, which is the same as maximizing the cut with weights $J_{uv}$.
- **Planar graphs.** A cut of a planar graph is a set of edges whose dual edges form an even subgraph. So max cut becomes a maximum-weight even subgraph problem in the dual, solved by matching.

## Applications

- **Statistical physics.** Ground states of spin glasses are max cut problems, and Barahona and others solved large instances by branch and cut.
- **VLSI layout.** Assigning wire segments to two layers to reduce the number of vias is a max cut problem on planar graphs.
- **Clustering.** Splitting items so that dissimilar pairs fall on different sides is max cut on the dissimilarity weights; see also [correlation clustering](/correlation-clustering/).
- **Testing quantum and analog solvers.** Max cut is a standard benchmark for quantum annealers and for the QAOA algorithm.

## References
