---
tag: 7DRJZ2
kind: algorithm
slug: asadpour-atsp-algorithm
name: Asadpour et al. ATSP algorithm
aliases:
- O(log n / log log n) ATSP approximation
- thin-tree ATSP algorithm
area: approximation/tsp-approximation
level: research
summary: Sample max entropy spanning trees from the ATSP LP, keep the cheapest, and complete it to a tour by a min cost circulation. The tour costs O(log n / log log n) OPT with high probability.
solves: [asymmetric-tsp]
model: word-ram
complexity:
  vars: {n: the number of vertices}
  time: {worst: poly(n)}
  space: {extra: poly(n)}
properties: {deterministic: false, recursive: false, online: false}
history:
  year: 2010
  people: [Arash Asadpour, Michel X. Goemans, Aleksander Mądry, Shayan Oveis Gharan, Amin Saberi]
  note: Published at SODA 2010 and in Operations Research in 2017; it was the first ratio for ATSP of order below log n.
prereqs: [asymmetric-tsp, spanning-tree-polytope, matrix-tree-theorem, hoffman-circulation-theorem, chernoff-bound, union-bound]
see_also: [asymmetric-tsp, karlin-klein-oveis-gharan-algorithm, randomized-rounding, dependent-rounding, min-cost-flow-problem, global-min-cut-problem, integrality-gap, uniform-spanning-tree-sampling]
sources:
  - paper: doi:10.1287/opre.2017.1603
    title: Arash Asadpour, Michel X. Goemans, Aleksander Mądry, Shayan Oveis Gharan and Amin Saberi, An O(log n/log log n)-approximation algorithm for the asymmetric traveling salesman problem, Operations Research 65(4), 2017
    locator: pages 1043 to 1061 (Section 4, thin trees and the circulation; Section 6, the thinness of the max entropy tree)
  - title: Arash Asadpour, Michel X. Goemans, Aleksander Mądry, Shayan Oveis Gharan and Amin Saberi, An O(log n/log log n)-approximation algorithm for the asymmetric traveling salesman problem, SODA 2010
    locator: pages 379 to 389 (the conference version)
  - paper: doi:10.1002/net.3230120103
    title: Alan M. Frieze, Giulia Galbiati and Francesco Maffioli, On the worst-case performance of some algorithms for the asymmetric traveling salesman problem, Networks 12(1), 1982
    locator: pages 23 to 39 (the log n ratio that this algorithm improves)
  - paper: doi:10.1145/3188745.3188824
    title: Ola Svensson, Jakub Tarnawski and László A. Végh, A constant-factor approximation algorithm for the asymmetric traveling salesman problem, STOC 2018
    locator: the main theorem (the first constant ratio, by a route other than thin trees)
---

The algorithm of Asadpour, Goemans, Mądry, Oveis Gharan and Saberi is a randomized approximation algorithm for the [asymmetric TSP](/asymmetric-tsp/) with the ratio $O(\log n / \log\log n)$ with high probability. It solves the LP relaxation, forgets the directions, samples random spanning trees whose edge probabilities follow the LP, keeps the cheapest tree, and adds a least cost set of arcs so that each vertex has equal in-degree and out-degree. The key notion is a *thin* tree: a tree that crosses each cut only a few times compared with the LP. The analysis proves that a thin tree gives a cheap tour, and that a max entropy tree is thin with high probability.

## In plain words

The roads are one-way, and a road and its opposite can have different lengths. A round trip must leave each group of cities as often as it enters it.

First solve a relaxed version of the problem, in which a trip can use a road in part. Then forget the directions and pick a random tree that connects all cities, where each road appears with about the chance that the relaxed answer gives it. Pick a few such trees and keep the cheapest. Give each tree road its cheaper direction, then add the cheapest extra roads that make each city have as many roads in as out. Walk all these roads in one trip and skip repeated cities.

The extra roads are cheap when the tree crosses each border between two groups of cities only a few times. A random tree of this kind does that with high probability.

## The problem

The input is a set $V$ of $n \ge 3$ vertices with costs $c(u, v) \ge 0$ on the ordered pairs, which can differ from $c(v, u)$. The costs satisfy the directed triangle inequality $c(u, w) \le c(u, v) + c(v, w)$; for a road network, use the shortest path costs. The output is a directed tour. OPT is the least cost of a tour, ALG the cost of the output, and LP* the value of the ATSP LP below, with $\text{LP}^* \le \text{OPT}$. The ratio $\rho$ means ALG $\le \rho \cdot \text{OPT}$; here it holds with probability at least $1 - O(1/n)$ on each instance. All logarithms are natural.

## The algorithm

```pseudo id=main
ASADPOUR-ATSP(V, c)
L1  x ← an optimal solution of the ATSP LP for (V, c)
L2  z_{uv} ← (1 − 1/n)(x_{uv} + x_{vu}) for each unordered pair {u, v}
L3  λ ← weights on the support of z with Pr_λ[e ∈ T] = z_e for each edge e
L4  T_1, ..., T_k ← k = 2⌈ln n⌉ independent trees with Pr[T] proportional to the product of λ_e over e in T
L5  T ← the cheapest T_i, where the edge {u, v} costs min(c(u, v), c(v, u))
L6  A ← the edges of T, each oriented in its cheaper direction
L7  F ← A plus a least cost multiset of arcs that makes in-degree equal out-degree at each vertex
L8  W ← an Euler circuit of the multigraph F
L9  H ← the vertices of W, each kept only at its first visit
L10 return H
```

The ATSP LP of line L1 is the asymmetric form of the [Held-Karp bound](/held-karp-bound/): $x(\delta^+(v)) = x(\delta^-(v)) = 1$ at each vertex, $x(\delta^+(U)) \ge 1$ for each set $U$, and $x \ge 0$. Line L2 forgets the directions. The sum of the $x_{uv}$ is $n$, so the factor $1 - 1/n$ gives total $n - 1$, and $z$ is a point of the [spanning tree polytope](/spanning-tree-polytope/) of the support graph, in its relative interior.

Lines L3 and L4 sample from the maximum entropy distribution with the marginals $z$, which has the product form $\Pr[T] \propto \prod_{e \in T} \lambda_e$. The weights are the solution of a [convex optimization](/convex-optimization/) problem, $\min_\gamma \log \sum_T \exp(\gamma(T)) - \gamma \cdot z$ with $\lambda = e^\gamma$; the code uses [Newton's method](/newton-method-for-systems/). The same distribution is the base of the [Karlin-Klein-Oveis Gharan algorithm](/karlin-klein-oveis-gharan-algorithm/) for symmetric TSP.

Line L7 is a least cost [circulation](/circulation-problem/) with flow at least 1 on each arc of $A$. With the directed triangle inequality, it reduces to a transport problem: a vertex with $b$ more arcs in than out sends $b$ units to the vertices with a deficit, and each unit uses a direct arc. The code solves this exactly with a dynamic program over subsets; in general a [min cost flow](/min-cost-flow-problem/) or an [assignment](/assignment-problem/) code does it. $F$ is balanced and contains a spanning tree, so it is strongly connected and line L8 can walk an [Euler circuit](/eulerian-circuit/).

## Example

Six vertices $A, \ldots, F$. The costs are the shortest path costs of a random complete digraph with arc costs from 1 to 9 (seed 23); the row is the tail and the column the head.

| | $A$ | $B$ | $C$ | $D$ | $E$ | $F$ |
|---|---|---|---|---|---|---|
| $A$ | 0 | 3 | 2 | 1 | 5 | 6 |
| $B$ | 4 | 0 | 6 | 5 | 3 | 4 |
| $C$ | 2 | 3 | 0 | 1 | 4 | 5 |
| $D$ | 1 | 2 | 2 | 0 | 5 | 6 |
| $E$ | 1 | 2 | 3 | 2 | 0 | 1 |
| $F$ | 4 | 1 | 5 | 3 | 4 | 0 |

OPT $= 13$, found by trying all tours. One run with the seed 2010 in the code on this page:

| line | result |
|---|---|
| L1 | $x = 1$ on $AC$, $EF$ and $x = 1/2$ on $BA$, $BE$, $CD$, $CE$, $DA$, $DB$, $FB$, $FD$; LP* $= 25/2$ |
| L2 | $z = 5/6$ on $\{A, C\}$, $\{E, F\}$ and $z = 5/12$ on the eight other pairs of the support |
| L3 | the support graph has 130 spanning trees; $\mathbb{E}[c(T)] = 55/6 \approx 9.17 \le (5/6)\,\text{LP}^* \approx 10.42$ |
| L4 | $k = 2\lceil \ln 6 \rceil = 4$ trees, of costs 9, 9, 11 and 9 |
| L5 | $T = \{AB, AC, BD, BF, EF\}$, the first tree of cost 9 |
| L6 | $A \to B$ (3), $A \to C$ (2), $D \to B$ (2), $F \to B$ (1), $E \to F$ (1), total 9 |
| L7 | in minus out: $A{:}{-2}$, $B{:}{+3}$, $C{:}{+1}$, $D{:}{-1}$, $E{:}{-1}$, $F{:}0$; extra arcs $B \to A$ two times, $B \to E$, $C \to D$, of cost $4 + 4 + 3 + 1 = 12$ |
| L8 | $W = A\,B\,A\,C\,D\,B\,E\,F\,B\,A$, of cost $9 + 12 = 21$ |
| L9 | $H = A\,B\,C\,D\,E\,F$, of cost 20 |

The tour costs 20 against OPT $= 13$. The thinness of $T$ is $9/5$, from the cut $U = \{B\}$: $T$ has 3 edges at $B$ and $z(\delta(B)) = 4 \cdot 5/12 = 5/3$. The proved bound for this tree is $c(T) + 2 \cdot \tfrac{9}{5} \cdot \text{LP}^* = 9 + 45 = 54$. With one sample instead of four, the expected tour cost over all 130 trees is about 14.64 and the worst is 23. On small instances the bound is weak and other methods do better; the strength of the method is its growth with $n$.

## Correctness

**Theorem (Asadpour et al.).** For $n \ge 5$, with probability at least $1 - O(1/n)$, ASADPOUR-ATSP returns a tour with

$$\text{ALG} \le \Big(2 + \frac{8 \ln n}{\ln\ln n}\Big) \cdot \text{LP}^* \le \Big(2 + \frac{8 \ln n}{\ln\ln n}\Big) \cdot \text{OPT}.$$

The ratio is with high probability, and it is a bound against the lower bound LP*. The proof has two parts.

1. **A thin tree gives a cheap tour (proved here).** A spanning tree $T$ is $\alpha$-thin if $|T \cap \delta(U)| \le \alpha \cdot z(\delta(U))$ for each cut $U$. Put lower bound 1 on the arcs of $A$ and upper bound $1 + 2\alpha x_a$ on each arc. Each cut has $x(\delta^+(U)) = x(\delta^-(U)) \ge z(\delta(U))/2$, so the condition of [Hoffman's circulation theorem](/hoffman-circulation-theorem/) holds, and a circulation of cost at most $c(T) + 2\alpha \cdot \text{LP}^*$ exists. Line L7 finds the least cost one, and shortcuts do not add cost. So $\text{ALG} \le c(T) + 2\alpha \cdot \text{LP}^*$ for each tree.
2. **The cheapest sample is cheap (proved here).** $\mathbb{E}[c(T)] \le (1 - 1/n)\text{LP}^*$ by linearity. By [Markov's inequality](/markov-inequality/), each sample costs more than $2 \cdot \text{LP}^*$ with probability at most 1/2, so all $k = 2\lceil \ln n \rceil$ samples do with probability at most $1/n$.
3. **Max entropy trees are thin (cited, with an outline).** A $\lambda$-uniform tree is $(4 \ln n / \ln\ln n)$-thin with probability at least $1 - 1/n$. The edges of such a tree are negatively correlated, so a [Chernoff bound](/chernoff-bound/) holds for each cut; Karger's bound on the number of near minimum cuts and a [union bound](/union-bound/) then cover all cuts.

The proof file gives parts 1 and 2 in full and part 3 as an outline.

**Integrality gap.** The proof gives an integrality gap of $O(\log n / \log\log n)$ for the ATSP LP. Later work shows that the gap is a constant, and the gap is at least 2 (Charikar, Goemans and Karloff 2006).

**Hardness.** ATSP is NP-hard to approximate within $75/74$ (Karlin, Lampis and Schmied 2015). Without the triangle inequality no ratio is possible unless P = NP, as for symmetric TSP; see [general TSP inapproximability](/general-tsp-inapproximability/).

## Complexity

- **Line L1.** The ATSP LP has a constraint for each cut, but a [separation oracle](/separation-oracle/) by min cuts and the [ellipsoid method](/ellipsoid-method/) solve it in polynomial time; a compact LP with flow variables works too.
- **Line L3.** Asadpour et al. compute weights whose marginals are within a factor $1 + \varepsilon$ of $z$ in time polynomial in $n$ and $\log(1/\varepsilon)$, and the analysis allows this error.
- **Line L4.** By the [matrix-tree theorem](/matrix-tree-theorem/), the total weight of the trees is a determinant, and a tree can be sampled one edge at a time with $O(m)$ determinants of size $n$ for $m$ edges in the support.
- **Lines L6 to L9.** The transport problem of line L7 has at most $n - 1$ units, so the [Hungarian algorithm](/hungarian-algorithm/) solves it in $O(n^3)$; the rest is $O(n)$.
- **Total.** Polynomial in $n$ in the [word RAM](/word-ram/), with $O(\log n)$ samples.

The code on this page is for small instances only. It solves the LP exactly with fractions and adds cut constraints over all $2^n - 2$ sets, lists all spanning trees of the support, and solves the transport problem by a dynamic program over subsets. This is exponential, but it makes each number in the example exact.

## Properties

- **Randomized, ratio with high probability.** The bound holds with probability $1 - O(1/n)$ over the samples, on each instance. The per tree bound $c(T) + 2\alpha_T \cdot \text{LP}^*$ holds always.
- **The directions are used only twice.** The LP of line L1 and the circulation of line L7 see the directions. The sampling sees only the undirected pairs.
- **Thinness is the measure.** Any method that finds an $\alpha$-thin tree of cost $s \cdot \text{LP}^*$ gives the ratio $2\alpha + s$. So better thin trees give better ratios.
- **Max entropy is needed for thinness, not for cost.** Any distribution with the marginals $z$ gives a cheap tree on average. The negative correlation of the max entropy distribution is what makes the tree thin in all cuts at once.

## Variants and improvements

- **Better thin trees.** Anari and Oveis Gharan (2015) showed that the ATSP LP has an integrality gap of $O(\log\log n)^{O(1)}$, by proving the existence of thin trees with a polyloglog bound; their proof does not give a polynomial algorithm.
- **The thin tree conjecture.** Goddyn conjectured that each $k$-edge-connected graph has an $O(1/k)$-thin spanning tree. This would give a constant integrality gap by the same route, and it is still open.
- **Graphs of bounded genus.** For ATSP on shortest path costs of planar graphs and of graphs of bounded genus, thin trees with a constant bound exist and give a constant ratio (Oveis Gharan and Saberi 2011).
- **Constant ratios.** Svensson, Tarnawski and Végh (2018) gave the first constant ratio for ATSP by a different method, and Traub and Vygen later lowered the constant to $22 + \varepsilon$. See [asymmetric TSP](/asymmetric-tsp/).
- **Other rounding.** [Dependent rounding](/dependent-rounding/) and [swap rounding](/swap-rounding/) for matroids also give negatively correlated trees with given marginals, and the same Chernoff bound applies to them.

## When to use it

Use this page to understand the thin tree method and the step below the $\log n$ ratio of the cycle cover algorithm of [Frieze, Galbiati and Maffioli](/asymmetric-tsp/). It is also the first use of max entropy spanning trees in approximation algorithms. For a constant ratio in theory, use the algorithm of Svensson, Tarnawski and Végh. For good tours in practice, transform the instance to a symmetric one and use [Lin-Kernighan-Helsgaun](/lin-kernighan-helsgaun/).

## Pitfalls

- **Directions kept in line L2.** The trees are undirected. A program that samples directed arborescences with the marginals $x$ solves a different problem, and the thinness argument does not apply to it. Line L2 must add $x_{uv}$ and $x_{vu}$.
- **A single sample in line L4.** One tree costs at most $(1 - 1/n)\text{LP}^*$ only on average. The $2\lceil \ln n \rceil$ samples and the choice of the cheapest in line L5 are what make the cost bound hold with high probability.
- **No triangle inequality in line L7.** The reduction of the circulation to direct arcs needs the directed triangle inequality. With raw road costs, an extra unit must follow a shortest path, so use the shortest path costs first. The shortcut of line L9 needs it too.
- **An unbalanced multigraph in line L8.** In the example, the arc $B \to A$ is needed two times. A program that stores $F$ as a set of arcs loses one copy, and the Euler circuit does not exist.
- **Thinness checked only on vertex cuts.** The definition needs all cuts $U$, not only single vertices. A tree with small degrees can still cross some larger cut many times.

## Implementations

## History

Frieze, Galbiati and Maffioli (1982) gave the ratio $\log_2 n$ for ATSP by repeated cycle covers, and the constant in front of $\log n$ was lowered several times in the next 25 years. Asadpour, Goemans, Mądry, Oveis Gharan and Saberi broke the order $\log n$ at SODA 2010 with thin trees and max entropy sampling; the journal version appeared in Operations Research in 2017. The same distributions led to the graphic TSP result of Oveis Gharan, Saberi and Singh (2011) and to the metric TSP result of Karlin, Klein and Oveis Gharan (2021). Anari and Oveis Gharan (2015) improved the bound on the integrality gap with thin trees, and Svensson, Tarnawski and Végh (2018) found the first constant ratio by another route.

## References
